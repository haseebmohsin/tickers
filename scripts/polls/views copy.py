from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import asyncio
import threading
import concurrent.futures
from asgiref.sync import async_to_sync,sync_to_async
import glob
import os
import json
from django.views.decorators.csrf import csrf_exempt
from google_ocr.ocr import Drive_OCR
all_data_comparer=0
from django.views.decorators.csrf import csrf_exempt
import uuid
@csrf_exempt
def index(request):
    if request.method=='POST':
            
            global all_data_comparer
            all_data_comparer=0
            searching_word=request.POST['wordsearched']
            channel_name_search=request.POST['channel_name']
            if channel_name_search=='option1':
                channel_name_search='Geo'
            if channel_name_search=='option2':
                channel_name_search='Ary'
            if channel_name_search=='option3':
                channel_name_search='Samaa'
            if channel_name_search=='option4':
                channel_name_search='Express'
            if channel_name_search=='option5':
                channel_name_search='Dunya'
            if channel_name_search=='option6':
                channel_name_search='NinetyTwo'


            print('channel_name',channel_name_search)
            date_search=request.POST['gettingdate']
            date_search_end=request.POST['gettingdateend']
            time_search=request.POST['gettingtime']
            if time_search:
                time_search=convert_time_format(time_search)
        
            time_search_end=request.POST['gettingtimeend']
            if time_search_end:
                time_search_end=convert_time_format(time_search_end)
            print('date_search',date_search)
            print('time',time_search)
            if  channel_name_search=='option0' and date_search and not searching_word and  date_search_end and not time_search and not time_search_end:
                result= Ticker_Extraction_Model.objects.filter(date__range=[date_search,date_search_end]).order_by('-id')
            if  channel_name_search=='option0' and not date_search and not searching_word and  not date_search_end and  time_search and  time_search_end:
                result= Ticker_Extraction_Model.objects.filter(time__range=(time_search,time_search_end)).order_by('-id')

            if  channel_name_search=='option0' and date_search and not searching_word and not date_search_end and not time_search and not time_search_end:
                result= Ticker_Extraction_Model.objects.filter(date=date_search).order_by('-id')
            if  channel_name_search=='option0' and not date_search and not searching_word and date_search_end and not time_search and not time_search_end:
                result= Ticker_Extraction_Model.objects.filter(date=date_search_end).order_by('-id')
            if  channel_name_search=='option0' and not date_search and not searching_word and not date_search_end and  time_search and not time_search_end:
                result= Ticker_Extraction_Model.objects.filter(time=time_search).order_by('-id')
            if  channel_name_search=='option0' and not date_search and not searching_word and not date_search_end and not time_search and  time_search_end:
                result= Ticker_Extraction_Model.objects.filter(time=time_search_end).order_by('-id')
            if not searching_word and channel_name_search == 'option0' and date_search and date_search_end and  time_search and time_search_end:
                result= Ticker_Extraction_Model.objects.filter(date__range=[date_search, date_search_end],time__range=(time_search,time_search_end)).order_by('-id')

            if not searching_word and channel_name_search != 'option0' and date_search and date_search_end and  time_search and time_search_end:
                result= Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search,date__range=[date_search, date_search_end],time__range=(time_search,time_search_end)).order_by('-id')
            if not searching_word and channel_name_search != 'option0'  and date_search and date_search_end and not time_search and not time_search_end:
                result= Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search,date__range=[date_search, date_search_end]).order_by('-id')
            if not searching_word and channel_name_search != 'option0' and not date_search and not date_search_end and time_search and  time_search_end:
                result = Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search,time__range=(time_search, time_search_end)).order_by('-id')


            if not searching_word and channel_name_search != 'option0' and date_search and not time_search and not date_search_end and not time_search_end:
                result=Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search,date=date_search).order_by('-id')
                print('result',result)
            if not searching_word and channel_name_search != 'option0' and time_search and not date_search and not date_search_end and not time_search_end:
                result=Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search ,time=time_search).order_by('-id')
            
            if not searching_word and channel_name_search != 'option0' and time_search and date_search and not date_search_end and not time_search_end:
                result=Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search ,time=time_search,date=date_search).order_by('-id')
            if not searching_word  and  channel_name_search == 'option0' and not date_search and  not time_search and not date_search_end and not time_search_end:
                # return render(request,'index.html')
                result=Ticker_Extraction_Model.objects.all().order_by('-id')
            if not searching_word and channel_name_search != 'option0' and not searching_word and not date_search and not date_search_end and not time_search and not time_search_end:
                result= Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search).order_by('-id')
            if searching_word and channel_name_search != 'option0' and  not date_search and  not date_search_end and  not time_search and not time_search_end:
                result= Ticker_Extraction_Model.objects.filter(text_ocr__icontains=searching_word,channel_name=channel_name_search).order_by('-id')


            if searching_word and channel_name_search != 'option0' and date_search and date_search_end and  time_search and time_search_end:
                result= Ticker_Extraction_Model.objects.filter(text_ocr__icontains=searching_word,channel_name=channel_name_search,date__range=[date_search, date_search_end],time__range=(time_search,time_search_end)).order_by('-id')
            if searching_word and channel_name_search != 'option0'  and date_search and date_search_end and not time_search and not time_search_end:
                result= Ticker_Extraction_Model.objects.filter(text_ocr__icontains=searching_word,channel_name=channel_name_search,date__range=[date_search, date_search_end]).order_by('-id')
            if searching_word and channel_name_search != 'option0' and not date_search and not date_search_end and time_search and  time_search_end:
                result = Ticker_Extraction_Model.objects.filter(text_ocr__icontains=searching_word,channel_name=channel_name_search,time__range=(time_search, time_search_end)).order_by('-id')


            if searching_word and channel_name_search != 'option0' and date_search and not time_search and not date_search_end and not time_search_end:
                result=Ticker_Extraction_Model.objects.filter(text_ocr__icontains=searching_word,channel_name=channel_name_search,date=date_search).order_by('-id')
                print('result',result)
            if searching_word and channel_name_search != 'option0' and time_search and not date_search and not date_search_end and not time_search_end:
                result=Ticker_Extraction_Model.objects.filter(text_ocr__icontains=searching_word,channel_name=channel_name_search ,time=time_search).order_by('-id')
            
            if searching_word and channel_name_search != 'option0' and time_search and date_search and not date_search_end and not time_search_end:
                result=Ticker_Extraction_Model.objects.filter(text_ocr__icontains=searching_word,channel_name=channel_name_search ,time=time_search,date=date_search).order_by('-id')
        
                

            if  channel_name_search == 'option0' and searching_word  and not date_search and  not time_search and not date_search_end and not time_search_end:
            # else :
                result=Ticker_Extraction_Model.objects.filter(text_ocr__icontains=searching_word).order_by('-id')

            if  channel_name_search == 'option0' and not searching_word and  not date_search and  not time_search and not date_search_end and not time_search_end:
                # return render(request,'index.html')
                result=Ticker_Extraction_Model.objects.all().order_by('-id')

                    # paginator = Paginator(result, 10)  # Show 10 items per page
                    
            global data_result
            data_result=result
            # page_number = request.GET.get('page')
            # page_obj = paginator.get_page(page_number)
            return render (request,'index.html',{'result':result[:10],'channel_name':channel_name_search})
    else:
   
        return render(request,'index.html',{'data':'data'})



