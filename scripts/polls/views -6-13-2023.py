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
from google_drive_ocr.ocr import Drive_OCR
all_data_comparer=0
import uuid
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
                result= Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search)
            if searching_word and channel_name_search != 'option0' and  not date_search and  not date_search_end and  not time_search and not time_search_end:
                result= Ticker_Extraction_Model.objects.filter(text_ocr__icontains=searching_word,channel_name=channel_name_search)


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
            return render (request,'index.html',{'result':result[:10]})
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
        "https://www.youtube.com/@geonews/live",
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
    # all_tickers_remove=glob.glob('extract/*.jpg')
    # for i in all_tickers_remove:
    #     os.remove(i)

    while success:
        print('count',count)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        # color = (255, 0, 0)
        # thickness = 2
        # image = cv2.rectangle(resized,  (250,526),(295,345), color, thickness)  
        if count % 60 == 0: 
            # cv2.imwrite("frames/%d.jpg" % count, image)     # save frame as JPEG file  
            # image = cv2.imread(f'{resized}')
            face = image[305:344, 1:520]
            # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
            
            characters = generate_unique_filename()

            compare=Character_Comparison.objects.create(characters_comparing=characters)
            if not Character_Comparison.objects.filter(characters_comparing__iexact=characters).exists():    
                
                cv2.imwrite(f"Dunya_Ticker/{characters}.jpg", face)  
                cv2.imwrite(f"extract/{characters}.jpg", face)  

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
            else:
                    # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                   
                    characters = generate_unique_filename()

                    cv2.imwrite(f"Dunya_Ticker/{characters}.jpg", face)  
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
            ob = Drive_OCR(f"Dunya_Ticker/{characters}.jpg")

            text_ticker=ob.main()
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
    all_tickers_files=Ticker_Extraction_Model.objects.filter(date=date,channel_name='Geo').order_by('-id')[:10]
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
        result= Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search,date__range=[date_search, date_search_end],time__range=(time_search,time_search_end))
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
       
        if count % 60 == 0: 
            # cv2.imwrite("frames/%d.jpg" % count, image)     # save frame as JPEG file  
            # image = cv2.imread(f'{resized}')
            face = image[302:359, 0:531]
            # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
           
            characters = generate_unique_filename()

            compare=Character_Comparison.objects.create(characters_comparing=characters)
            if not Character_Comparison.objects.filter(characters_comparing__iexact=characters).exists():    
                
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
            else:
                    # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                  
                    characters = generate_unique_filename()

                    cv2.imwrite(f"Ary_Ticker/{characters}.jpg", face)  
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
            ob = Drive_OCR(f"Ary_Ticker/{characters}.jpg")

            text_ticker=ob.main()
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
    all_tickers_files=Ticker_Extraction_Model.objects.filter(date=date,channel_name='Ary').order_by('-id')[:10]
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
        "https://www.youtube.com/samaatvnews/live",
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
    # all_tickers_remove=glob.glob('extract/*.jpg')
    # for i in all_tickers_remove:
    #     os.remove(i)

    while success:
        print('count',count)
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
       
        if count % 60 == 0: 
            # cv2.imwrite("frames/%d.jpg" % count, image)     # save frame as JPEG file  
            # image = cv2.imread(f'{resized}')
            face = image[305:345, 1:515]
            # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
          
            characters = generate_unique_filename()

            compare=Character_Comparison.objects.create(characters_comparing=characters)
            if not Character_Comparison.objects.filter(characters_comparing__iexact=characters).exists():    
                
                cv2.imwrite(f"Samaa_Ticker/{characters}.jpg", face)  
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
            else:
                    # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                    

                    # Remove any invalid characters from the UUID string
                   
                    characters = generate_unique_filename()

                    cv2.imwrite(f"Samaa_Ticker/{characters}.jpg", face)  
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
            ob = Drive_OCR(f"Samaa_Ticker/{characters}.jpg")

            text_ticker=ob.main()
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
    all_tickers_files=Ticker_Extraction_Model.objects.filter(date=date,channel_name='Samaa').order_by('-id')[:10]
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
       
        if count % 60 == 0: 
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

            compare=Character_Comparison.objects.create(characters_comparing=characters)
            if not Character_Comparison.objects.filter(characters_comparing__iexact=characters).exists():    
                
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
            else:
                    # characters=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                    
                    characters = generate_unique_filename()
                    cv2.imwrite(f"Express_Ticker/{characters}.jpg", face)  
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
            ob = Drive_OCR(f"Express_Ticker/{characters}.jpg")

            text_ticker=ob.main()
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
    all_tickers_files=Ticker_Extraction_Model.objects.filter(date=date,channel_name='Express').order_by('-id')[:10]
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