counter_dunya=0
full_report_dunya=[]
import time
import subprocess
import cv2
all_files_with_names=[]
import random
import string
import os
import datetime
import shutil
import time
from rapidfuzz import fuzz
time_data=[]
# GEO NEWS IS RUNNING IN PLACE OF DUNYA NOW
import time
from .models import Ticker_Extraction_Model,Character_Comparison

def generate_unique_filename():
    unique_id = str(uuid.uuid4())
    valid_chars = string.ascii_letters + string.digits + "_-"
    filename = ''.join(c for c in unique_id if c in valid_chars)
    return filename
def file_remover(folder_name,extension_name,appended_file_name):
    # jpg_files = glob.glob('headline_checker/*.jpg')
    jpg_files = glob.glob(f'{folder_name}/*.jpg')

    sorted_files = sorted(jpg_files, key=lambda x: os.path.getctime(x))
    
    for i in sorted_files:
        print('os.path.basename(i[0:3])',os.path.basename(i)[0:3])
        # if os.path.basename(i)[0:3]=='Geo':
        if os.path.basename(i)[0:3]==extension_name:

            # geo_ticker_remove.append(i)
            appended_file_name.append(i)
    # print('geo_ticker_remove',geo_ticker_remove)
    if len(appended_file_name)>=100:
      for i in appended_file_name[0:96]:
          os.remove(i)
def dunya_ticker(request):


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
    # if convert_to_python==False:


    # Ticker_Extraction_Model.objects.all().delete()

        # global counter_dunya
        # global res_str_dunya

    time_data.clear()
    all_files_with_names.clear()


  
    # def one():

        
    # val.clear()
    test = [
        "streamlink",
        "--hls-duration", "1",  # Limit the duration to 4 seconds
        "--hls-live-edge", "99999",
        "--stream-segment-threads", "5",
        "--stream-timeout", "1215",
        "--force",
        "-o", r"opencv_videos/vid_dunya.mp4",
        "https://www.youtube.com/watch?v=O3DPVlynUM0",
        "480p",
        "--force"
    ]
    
    process = subprocess.run(test, universal_newlines=True)
    # time.sleep(1)

    # Wait for 4 seconds

    # Terminate the subprocess
    # process.terminate()
    ticker_video=f'opencv_videos/vid_dunya.mp4'

    vidcap = cv2.VideoCapture(ticker_video)
    total = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    value= int(vidcap.get(cv2.CAP_PROP_FPS))
    # print('val',value)
    # val.append(value)
    success,image = vidcap.read()
    # print('total',total)
    # print('valllllllll',value)
    width = 640 # keep original width
    height = 360
    dim = (width, height)
    count = 0
    lst=[]
    ticker_idx=0
    global geo_ticker_remove
    geo_ticker_remove=[]
 
    file_remover(folder_name='headline_checker',extension_name='Geo',appended_file_name=geo_ticker_remove)
    while success:
        print('count',count)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        # color = (255, 0, 0)
        # thickness = 2
        # image = cv2.rectangle(resized,  (250,526),(295,345), color, thickness)  
        if count % 50 == 0: 
            # cv2.imwrite("frames/%d.jpg" % count, image)     # save frame as JPEG file  
            # headline_checker=image[262:287,162:401]
            # cv2.imwrite('headline_checker/Geo.jpg',headline_checker)
            # text_ticker = Drive_OCR("headline_checker/Geo.jpg")
            # print('ob',ob.main())
            # if ob.main()=='Geo Headlines' or ob.main()=="جیو ہیڈلائنز":
            #     face=image[285:357,0:522]
            # else:
            face = image[265:357, 1:522]
            # image = cv2.imread(f'{resized}')
            # face = image[305:344, 1:520]
            # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
            
            characters = generate_unique_filename()

            # compare=Character_Comparison.objects.create(characters_comparing=characters)
            # if not Character_Comparison.objects.filter(characters_comparing__iexact=characters).exists():    
                
            cv2.imwrite(f"headline_checker/{'Geo'+characters}.jpg", face)  
                # cv2.imwrite(f"extract/{characters}.jpg", face)  

                # source = f"extract/{characters}.jpg"
                # # Destination path
                # destination = f"Dunya_Ticker/{characters}.jpg"
                
                # # Copy the content of
                # # source to destination
                
                # try:
                #     shutil.copy(source, destination)
                #     print("File copied successfully.")
                
                # # If source and destination are same
                # except shutil.SameFileError:
                #     print("Source and destination represents the same file.")
                
                # # If there is any permission issue
                # except PermissionError:
                #     print("Permission denied.")
                
                # # For other errors
                # except:
                #     print("Error occurred while copying file.")
            # else:
                    # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                   
                    # characters = generate_unique_filename()

                    # cv2.imwrite(f"Dunya_Ticker/{characters}.jpg", face)  
                # cv2.imwrite(f"extract/{characters}.jpg", face)  

                # source = f"extract/{characters}.jpg"
    
                # Destination path
                # destination = f"Dunya_Ticker/{characters}.jpg"
                
                # Copy the content of
                # source to destination
                
                # try:
                #     shutil.copy(source, destination)
                #     print("File copied successfully.")
                
                # # If source and destination are same
                # except shutil.SameFileError:
                #     print("Source and destination represents the same file.")
                
                # # If there is any permission issue
                # except PermissionError:
                #     print("Permission denied.")
                
                # # For other errors
                # except:
                #     print("Error occurred while copying file.")
            text_ticker = Drive_OCR(f"headline_checker/{'Geo'+characters}.jpg")

            # text_ticker=ob.main()
            print('text_ticker',text_ticker)
            if 'Headlines' in str(text_ticker) or "ہیڈلائنز" in str(text_ticker):

                face = image[286:349, 11:519]
                cv2.imwrite(f"Dunya_Ticker/{characters}.jpg", face)  
                print('TRUEEEEEEEEEEEEEEEE')
            else:
                face = image[305:344, 1:520]
                cv2.imwrite(f"Dunya_Ticker/{characters}.jpg", face)  
                print('FALSEEEEEEEEEEEEEEEE')


            print('text_ticker',text_ticker)
            if len(text_ticker)>=6:
                # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
                all_objects = Ticker_Extraction_Model.objects.all().order_by('-id')[:10]
                ticker_write=True
                # Compare text similarity with each object
                for obj in all_objects:
                    similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
                    
                    if similarity_ratio >= 50:
                        # os.remove(f"Dunya_Ticker/{characters}.jpg")
                        # print('I am similarity')
                        ticker_write=False
                        break
                        # matching_objects.append(obj)
                        # ticker_write=True
                if ticker_write:
                    # print('I am writing in database')
                    Ticker_Extraction_Model.objects.create(channel_name="Geo",channel_image="geo.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)
                    
                            


                # ticker_idx+=1 
        # cv2.imwrite("frame/%d.jpg" % count, image)     # save frame as JPEG file   
        
        success,image = vidcap.read()
        # print('Read a new frame: ', success)
        if not success:
            break
        # else:
        #      resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        count += 1
    vidcap.release()
    # if convert_to_python==False:
    #                 return JsonResponse({'success:success'}) 

    # if convert_to_python==True:    
    # def two():
    # all_tickers_files=Ticker_Extraction_Model.objects.filter(date=date,channel_name='Geo').order_by('-id')[:10]
    all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Geo').order_by('-id')[:10]

    for i in all_tickers_files:
        # file_name=os.path.basename(i)
        all_files_with_names.append(i.ticker_image)
        time_data.append(i.time)
            # print('all_ocr_result',all_ocr_result)
            
            
            
            
            # images_frames=glob.glob('frames/*.jpg')
            # for i in images_frames:
            #     image = cv2.imread(f'frames/{ticker_idx}.jpg')
            #     face = image[277:350, 32:553]
            #     cv2.imwrite(f"extract/{ticker_idx}.jpg", face)    
            #     ticker_idx+=1
            # # return HttpResponse('Done')
      
    # one_func=threading.Thread(target=one)
    # two_func=threading.Thread(target=two)
    # one_func.start()
    # two_func.start()
    # one_func.join()
    # two_func.join()

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers':all_files_with_names,'date':date,'time':formatted_time,'timedata':time_data}) 
    
        
            
            # return JsonResponse({'all_tickers':sorted(all_files_with_names,key=len),'date':date,'time':formatted_time}) 
#    <xmin>32</xmin>
#     <ymin>277</ymin>
#     <xmax>553</xmax>
#     <ymax>350</ymax>
result_all=[]

from django.core.paginator import Paginator
# searching is working from index not this one
def searching_queries(request):
    global all_data_comparer
    all_data_comparer=0
    channel_name_search=request.POST['channel_name']
    if channel_name_search=='option1':
        channel_name_search='Dunya'
    print('channel_name',channel_name_search)
    date_search=request.POST['gettingdate']
    date_search_end=request.POST['gettingdateend']
    time_search=request.POST['gettingtime']
    if time_search:
        time_search=convert_time_format(time_search)
  
    time_search_end=request.POST['gettingtimeend']
    if time_search_end:
        time_search_end=convert_time_format(time_search_end)
    # print('date_search',date_search)
    # print('time',time_search)
        
    if channel_name_search != 'option0' and date_search and date_search_end and  time_search and time_search_end:
        result= Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search,date__range=[date_search, date_search_end],time__range=(time_search,time_search_end)).order_by('-id')
    if channel_name_search != 'option0'  and date_search and date_search_end and not time_search and not time_search_end:
        result= Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search,date__range=[date_search, date_search_end])
    if channel_name_search != 'option0' and not date_search and not date_search_end and time_search and  time_search_end:
       result = Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search,time__range=(time_search, time_search_end))


    if channel_name_search != 'option0' and date_search and not time_search and not date_search_end and not time_search_end:
        result=Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search,date=date_search)
        print('result',result)
    elif channel_name_search != 'option0' and time_search and not date_search and not date_search_end and not time_search_end:
        result=Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search ,time=time_search)
    
    elif channel_name_search != 'option0' and time_search and date_search and not date_search_end and not time_search_end:
        resut=Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search ,time=time_search,date=date_search)
    if channel_name_search == 'option0' and not date_search and  not time_search and not date_search_end and not time_search_end:
        return render(request,'index.html')
    else :

            # paginator = Paginator(result, 10)  # Show 10 items per page
            
            global data_result
            data_result=result
            # page_number = request.GET.get('page')
            # page_obj = paginator.get_page(page_number)
            return render (request,'index.html',{'result':result[:10]})
   

def convert_time_format(time_str):
    # Parse the time string into a datetime object
    time_obj = datetime.datetime.strptime(time_str, "%H:%M")
    
    # Convert the time to 12-hour format with AM/PM indicator
    formatted_time = time_obj.strftime("%I:%M %p")
    
    return formatted_time



from django.core.paginator import Paginator
from django.shortcuts import render

def table_view(request):
    global all_data_comparer
    
    data = data_result[10:]
    lenght_of_data=len(data_result)
    if all_data_comparer<=lenght_of_data:
        paginator = Paginator(data, 10)  # Display 10 entries per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        all_data_comparer+=10
        # print('length_data',lenght_of_data)
        # print('all_data_comparer',all_data_comparer)
        return render(request, 'index.html', {'result': page_obj,'clear':'True'})

    elif all_data_comparer>lenght_of_data:
      paginator = Paginator(data, 0)
      page_number = request.GET.get('page')
      page_obj = paginator.get_page(page_number)
      all_data_comparer=0
 
      return render(request, 'index.html',)
timedata_ary=[]
all_files_with_names_ary=[]
def ary_ticker(request):
    

    

    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    timedata_ary.clear()
    all_files_with_names_ary.clear()
    test = [
        "streamlink",
        "--hls-duration", "1",  # Limit the duration to 4 seconds
        "--hls-live-edge", "99999",
        "--stream-segment-threads", "5",
        "--stream-timeout", "1215",
        "--force",
        "-o", r"opencv_videos/vid_ary.mp4",
        "https://www.youtube.com/watch?v=sUKwTVAc0Vo",
        "480p",
        "--force"
    ]
    
    process = subprocess.run(test, universal_newlines=True)
    # time.sleep(1)

    ticker_video=f'opencv_videos/vid_ary.mp4'

    vidcap = cv2.VideoCapture(ticker_video)
    total = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    value= int(vidcap.get(cv2.CAP_PROP_FPS))
    print('val',value)
    # val.append(value)
    success,image = vidcap.read()
    print('total',total)
    print('valllllllll',value)
    width = 640 # keep original width
    height = 360
    dim = (width, height)
    count = 0
    lst=[]
    ticker_idx=0
    # all_tickers_remove=glob.glob('extract/*.jpg')
    # for i in all_tickers_remove:
    #     os.remove(i)

    while success:
        print('count',count)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
       
        if count % 50 == 0: 
            cv2.imwrite("frames/%d.jpg" % count, image)     # save frame as JPEG file  
            # image = cv2.imread(f'{resized}')
            face = image[302:359, 0:531]
            # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
           
            characters = generate_unique_filename()

            # compare=Character_Comparison.objects.create(characters_comparing=characters)
            # if not Character_Comparison.objects.filter(characters_comparing__iexact=characters).exists():    
                
            cv2.imwrite(f"Ary_Ticker/{characters}.jpg", face)  
                # cv2.imwrite(f"extract/{characters}.jpg", face)  

                # source = f"extract/{characters}.jpg"
                # # Destination path
                # destination = f"Dunya_Ticker/{characters}.jpg"
                
                # # Copy the content of
                # # source to destination
                
                # try:
                #     shutil.copy(source, destination)
                #     print("File copied successfully.")
                
                # # If source and destination are same
                # except shutil.SameFileError:
                #     print("Source and destination represents the same file.")
                
                # # If there is any permission issue
                # except PermissionError:
                #     print("Permission denied.")
                
                # # For other errors
                # except:
                #     print("Error occurred while copying file.")
            # else:
                    # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                  
                    # characters = generate_unique_filename()

                    # cv2.imwrite(f"Ary_Ticker/{characters}.jpg", face)  
                # cv2.imwrite(f"extract/{characters}.jpg", face)  

                # source = f"extract/{characters}.jpg"
    
                # Destination path
                # destination = f"Dunya_Ticker/{characters}.jpg"
                
                # Copy the content of
                # source to destination
                
                # try:
                #     shutil.copy(source, destination)
                #     print("File copied successfully.")
                
                # # If source and destination are same
                # except shutil.SameFileError:
                #     print("Source and destination represents the same file.")
                
                # # If there is any permission issue
                # except PermissionError:
                #     print("Permission denied.")
                
                # # For other errors
                # except:
                #     print("Error occurred while copying file.")
            text_ticker = Drive_OCR(f"Ary_Ticker/{characters}.jpg")

            # text_ticker=ob.main()
            print('text_ticker',text_ticker)
            if len(text_ticker)>=6:
                # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
                all_objects = Ticker_Extraction_Model.objects.all().order_by('-id')[:10]
                ticker_write=True
                # Compare text similarity with each object
                for obj in all_objects:
                    similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
                    
                    if similarity_ratio >= 50:
                        # os.remove(f"Dunya_Ticker/{characters}.jpg")
                        print('I am similarity')
                        ticker_write=False
                        break
                        # matching_objects.append(obj)
                        # ticker_write=True
                if ticker_write:
                    print('I am writing in database')
                    Ticker_Extraction_Model.objects.create(channel_name="Ary",channel_image="ary.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

                            


                # ticker_idx+=1 
        # cv2.imwrite("frame/%d.jpg" % count, image)     # save frame as JPEG file   
        
        success,image = vidcap.read()
        # print('Read a new frame: ', success)
        if not success:
            break
        # else:
        #      resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        count += 1
    vidcap.release()
    # if convert_to_python==False:
    #                 return JsonResponse({'success:success'}) 

    # if convert_to_python==True:    
    # def two():
    # all_tickers_files=Ticker_Extraction_Model.objects.filter(date=date,channel_name='Ary').order_by('-id')[:10]
    all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Ary').order_by('-id')[:10]

    for i in all_tickers_files:
        # file_name=os.path.basename(i)
        all_files_with_names_ary.append(i.ticker_image)
        timedata_ary.append(i.time)
            # print('all_ocr_result',all_ocr_result)
            
            
            
            
            # images_frames=glob.glob('frames/*.jpg')
            # for i in images_frames:
            #     image = cv2.imread(f'frames/{ticker_idx}.jpg')
            #     face = image[277:350, 32:553]
            #     cv2.imwrite(f"extract/{ticker_idx}.jpg", face)    
            #     ticker_idx+=1
            # # return HttpResponse('Done')
      
    # one_func=threading.Thread(target=one)
    # two_func=threading.Thread(target=two)
    # one_func.start()
    # two_func.start()
    # one_func.join()
    # two_func.join()

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers':all_files_with_names_ary,'date':date,'time':formatted_time,'timedata':timedata_ary}) 
    




timedata_samaa=[]
all_files_with_names_samaa=[]
def samaa_ticker(request):
    

    

    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    timedata_samaa.clear()
    all_files_with_names_samaa.clear()
    test = [
        "streamlink",
        "--hls-duration", "1",  # Limit the duration to 4 seconds
        "--hls-live-edge", "99999",
        "--stream-segment-threads", "5",
        "--stream-timeout", "1215",
        "--force",
        "-o", r"opencv_videos/vid_samaa.mp4",
        "https://www.youtube.com/watch?v=rYrDIHRFzOU",
        "480p",
        "--force"
    ]
    
    process = subprocess.run(test, universal_newlines=True)
    # time.sleep(1)

    ticker_video=f'opencv_videos/vid_samaa.mp4'

    vidcap = cv2.VideoCapture(ticker_video)
    total = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    value= int(vidcap.get(cv2.CAP_PROP_FPS))
    # print('val',value)
    # val.append(value)
    success,image = vidcap.read()
    # print('total',total)
    # print('valllllllll',value)
    width = 640 # keep original width
    height = 360
    dim = (width, height)
    count = 0
    lst=[]
    ticker_idx=0
    global samaa_ticker_remove
    samaa_ticker_remove=[]
    # all_tickers_remove=glob.glob('extract/*.jpg')
    # for i in all_tickers_remove:
    #     os.remove(i)
    
    file_remover(folder_name='headline_checker',extension_name='Sam',appended_file_name=samaa_ticker_remove)

    while success:
        print('count',count)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
       
        if count % 50 == 0: 
            # cv2.imwrite("frames/%d.jpg" % count, image)     # save frame as JPEG file  
            # image = cv2.imread(f'{resized}')
          


            face = image[257:341, 2:514]
            # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
          
            characters = generate_unique_filename()

            # compare=Character_Comparison.objects.create(characters_comparing=characters)
            # if not Character_Comparison.objects.filter(characters_comparing__iexact=characters).exists():    
            cv2.imwrite(f"headline_checker/{'Samaa'+characters}.jpg",face)    
            # cv2.imwrite(f"Samaa_Ticker/{characters}.jpg", face)  
                # cv2.imwrite(f"extract/{characters}.jpg", face)  

                # source = f"extract/{characters}.jpg"
                # # Destination path
                # destination = f"Dunya_Ticker/{characters}.jpg"
                
                # # Copy the content of
                # # source to destination
                
                # try:
                #     shutil.copy(source, destination)
                #     print("File copied successfully.")
                
                # # If source and destination are same
                # except shutil.SameFileError:
                #     print("Source and destination represents the same file.")
                
                # # If there is any permission issue
                # except PermissionError:
                #     print("Permission denied.")
                
                # # For other errors
                # except:
                #     print("Error occurred while copying file.")
            # else:
                    # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                    

                    # Remove any invalid characters from the UUID string
                   
                    # characters = generate_unique_filename()

                    # cv2.imwrite(f"Samaa_Ticker/{characters}.jpg", face)  
                # cv2.imwrite(f"extract/{characters}.jpg", face)  

                # source = f"extract/{characters}.jpg"
    
                # Destination path
                # destination = f"Dunya_Ticker/{characters}.jpg"
                
                # Copy the content of
                # source to destination
                
                # try:
                #     shutil.copy(source, destination)
                #     print("File copied successfully.")
                
                # # If source and destination are same
                # except shutil.SameFileError:
                #     print("Source and destination represents the same file.")
                
                # # If there is any permission issue
                # except PermissionError:
                #     print("Permission denied.")
                
                # # For other errors
                # except:
                #     print("Error occurred while copying file.")
            text_ticker = Drive_OCR(f"headline_checker/{'Samaa'+characters}.jpg")

            # text_ticker=ob.main()
            if 'Headlines' in str(text_ticker) or "ہیڈلائنز" in str(text_ticker):
                face=image[281:335,2:514]
                cv2.imwrite(f'Samaa_Ticker/{characters}.jpg',face)
            else:
                face = image[305:345, 1:515]
                cv2.imwrite(f'Samaa_Ticker/{characters}.jpg',face)



            # print('text_ticker',text_ticker)
            if len(text_ticker)>=6:
                # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
                all_objects = Ticker_Extraction_Model.objects.all().order_by('-id')[:10]
                ticker_write=True
                # Compare text similarity with each object
                for obj in all_objects:
                    similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
                    
                    if similarity_ratio >= 50:
                        # os.remove(f"Dunya_Ticker/{characters}.jpg")
                        print('I am similarity')
                        ticker_write=False
                        break
                        # matching_objects.append(obj)
                        # ticker_write=True
                if ticker_write:
                    print('I am writing in database')
                    Ticker_Extraction_Model.objects.create(channel_name="Samaa",channel_image="Samaa_logo.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

                            


                # ticker_idx+=1 
        # cv2.imwrite("frame/%d.jpg" % count, image)     # save frame as JPEG file   
        
        success,image = vidcap.read()
        # print('Read a new frame: ', success)
        if not success:
            break
        # else:
        #      resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        count += 1
    vidcap.release()
    # if convert_to_python==False:
    #                 return JsonResponse({'success:success'}) 

    # if convert_to_python==True:    
    # def two():
    # all_tickers_files=Ticker_Extraction_Model.objects.filter(date=date,channel_name='Samaa').order_by('-id')[:10]
    all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Samaa').order_by('-id')[:10]

    for i in all_tickers_files:
        # file_name=os.path.basename(i)
        all_files_with_names_samaa.append(i.ticker_image)
        timedata_samaa.append(i.time)
            # print('all_ocr_result',all_ocr_result)
            
            
            
            
            # images_frames=glob.glob('frames/*.jpg')
            # for i in images_frames:
            #     image = cv2.imread(f'frames/{ticker_idx}.jpg')
            #     face = image[277:350, 32:553]
            #     cv2.imwrite(f"extract/{ticker_idx}.jpg", face)    
            #     ticker_idx+=1
            # # return HttpResponse('Done')
      
    # one_func=threading.Thread(target=one)
    # two_func=threading.Thread(target=two)
    # one_func.start()
    # two_func.start()
    # one_func.join()
    # two_func.join()

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers':all_files_with_names_samaa,'date':date,'time':formatted_time,'timedata':timedata_samaa}) 


timedata_express=[]
all_files_with_names_express=[]
def express_ticker(request):
    

    

    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    timedata_express.clear()
    all_files_with_names_express.clear()
    test = [
        "streamlink",
        "--hls-duration", "1",  # Limit the duration to 4 seconds
        "--hls-live-edge", "99999",
        "--stream-segment-threads", "5",
        "--stream-timeout", "1215",
        "--force",
        "-o", r"opencv_videos/vid_express.mp4",
        "https://www.youtube.com/watch?v=muBr6a3Xi2c",
        "480p",
        "--force"
    ]
    
    process = subprocess.run(test, universal_newlines=True)
    # time.sleep(1)

    ticker_video=f'opencv_videos/vid_express.mp4'

    vidcap = cv2.VideoCapture(ticker_video)
    total = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    value= int(vidcap.get(cv2.CAP_PROP_FPS))
    # print('val',value)
    # val.append(value)
    success,image = vidcap.read()
    # print('total',total)
    # print('valllllllll',value)
    width = 640 # keep original width
    height = 360
    dim = (width, height)
    count = 0
    lst=[]
    ticker_idx=0
    # all_tickers_remove=glob.glob('extract/*.jpg')
    # for i in all_tickers_remove:
    #     os.remove(i)

    while success:
        print('count',count)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
       
        if count % 50 == 0: 
            cv2.imwrite("frames/%d.jpg" % count, image)     # save frame as JPEG file  
            # image = cv2.imread(f'{resized}')
            face = image[310:358, 0:495]
            # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
            unique_id = str(uuid.uuid4())
            # print('unique_id',unique_id)

            # Remove any invalid characters from the UUID string
            # valid_chars = string.ascii_letters + string.digits + "_-"
            # print('valid_chars',valid_chars)
            # checker=(c for c in unique_id if c in valid_chars)
            # print('checker',list(checker))
            characters = generate_unique_filename()

            # compare=Character_Comparison.objects.create(characters_comparing=characters)
            # if not Character_Comparison.objects.filter(characters_comparing__iexact=characters).exists():    
                
            cv2.imwrite(f"Express_Ticker/{characters}.jpg", face)  
                # cv2.imwrite(f"extract/{characters}.jpg", face)  

                # source = f"extract/{characters}.jpg"
                # # Destination path
                # destination = f"Dunya_Ticker/{characters}.jpg"
                
                # # Copy the content of
                # # source to destination
                
                # try:
                #     shutil.copy(source, destination)
                #     print("File copied successfully.")
                
                # # If source and destination are same
                # except shutil.SameFileError:
                #     print("Source and destination represents the same file.")
                
                # # If there is any permission issue
                # except PermissionError:
                #     print("Permission denied.")
                
                # # For other errors
                # except:
                #     print("Error occurred while copying file.")
            # else:
            #         # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                    
            #         characters = generate_unique_filename()
            #         cv2.imwrite(f"Express_Ticker/{characters}.jpg", face)  
                # cv2.imwrite(f"extract/{characters}.jpg", face)  

                # source = f"extract/{characters}.jpg"
    
                # Destination path
                # destination = f"Dunya_Ticker/{characters}.jpg"
                
                # Copy the content of
                # source to destination
                
                # try:
                #     shutil.copy(source, destination)
                #     print("File copied successfully.")
                
                # # If source and destination are same
                # except shutil.SameFileError:
                #     print("Source and destination represents the same file.")
                
                # # If there is any permission issue
                # except PermissionError:
                #     print("Permission denied.")
                
                # # For other errors
                # except:
                #     print("Error occurred while copying file.")
            text_ticker = Drive_OCR(f"Express_Ticker/{characters}.jpg")

            # text_ticker=ob.main()
            # print('text_ticker',text_ticker)
            if len(text_ticker)>=6:
                # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
                all_objects = Ticker_Extraction_Model.objects.all().order_by('-id')[:10]
                ticker_write=True
                # Compare text similarity with each object
                for obj in all_objects:
                    similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
                    
                    if similarity_ratio >= 70:
                        # os.remove(f"Dunya_Ticker/{characters}.jpg")
                        print('I am similarity')
                        ticker_write=False
                        break
                        # matching_objects.append(obj)
                        # ticker_write=True
                if ticker_write:
                    print('I am writing in database')
                    Ticker_Extraction_Model.objects.create(channel_name="Express",channel_image="express.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

                            


                # ticker_idx+=1 
        # cv2.imwrite("frame/%d.jpg" % count, image)     # save frame as JPEG file   
        
        success,image = vidcap.read()
        # print('Read a new frame: ', success)
        if not success:
            break
        # else:
        #      resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        count += 1
    vidcap.release()
    # if convert_to_python==False:
    #                 return JsonResponse({'success:success'}) 

    # if convert_to_python==True:    
    # def two():
    # all_tickers_files=Ticker_Extraction_Model.objects.filter(date=date,channel_name='Express').order_by('-id')[:10]
    all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Express').order_by('-id')[:10]

    for i in all_tickers_files:
        # file_name=os.path.basename(i)
        all_files_with_names_express.append(i.ticker_image)
        timedata_express.append(i.time)
            # print('all_ocr_result',all_ocr_result)
            
            
            
            
            # images_frames=glob.glob('frames/*.jpg')
            # for i in images_frames:
            #     image = cv2.imread(f'frames/{ticker_idx}.jpg')
            #     face = image[277:350, 32:553]
            #     cv2.imwrite(f"extract/{ticker_idx}.jpg", face)    
            #     ticker_idx+=1
            # # return HttpResponse('Done')
      
    # one_func=threading.Thread(target=one)
    # two_func=threading.Thread(target=two)
    # one_func.start()
    # two_func.start()
    # one_func.join()
    # two_func.join()

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers':all_files_with_names_express,'date':date,'time':formatted_time,'timedata':timedata_express}) 

# inside geo the dunya is running and inside dunya the geo is running
timedata_geo=[]
all_files_with_names_geo=[]
def geo_ticker(request):
    

    

    # start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    timedata_geo.clear()
    all_files_with_names_geo.clear()
    start_time = time.time()  # Get the current time

    test = [
        "streamlink",
        "--hls-duration", "1",  # Limit the duration to 4 seconds
        "--hls-live-edge", "99999",
        "--stream-segment-threads", "5",
        "--stream-timeout", "1215",
        "--force",
        "-o", r"opencv_videos/vid_geo.mp4",
        "https://www.youtube.com/watch?v=_Q6X1VylryE",
        "480p",
        "--force"
    ]
    
    process = subprocess.run(test, universal_newlines=True)
    # time.sleep(1)
    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"File Download executed in {execution_time:.2f} seconds")
    ticker_video=f'opencv_videos/vid_geo.mp4'

    vidcap = cv2.VideoCapture(ticker_video)
    total = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    value= int(vidcap.get(cv2.CAP_PROP_FPS))
    # print('val',value)
    # val.append(value)
    success,image = vidcap.read()
    # print('total',total)
    # print('valllllllll',value)
    width = 640 # keep original width
    height = 360
    dim = (width, height)
    count = 0
    lst=[]
    ticker_idx=0
    # all_tickers_remove=glob.glob('extract/*.jpg')
    # for i in all_tickers_remove:z
    #     os.remove(i)

    while success:
        print('count',count)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
       
        if count % 50 == 0: 
            cv2.imwrite("frames/%d.jpg" % count, image)     # save frame as JPEG file  
            # image = cv2.imread(f'{resized}')
            face = image[297:335, 89:550]
            # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
            unique_id = str(uuid.uuid4())
            # print('unique_id',unique_id)

            # Remove any invalid characters from the UUID string
            # valid_chars = string.ascii_letters + string.digits + "_-"
            # print('valid_chars',valid_chars)
            # checker=(c for c in unique_id if c in valid_chars)
            # print('checker',list(checker))
            characters = generate_unique_filename()

            # compare=Character_Comparison.objects.create(characters_comparing=characters)
            # if not Character_Comparison.objects.filter(characters_comparing__iexact=characters).exists():    
                
            cv2.imwrite(f"Geo_Ticker/{characters}.jpg", face)  
                # cv2.imwrite(f"extract/{characters}.jpg", face)  

                # source = f"extract/{characters}.jpg"
                # # Destination path
                # destination = f"Dunya_Ticker/{characters}.jpg"
                
                # # Copy the content of
                # # source to destination
                
                # try:
                #     shutil.copy(source, destination)
                #     print("File copied successfully.")
                
                # # If source and destination are same
                # except shutil.SameFileError:
                #     print("Source and destination represents the same file.")
                
                # # If there is any permission issue
                # except PermissionError:
                #     print("Permission denied.")
                
                # # For other errors
                # except:
                #     print("Error occurred while copying file.")
            # else:
            #         # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                    
            #         characters = generate_unique_filename()
            #         cv2.imwrite(f"Express_Ticker/{characters}.jpg", face)  
                # cv2.imwrite(f"extract/{characters}.jpg", face)  

                # source = f"extract/{characters}.jpg"
    
                # Destination path
                # destination = f"Dunya_Ticker/{characters}.jpg"
                
                # Copy the content of
                # source to destination
                
                # try:
                #     shutil.copy(source, destination)
                #     print("File copied successfully.")
                
                # # If source and destination are same
                # except shutil.SameFileError:
                #     print("Source and destination represents the same file.")
                
                # # If there is any permission issue
                # except PermissionError:
                #     print("Permission denied.")
                
                # # For other errors
                # except:
                #     print("Error occurred while copying file.")
            text_ticker = Drive_OCR(f"Geo_Ticker/{characters}.jpg")

            # text_ticker=ob.main()
            # print('text_ticker',text_ticker)
            if len(text_ticker)>=6:
                # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
                all_objects = Ticker_Extraction_Model.objects.all().order_by('-id')[:10]
                ticker_write=True
                # Compare text similarity with each object
                for obj in all_objects:
                    similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
                    
                    if similarity_ratio >= 50:
                        # os.remove(f"Dunya_Ticker/{characters}.jpg")
                        print('I am similarity')
                        ticker_write=False
                        break
                        # matching_objects.append(obj)
                        # ticker_write=True
                if ticker_write:
                    print('I am writing in database')
                    Ticker_Extraction_Model.objects.create(channel_name="Dunya",channel_image="mzl-ftpchoha.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

                            


                # ticker_idx+=1 
        # cv2.imwrite("frame/%d.jpg" % count, image)     # save frame as JPEG file   
        
        success,image = vidcap.read()
        # print('Read a new frame: ', success)
        if not success:
            break
        # else:
        #      resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        count += 1
    vidcap.release()
    # if convert_to_python==False:
    #                 return JsonResponse({'success:success'}) 

    # if convert_to_python==True:    
    # def two():
    # all_tickers_files=Ticker_Extraction_Model.objects.filter(date=date,channel_name='Express').order_by('-id')[:10]
    all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Dunya').order_by('-id')[:10]

    for i in all_tickers_files:
        # file_name=os.path.basename(i)
        all_files_with_names_geo.append(i.ticker_image)
        timedata_geo.append(i.time)
            # print('all_ocr_result',all_ocr_result)
            
            
            
            
            # images_frames=glob.glob('frames/*.jpg')
            # for i in images_frames:
            #     image = cv2.imread(f'frames/{ticker_idx}.jpg')
            #     face = image[277:350, 32:553]
            #     cv2.imwrite(f"extract/{ticker_idx}.jpg", face)    
            #     ticker_idx+=1
            # # return HttpResponse('Done')
      
    # one_func=threading.Thread(target=one)
    # two_func=threading.Thread(target=two)
    # one_func.start()
    # two_func.start()
    # one_func.join()
    # two_func.join()

    # end_time = time.time()  # Get the current time after the task is completed
    # execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers':all_files_with_names_geo,'date':date,'time':formatted_time,'timedata':timedata_geo}) 

timedata_ninety_two=[]
all_files_with_names_ninety_two=[]
def ninety_two_ticker(request):
    

    

    # start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    timedata_ninety_two.clear()
    all_files_with_names_ninety_two.clear()
    start_time = time.time()  # Get the current time

    test = [
        "streamlink",
        "--hls-duration", "1",  # Limit the duration to 4 seconds
        "--hls-live-edge", "99999",
        "--stream-segment-threads", "5",
        "--stream-timeout", "1215",
        "--force",
        "-o", r"opencv_videos/vid_ninety_two.mp4",
        "https://www.youtube.com/@92newshdTv/live",
        "480p",
        "--force"
    ]
    
    process = subprocess.run(test, universal_newlines=True)
    # time.sleep(1)
    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"File Download executed in {execution_time:.2f} seconds")
    ticker_video=f'opencv_videos/vid_ninety_two.mp4'

    vidcap = cv2.VideoCapture(ticker_video)
    total = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    value= int(vidcap.get(cv2.CAP_PROP_FPS))
    # print('val',value)
    # val.append(value)
    success,image = vidcap.read()
    # print('total',total)
    # print('valllllllll',value)
    width = 640 # keep original width
    height = 360
    dim = (width, height)
    count = 0
    lst=[]
    ticker_idx=0
    # all_tickers_remove=glob.glob('extract/*.jpg')
    # for i in all_tickers_remove:z
    #     os.remove(i)

    while success:
        print('count',count)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
       
        if count % 50 == 0: 
            cv2.imwrite("frames/%d.jpg" % count, image)     # save frame as JPEG file  
            # image = cv2.imread(f'{resized}')
            face = image[297:335, 89:550]
            # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
            unique_id = str(uuid.uuid4())
            # print('unique_id',unique_id)

            # Remove any invalid characters from the UUID string
            # valid_chars = string.ascii_letters + string.digits + "_-"
            # print('valid_chars',valid_chars)
            # checker=(c for c in unique_id if c in valid_chars)
            # print('checker',list(checker))
            characters = generate_unique_filename()

            # compare=Character_Comparison.objects.create(characters_comparing=characters)
            # if not Character_Comparison.objects.filter(characters_comparing__iexact=characters).exists():    
                
            cv2.imwrite(f"NinetyTwo_Ticker/{characters}.jpg", face)  
                # cv2.imwrite(f"extract/{characters}.jpg", face)  

                # source = f"extract/{characters}.jpg"
                # # Destination path
                # destination = f"Dunya_Ticker/{characters}.jpg"
                
                # # Copy the content of
                # # source to destination
                
                # try:
                #     shutil.copy(source, destination)
                #     print("File copied successfully.")
                
                # # If source and destination are same
                # except shutil.SameFileError:
                #     print("Source and destination represents the same file.")
                
                # # If there is any permission issue
                # except PermissionError:
                #     print("Permission denied.")
                
                # # For other errors
                # except:
                #     print("Error occurred while copying file.")
            # else:
            #         # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                    
            #         characters = generate_unique_filename()
            #         cv2.imwrite(f"Express_Ticker/{characters}.jpg", face)  
                # cv2.imwrite(f"extract/{characters}.jpg", face)  

                # source = f"extract/{characters}.jpg"
    
                # Destination path
                # destination = f"Dunya_Ticker/{characters}.jpg"
                
                # Copy the content of
                # source to destination
                
                # try:
                #     shutil.copy(source, destination)
                #     print("File copied successfully.")
                
                # # If source and destination are same
                # except shutil.SameFileError:
                #     print("Source and destination represents the same file.")
                
                # # If there is any permission issue
                # except PermissionError:
                #     print("Permission denied.")
                
                # # For other errors
                # except:
                #     print("Error occurred while copying file.")
            text_ticker = Drive_OCR(f"NinetyTwo_Ticker/{characters}.jpg")

            # text_ticker=ob.main()
            # print('text_ticker',text_ticker)
            if len(text_ticker)>=6:
                # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
                all_objects = Ticker_Extraction_Model.objects.all().order_by('-id')[:10]
                ticker_write=True
                # Compare text similarity with each object
                for obj in all_objects:
                    similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
                    
                    if similarity_ratio >= 50:
                        # os.remove(f"Dunya_Ticker/{characters}.jpg")
                        print('I am similarity')
                        ticker_write=False
                        break
                        # matching_objects.append(obj)
                        # ticker_write=True
                if ticker_write:
                    print('I am writing in database')
                    Ticker_Extraction_Model.objects.create(channel_name="NinetyTwo",channel_image="ninety_two.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

                            


                # ticker_idx+=1 
        # cv2.imwrite("frame/%d.jpg" % count, image)     # save frame as JPEG file   
        
        success,image = vidcap.read()
        # print('Read a new frame: ', success)
        if not success:
            break
        # else:
        #      resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        count += 1
    vidcap.release()
    # if convert_to_python==False:
    #                 return JsonResponse({'success:success'}) 

    # if convert_to_python==True:    
    # def two():
    # all_tickers_files=Ticker_Extraction_Model.objects.filter(date=date,channel_name='Express').order_by('-id')[:10]
    all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='NinetyTwo').order_by('-id')[:10]

    for i in all_tickers_files:
        # file_name=os.path.basename(i)
        all_files_with_names_ninety_two.append(i.ticker_image)
        timedata_ninety_two.append(i.time)
            # print('all_ocr_result',all_ocr_result)
            
            
            
            
            # images_frames=glob.glob('frames/*.jpg')
            # for i in images_frames:
            #     image = cv2.imread(f'frames/{ticker_idx}.jpg')
            #     face = image[277:350, 32:553]
            #     cv2.imwrite(f"extract/{ticker_idx}.jpg", face)    
            #     ticker_idx+=1
            # # return HttpResponse('Done')
      
    # one_func=threading.Thread(target=one)
    # two_func=threading.Thread(target=two)
    # one_func.start()
    # two_func.start()
    # one_func.join()
    # two_func.join()

    # end_time = time.time()  # Get the current time after the task is completed
    # execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers':all_files_with_names_ninety_two,'date':date,'time':formatted_time,'timedata':timedata_ninety_two}) 

import numpy as np

import numpy as np
import cv2
@csrf_exempt
def getting_live_collage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        getting_name = data.get('channelNameValue')
        print('i am channel', getting_name)
        getting_live_collage_list = data.get('liveCollageList')
        all_images_files = []
        image_width = 700
        image_height = 100
        for i in getting_live_collage_list:
            if getting_name == 'option1':
                logo = cv2.imread('image_detections/geo.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Dunya_Ticker/' + os.path.basename(i))
            elif getting_name == 'option2':
                logo = cv2.imread('image_detections/ary.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Ary_Ticker/' + os.path.basename(i))
            elif getting_name == 'option3':
                logo = cv2.imread('image_detections/Samaa_logo.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Samaa_Ticker/' + os.path.basename(i))
            elif getting_name == 'option4':
                logo = cv2.imread('image_detections/Express.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Express_Ticker/' + os.path.basename(i))
            elif getting_name == 'option5':
                logo = cv2.imread('image_detections/mzl-ftpchoha.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Geo_Ticker/' + os.path.basename(i))
            elif getting_name == 'option6':
                logo = cv2.imread('image_detections/ninety_two.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('NinetyTwo_Ticker/' + os.path.basename(i))

        print('getting_live_collage_list', getting_live_collage_list)

        resized_images = []
     

        # Load the logo image and resize it
       

        # Resize and horizontally stack the logo and each image
        for image_file in all_images_files:
            image = cv2.imread(image_file)
            resized_image = cv2.resize(image, (image_width, image_height))
            stacked = np.hstack((logo, resized_image))
            resized_images.append(stacked)

        # Vertically stack the stacked images
        output_final = np.vstack(resized_images)
        cv2.imwrite('Collage/ticker.png', output_final)
        return JsonResponse({'success': 'success'})
    else:
        return JsonResponse({'error': 'error'})
import numpy as np
import cv2
@csrf_exempt
def getting_offline_collage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        getting_name = data.get('channelNameValue')
        print('i am channel', getting_name)
        getting_live_collage_list = data.get('liveCollageList')
        all_images_files = []
        image_width = 700
        image_height = 100
        for i in getting_live_collage_list:
            if getting_name == 'option1':
                logo = cv2.imread('image_detections/geo.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Dunya_Ticker/' + os.path.basename(i))
            elif getting_name == 'option2':
                logo = cv2.imread('image_detections/ary.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Ary_Ticker/' + os.path.basename(i))
            elif getting_name == 'option3':
                logo = cv2.imread('image_detections/Samaa_logo.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Samaa_Ticker/' + os.path.basename(i))
            elif getting_name == 'option4':
                logo = cv2.imread('image_detections/Express.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Express_Ticker/' + os.path.basename(i))
            elif getting_name == 'option5':
                logo = cv2.imread('image_detections/mzl-ftpchoha.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Geo_Ticker/' + os.path.basename(i))
            elif getting_name == 'option6':
                logo = cv2.imread('image_detections/ninety_two.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('NinetyTwo_Ticker/' + os.path.basename(i))

        print('getting_live_collage_list', getting_live_collage_list)

        resized_images = []
     

        # Load the logo image and resize it
       

        # Resize and horizontally stack the logo and each image
        for image_file in all_images_files:
            image = cv2.imread(image_file)
            resized_image = cv2.resize(image, (image_width, image_height))
            stacked = np.hstack((logo, resized_image))
            resized_images.append(stacked)

        # Vertically stack the stacked images
        output_final = np.vstack(resized_images)
        cv2.imwrite('Collage/ticker.png', output_final)
        return JsonResponse({'success': 'success'})
    else:
        return JsonResponse({'error': 'error'})

# Usage example

import pywhatkit
import keyboard

    # whatsapp.close()
@csrf_exempt
def whatsapp_sender(request):

    if request.method=="POST":

        number=request.POST['numbersent']
        print('number',number)
        print('numbertype',type(number))
       
        # image_path = r "Collage\ticker.jpg"

        # pywhatkit.sendwhats_image(number, image_path)
        # pywhatkit.sendwhats_image("+923119633700", r'Collage\ticker.jpg')
        # pywhatkit.sendwhats_image('+923119633700' , r'Collage\ticker.jpg')
        # number = "+923119633700"  # Recipient's phone number
        # image_path=r"D:\ticker_new\Collage\ticker.jpg"
        pywhatkit.sendwhats_image(number , r'Collage\ticker.png')
        # time.sleep(5)
        time.sleep(3)
        keyboard.press_and_release('ctrl+w')
        # pywhatkit.sendwhatmsg_instantly("+923119633700", "Test msg.", 10, tab_close=True)



        return JsonResponse({'success':'success'})
    else:
        return JsonResponse({'error':'error'})
# from celery import shared_task
# import time
# import pywhatkit
# import keyboard

# @shared_task
# def send_whatsapp_message(number, image_path):
#     pywhatkit.sendwhats_image(number, image_path)
#     time.sleep(3)  # Simulate some processing time
#     keyboard.press_and_release('ctrl+w')
# # from .tasks import send_whatsapp_message
# @csrf_exempt
# def whatsapp_sender(request):
#     if request.method == "POST":
#         number = request.POST['numbersent']
#         image_path = r'Collage\ticker.png'
#         send_whatsapp_message.delay(number, image_path)
#         return JsonResponse({'success': 'success'})
#     else:
#         return JsonResponse({'error': 'error'})
