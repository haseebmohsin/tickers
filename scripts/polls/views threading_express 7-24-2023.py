from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import glob
import os
import json
from django.views.decorators.csrf import csrf_exempt
from google_ocr.ocr import Drive_OCR
all_data_comparer=0
from django.views.decorators.csrf import csrf_exempt
import uuid
import cv2
import pafy
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


def streamer(source,y1,y2,x1,x2,folder_save):
    video = pafy.new(source)
    best = video.getbest(preftype="mp4")

    # Open the video stream
    cap = cv2.VideoCapture(best.url)
    success, frame = cap.read()
    width = 640 # keep original width
    height = 360
    dim = (width, height)
    if success:
        image = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite(f'frames/{folder_save}.jpg',frame)
        ticker=image[y1:y2,x1:x2]
        characters = generate_unique_filename()
        # if folder_save=='Geo_Ticker':
            # cv2.imwrite(f"headline_checker/{'Geo'+characters}.jpg", ticker)  
            # return characters,image
        # if folder_save=='Samaa_Ticker':
            # cv2.imwrite(f"headline_checker/{'Samaa'+characters}.jpg", ticker) 
            # cap.release()
             
            # return characters,image

        # else:

        # Process the frame as needed
        cv2.imwrite(f"{folder_save}/{characters}.jpg", ticker)
    cap.release()      
    return characters
@login_required(login_url=reverse_lazy('login'))
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
            if searching_word and channel_name_search != 'option0' and  date_search and  date_search_end and not time_search and not time_search_end:
                result = Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search,date__range=[date_search, date_search_end],text_ocr__icontains=searching_word).order_by('-id')
            if searching_word and channel_name_search == 'option0' and  date_search and  date_search_end and not time_search and not time_search_end:
                result = Ticker_Extraction_Model.objects.filter(date__range=[date_search, date_search_end],text_ocr__icontains=searching_word).order_by('-id')
            if searching_word and channel_name_search != 'option0' and  date_search and  date_search_end and  time_search and  time_search_end:
                result = Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search,date__range=[date_search, date_search_end],time__range=(time_search,time_search_end),text_ocr__icontains=searching_word,).order_by('-id')


            if searching_word and channel_name_search == 'option0' and  date_search and  date_search_end and  time_search and  time_search_end:
                result = Ticker_Extraction_Model.objects.filter(date__range=[date_search, date_search_end],time__range=(time_search,time_search_end),text_ocr__icontains=searching_word,).order_by('-id')
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
timedata_geo=[]
all_files_with_names_geo=[]
@login_required(login_url=reverse_lazy('login'))
def dunya_ticker(request):
    

    

    # start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    timedata_geo.clear()
    all_files_with_names_geo.clear()
    start_time = time.time()  # Get the current time

    characters=streamer(source="https://www.youtube.com/watch?v=C6Se87yOvrk",y1=297,y2=335,x1=89,x2=550,folder_save='Dunya_Ticker')            

    text_ticker = Drive_OCR(f"Dunya_Ticker/{characters}.jpg")

    text_ticker=text_ticker.main()
    # print('text_ticker',text_ticker)
    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Dunya').order_by('-id')[:20]
   
    if len(text_ticker)>=16:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        ticker_write=True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
            
            if similarity_ratio >= 80:
                # os.remove(f"Dunya_Ticker/{characters}.jpg")
                print('I am similarity')
                ticker_write=False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Dunya",channel_image="mzl-ftpchoha.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

                            


    # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Dunya').order_by('-id')[:10]

    for i in all_objects[:10]:
        # file_name=os.path.basename(i)
        all_files_with_names_geo.append(i.ticker_image)
        timedata_geo.append(i.time)
       
    return JsonResponse({'all_tickers':all_files_with_names_geo,'date':date,'time':formatted_time,'timedata':timedata_geo}) 

@login_required(login_url=reverse_lazy('login'))
def geo_ticker(request):


    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
 

    time_data.clear()
    all_files_with_names.clear()

    global geo_ticker_remove
    geo_ticker_remove=[]
    
    # file_remover(folder_name='headline_checker',extension_name='Geo',appended_file_name=geo_ticker_remove)
   
    # characters,image=streamer(source="https://www.youtube.com/watch?v=O3DPVlynUM0",y1=262,y2=287,x1=162,x2=401,folder_save='Geo_Ticker')            
    characters=streamer(source="https://www.youtube.com/watch?v=O3DPVlynUM0",y1=305,y2=344,x1=1,x2=520,folder_save='Geo_Ticker')            


    # text_ticker = Drive_OCR(f"headline_checker/{'Geo'+characters}.jpg")
    text_ticker = Drive_OCR(f"Geo_Ticker/{characters}.jpg")


    text_ticker=text_ticker.main()
    # print('text_ticker',text_ticker)
    # if 'Headlines' in str(text_ticker) or "ہیڈلائنز" in str(text_ticker):

    #     face = image[286:349, 11:519]
    #     cv2.imwrite(f"Geo_Ticker/{characters}.jpg", face)  
    #     print('TRUEEEEEEEEEEEEEEEE')
    # else:
    #     face = image[305:344, 1:520]
    #     cv2.imwrite(f"Geo_Ticker/{characters}.jpg", face)  
    #     print('FALSEEEEEEEEEEEEEEEE')


    # print('text_ticker',text_ticker)
    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Geo').order_by('-id')[:20]
     
    if len(text_ticker)>=16:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        ticker_write=True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
            
            if similarity_ratio >= 80:
                # os.remove(f"Dunya_Ticker/{characters}.jpg")
                # print('I am similarity')
                ticker_write=False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            # print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Geo",channel_image="geo.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)
            
                    


                
    # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Geo').order_by('-id')[:10]

    for i in all_objects[:10]:
        # file_name=os.path.basename(i)
        all_files_with_names.append(i.ticker_image)
        time_data.append(i.time)
            # print('all_ocr_result',all_ocr_result)
            
            


    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers':all_files_with_names,'date':date,'time':formatted_time,'timedata':time_data}) 
    
        
            
   
result_all=[]


@login_required(login_url=reverse_lazy('login'))  

def convert_time_format(time_str):
    # Parse the time string into a datetime object
    time_obj = datetime.datetime.strptime(time_str, "%H:%M")
    
    # Convert the time to 12-hour format with AM/PM indicator
    formatted_time = time_obj.strftime("%I:%M %p")
    
    return formatted_time



from django.core.paginator import Paginator
from django.shortcuts import render
@login_required(login_url=reverse_lazy('login'))
def table_view(request):
    global all_data_comparer
    
    data = data_result[10:]
    lenght_of_data=len(data_result)
    if all_data_comparer<=lenght_of_data:
        paginator = Paginator(data, 10)  # Display 10 entries per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        all_data_comparer+=10
    
        return render(request, 'index.html', {'result': page_obj,'clear':'True'})

    elif all_data_comparer>lenght_of_data:
      paginator = Paginator(data, 0)
      page_number = request.GET.get('page')
      page_obj = paginator.get_page(page_number)
      all_data_comparer=0
 
      return render(request, 'index.html',)
timedata_ary=[]
all_files_with_names_ary=[]
@login_required(login_url=reverse_lazy('login'))
def ary_ticker(request):
    

    

    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    timedata_ary.clear()
    all_files_with_names_ary.clear()
 

    characters=streamer(source="https://www.youtube.com/watch?v=sUKwTVAc0Vo",y1=302,y2=359,x1= 0,x2=531,folder_save='Ary_Ticker')            
    text_ticker = Drive_OCR(f"Ary_Ticker/{characters}.jpg")

    text_ticker=text_ticker.main()
    print('text_ticker',text_ticker)
    all_objects = Ticker_Extraction_Model.objects.filter(channel_name="Ary").order_by('-id')[:20]
     
    if len(text_ticker)>=16:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        ticker_write=True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
            
            if similarity_ratio >= 80:
                # os.remove(f"Dunya_Ticker/{characters}.jpg")
                print('I am similarity')
                ticker_write=False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Ary",channel_image="ary.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

                    


    # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Ary').order_by('-id')[:10]

    for i in all_objects[:10]:
        # file_name=os.path.basename(i)
        all_files_with_names_ary.append(i.ticker_image)
        timedata_ary.append(i.time)
       

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers':all_files_with_names_ary,'date':date,'time':formatted_time,'timedata':timedata_ary}) 
    




timedata_samaa=[]
all_files_with_names_samaa=[]
@login_required(login_url=reverse_lazy('login'))
def samaa_ticker(request):
    

    

    start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    timedata_samaa.clear()
    all_files_with_names_samaa.clear()
    global samaa_ticker_remove
    samaa_ticker_remove=[]
 
    # file_remover(folder_name='headline_checker',extension_name='Sam',appended_file_name=samaa_ticker_remove)
  
    # characters,image=streamer(source="https://www.youtube.com/watch?v=yHi3yIkPcLE",y1=257,y2=341,x1= 2,x2=514,folder_save='Samaa_Ticker')            
    characters=streamer(source="https://www.youtube.com/watch?v=yHi3yIkPcLE",y1=304,y2=345,x1= 1,x2=515,folder_save='Samaa_Ticker')            

    # text_ticker = Drive_OCR(f"headline_checker/{'Samaa'+characters}.jpg")
    text_ticker = Drive_OCR(f"Samaa_Ticker/{characters}.jpg")

    text_ticker=text_ticker.main()
    # if 'Headlines' in str(text_ticker) or "ہیڈلائنز" in str(text_ticker):
        # face=image[281:335,2:514]
        # cv2.imwrite(f'Samaa_Ticker/{characters}.jpg',face)
    # else:
        # face = image[305:345, 1:515]
        # cv2.imwrite(f'Samaa_Ticker/{characters}.jpg',face)



    # print('text_ticker',text_ticker)
    all_objects = Ticker_Extraction_Model.objects.filter(channel_name="Samaa").order_by('-id')[:20]
   
    if len(text_ticker)>=16:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        ticker_write=True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
            
            if similarity_ratio >= 80:
                # os.remove(f"Dunya_Ticker/{characters}.jpg")
                print('I am similarity')
                ticker_write=False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Samaa",channel_image="Samaa_logo.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

                    


              
    # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Samaa').order_by('-id')[:10]

    for i in all_objects[:10]:
        # file_name=os.path.basename(i)
        all_files_with_names_samaa.append(i.ticker_image)
        timedata_samaa.append(i.time)
            # print('all_ocr_result',all_ocr_result)
            
            
            
            
         

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers':all_files_with_names_samaa,'date':date,'time':formatted_time,'timedata':timedata_samaa}) 


timedata_express=[]
all_files_with_names_express=[]

timedata_express=[]
all_files_with_names_express=[]
import threading
def ticker_express_frame_saver(request):
    start_time = time.time()  # Get the current time

    global all_tickers_files_express
    all_tickers_files_express=Ticker_Extraction_Model.objects.filter(channel_name='Express').order_by('-id')[:10]

    # FrameSaver.objects.all().delete()
    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    timedata_express.clear()
    all_files_with_names_express.clear()
 
    characters=streamer(source="https://www.youtube.com/watch?v=muBr6a3Xi2c",y1=310,y2=358,x1=0,x2=495,folder_save='Express_Ticker') 
    frame_saving_object=Ticker_Extraction_Model.objects.create(channel_name="Express",channel_image="express.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,)

    # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Express').order_by('-id')[:10]
    # Saving_Foreign_Object=FrameSaver.objects.create(Ticker_Model=frame_saving_object,character_foreign=characters)
    # global all_tickers_files_express

    for i in all_tickers_files_express:
        # file_name=os.path.basename(i)
        all_files_with_names_express.append(i.ticker_image)
        timedata_express.append(i.time)
    end_time=time.time()
    print(f'FIRST FUNCTION EXECUTED IN {end_time - start_time}s ')
     
    # end_time = time.time()  # Get the current time after the task is completed
    # execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers':all_files_with_names_express,'date':date,'time':formatted_time,'timedata':timedata_express}) 
count_save=0
@login_required(login_url=reverse_lazy('login'))
def express_ticker(request):
        global  count_save
        count_save+=1
        
        start_time = time.time()  # Get the current time
        if count_save%2!=0:
        # getting_ticker=Ticker_Extraction_Model.objects.filter(channel_name='Express').order_by('-id')[:2]
            getting_ticker=all_tickers_files_express[:2]
            print('getting_ticker[0]',getting_ticker[0].ticker_image)
            print('getting_ticker[1]',getting_ticker[1].ticker_image)

            getting_first_ticker = getting_ticker[:1]
            print('getting_first_ticker[0]',getting_first_ticker)
            getting_second_ticker=getting_ticker[1:2]
        
            def running_parallel_express(characters,object,):
                text_ticker = Drive_OCR(f"Express_Ticker/{characters}")

                text_ticker=text_ticker.main()

                if len(text_ticker)>16:
                    # print('getting',getting_two_created_tickers[0].date)
                    
        
                # print("I am text",text_ticker)
                # if Getting_Foreign_Object.exists():
                #             object_to_be_deleted=Getting_Foreign_Object[0]
                #             object_to_be_deleted.Ticker_Model.text_ocr=text_ticker
                #             object_to_be_deleted.delete()
                    if object=='first':
                        for i in getting_first_ticker:
                            i.text_ocr=text_ticker
                            i.save()
                            print('I am text0',text_ticker)

                        #  print('I am in 0')
                        #  getting_two_created_tickers[0].text_ocr=text_ticker
                        #  getting_two_created_tickers[0].save()
                    if object=='second':
                        for i in getting_second_ticker:
                            i.text_ocr=text_ticker
                            i.save()
                            print('I am text1',text_ticker)
                   
                        #  getting_two_created_tickers[1].text_ocr=text_ticker
                        #  print("I am in 1")
                        #  getting_two_created_tickers[1].save()
                    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Express',text_ocr=text_ticker)
                    if len(all_objects)>1 and len(all_objects)!=-1:
                        for obj in all_objects:
                                similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
                                
                                if similarity_ratio >= 70:
                                        obj.delete()
                        # for i in range(len(all_objects)-1):
                    #         i.delete()
            p3=threading.Thread(target=running_parallel_express,args=(getting_first_ticker[0].ticker_image,'first'))
            p4=threading.Thread(target=running_parallel_express,args=(getting_second_ticker[0].ticker_image,'second'))
            # p3=threading.Thread(target=running_parallel_express,args=(getting_third_ticker[0].ticker_image,'three'))
            # p4=threading.Thread(target=running_parallel_express,args=(getting_fourth_ticker[0].ticker_image,'four'))
            p3.start()
            p4.start()
            # p3.start()
            # p4.start()
            p3.join()
            p4.join()
            # p3.join()
            # p4.join()
            endtime=time.time()

            print(f'Process executed in: {endtime-start_time}')
            print("DONEEEEEEEEEEEEEEEEEEEEE")
            return JsonResponse({'success':'sucess'})

       
        elif count_save%2==0:
            getting_ticker_next=all_tickers_files_express[:2]
          

            getting_first_ticker_next = getting_ticker_next[:1]
            # print('getting_first_ticker[0]',getting_first_ticker)
            getting_second_ticker_next=getting_ticker_next[1:2]
            # print('getting_second_ticker[1]',getting_second_ticker)
            def running_parallel_express(characters,object,):
                text_ticker = Drive_OCR(f"Express_Ticker/{characters}")

                text_ticker=text_ticker.main()

                if len(text_ticker)>16:
                    # print('getting',getting_two_created_tickers[0].date)
                    
        
                # print("I am text",text_ticker)
                # if Getting_Foreign_Object.exists():
                #             object_to_be_deleted=Getting_Foreign_Object[0]
                #             object_to_be_deleted.Ticker_Model.text_ocr=text_ticker
                #             object_to_be_deleted.delete()
                    if object=='first':
                        for i in getting_first_ticker_next:
                            i.text_ocr=text_ticker
                            i.save()
                            print('I am text0',text_ticker)

                        #  print('I am in 0')
                        #  getting_two_created_tickers[0].text_ocr=text_ticker
                        #  getting_two_created_tickers[0].save()
                    if object=='second':
                        for i in getting_second_ticker_next:
                            i.text_ocr=text_ticker
                            i.save()
                            print('I am text1',text_ticker)
                
                        #  getting_two_created_tickers[1].text_ocr=text_ticker
                        #  print("I am in 1")
                        #  getting_two_created_tickers[1].save()
                    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Express',text_ocr=text_ticker)
                    if len(all_objects)>1 and len(all_objects)!=-1:
                        for obj in all_objects:
                                similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
                                
                                if similarity_ratio >= 70:
                                        obj.delete()
                        # for i in range(len(all_objects)-1):
                    #         i.delete()
            p1=threading.Thread(target=running_parallel_express,args=(getting_first_ticker_next[0].ticker_image,'first'))
            p2=threading.Thread(target=running_parallel_express,args=(getting_second_ticker_next[0].ticker_image,'second'))
            # p3=threading.Thread(target=running_parallel_express,args=(getting_third_ticker[0].ticker_image,'three'))
            # p4=threading.Thread(target=running_parallel_express,args=(getting_fourth_ticker[0].ticker_image,'four'))
            p1.start()
            p2.start()
            # p3.start()
            # p4.start()
            p1.join()
            p2.join()
            # p3.join()
            # p4.join()
            endtime=time.time()

            print(f'Process executed in: {endtime-start_time}')
            print("DONEEEEEEEEEEEEEEEEEEEEE")
            return JsonResponse({'success':'sucess'})
          




        # getting_two_created_tickers=Ticker_Extraction_Model.objects.filter(channel_name='Express').order_by('-id')[:2]
        # for i in getting_two_created_tickers:
        #     i.text_ocr='changed'
        #     i.save()
        # getting_two_created_tickers[0].text_ocr='changedone'
        # getting_two_created_tickers[1].text_ocr='changedtwo'
        # getting_two_created_tickers[0].save()
        # getting_two_created_tickers[1].save()
        # print('Getting_Foreign_Object',getting_two_created_tickers[0].text_ocr)
        # first_object=getting_two_created_tickers[0]
        # second_object=getting_two_created_tickers[1]
        # first_object_path=getting_two_created_tickers[0].ticker_image
        # print('first_object_path',first_object_path)
        # second_object_path=getting_two_created_tickers[1].ticker_image
        # print('second_object_path',second_object_path)
    # Access the text_ocr field of the first related Ticker_Extraction_Model
        # if Getting_Foreign_Object.exists():
        #     characters = Getting_Foreign_Object[0].Ticker_Model.ticker_image
        
# @login_required(login_url=reverse_lazy('login'))
# def express_ticker(request):
    

    

#     # start_time = time.time()  # Get the current time

#     date=datetime.datetime.now().date()
#     timeticker=datetime.datetime.now().time()
#     formatted_time = timeticker.strftime("%I:%M %p")
   
#     timedata_express.clear()
#     all_files_with_names_express.clear()
 
#     characters=streamer(source="https://www.youtube.com/watch?v=muBr6a3Xi2c",y1=310,y2=358,x1=0,x2=495,folder_save='Express_Ticker')            

#     text_ticker = Drive_OCR(f"Express_Ticker/{characters}.jpg")

#     text_ticker=text_ticker.main()
#     all_objects = Ticker_Extraction_Model.objects.filter(channel_name='Express').order_by('-id')[:20]

#     # print('text_ticker',text_ticker)
#     if len(text_ticker)>=16:
#         # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
#         ticker_write=True
#         # Compare text similarity with each object
#         for obj in all_objects:
#             similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)
            
#             if similarity_ratio >= 70:
#                 # os.remove(f"Dunya_Ticker/{characters}.jpg")
#                 # print('I am similarity')
#                 ticker_write=False
#                 break
#                 # matching_objects.append(obj)
#                 # ticker_write=True
#         if ticker_write:
#             # print('I am writing in database')
#             Ticker_Extraction_Model.objects.create(channel_name="Express",channel_image="express.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

                    


         
#     # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Express').order_by('-id')[:10]

#     for i in all_objects[:10]:
#         # file_name=os.path.basename(i)
#         all_files_with_names_express.append(i.ticker_image)
#         timedata_express.append(i.time)
     
#     # end_time = time.time()  # Get the current time after the task is completed
#     # execution_time = end_time - start_time  # Calculate the execution time

#     # print(f"Function executed in {execution_time:.2f} seconds")
#     return JsonResponse({'all_tickers':all_files_with_names_express,'date':date,'time':formatted_time,'timedata':timedata_express}) 

# inside geo the dunya is running and inside dunya the geo is running

timedata_ninety_two=[]
all_files_with_names_ninety_two=[]
@login_required(login_url=reverse_lazy('login'))
def ninety_two_ticker(request):
    

    

    # start_time = time.time()  # Get the current time

    date=datetime.datetime.now().date()
    timeticker=datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")
   
    timedata_ninety_two.clear()
    all_files_with_names_ninety_two.clear()
    start_time = time.time()  # Get the current time


                
    characters=streamer(source="https://www.youtube.com/watch?v=tF6CGSjU0uI",y1=297,y2=335,x1=89,x2=550,folder_save='NinetyTwo_Ticker')            

    text_ticker = Drive_OCR(f"NinetyTwo_Ticker/{characters}.jpg")

    text_ticker=text_ticker.main()
    # print('text_ticker',text_ticker)
    all_objects = Ticker_Extraction_Model.objects.filter(channel_name='NinetyTwo').order_by('-id')[:20]
    if len(text_ticker)>=16:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        
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
            Ticker_Extraction_Model.objects.create(channel_name="NinetyTwo",channel_image="ninety_two.png",ticker_image=f"{characters}.jpg",date=date,time=formatted_time,text_ocr=text_ticker)

                            


    # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='NinetyTwo').order_by('-id')[:10]

    for i in all_objects[:10]:
        # file_name=os.path.basename(i)
        all_files_with_names_ninety_two.append(i.ticker_image)
        timedata_ninety_two.append(i.time)
            # print('all_ocr_result',all_ocr_result)
            
            
            

    return JsonResponse({'all_tickers':all_files_with_names_ninety_two,'date':date,'time':formatted_time,'timedata':timedata_ninety_two}) 


import numpy as np
import cv2
import base64
# from PIL import Image
# @csrf_exempt
# def getting_live_collage(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         getting_name = data.get('channelNameValue')
#         print('i am channel', getting_name)
#         getting_live_collage_list = data.get('liveCollageList')
#         image=data.get('image')
#         image_data = base64.b64decode(image.split(',')[1])
#         save_path = 'date.jpg' 
#         with open(save_path, 'wb') as f:
#            f.write(image_data)
#     #     image = Image.open(save_path)
#     #     if image.mode == 'RGBA':
#     #         image = image.convert('RGB')

#     # # Resize the image to the desired dimensions
#     #     new_size = (1024, 1024)  # Replace with your desired dimensions
#     #     resized_image = image.resize(new_size)

#     #     # Save the resized image back to the same path
#     #     resized_image.save(save_path)

#         all_images_files = []
#         image_width = 700
#         image_height = 100
#         for i in getting_live_collage_list:
#             if getting_name == 'option1':
#                 logo = cv2.imread('image_detections/geo.png')
#                 # logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('Dunya_Ticker/' + os.path.basename(i))
#             elif getting_name == 'option2':
#                 logo = cv2.imread('image_detections/ary.png')
#                 # logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('Ary_Ticker/' + os.path.basename(i))
#             elif getting_name == 'option3':
#                 logo = cv2.imread('image_detections/Samaa_logo.png')
#                 # logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('Samaa_Ticker/' + os.path.basename(i))
#             elif getting_name == 'option4':
#                 logo = cv2.imread('image_detections/Express.png')
#                 # logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('Express_Ticker/' + os.path.basename(i))
#             elif getting_name == 'option5':
#                 logo = cv2.imread('image_detections/mzl-ftpchoha.png')
#                 # logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('Geo_Ticker/' + os.path.basename(i))
#             elif getting_name == 'option6':
#                 logo = cv2.imread('image_detections/ninety_two.png')
#                 # logo = cv2.resize(logo, (100, image_height))
#                 all_images_files.append('NinetyTwo_Ticker/' + os.path.basename(i))

#         print('getting_live_collage_list', getting_live_collage_list)

#         resized_images = []
#         date_image=cv2.imread('date.jpg')
#         logo = cv2.resize(logo, (100, 100)) 
#         date_image_resized = cv2.resize(date_image, (100, 100))

#         # Load the logo image and resize it
#         stacked_vertical = np.vstack((logo, date_image_resized))

#         stacked_vertical_resized = cv2.resize(stacked_vertical, (100, 100))

#         # Resize and horizontally stack the logo and each image
#         for image_file in all_images_files:
#             image = cv2.imread(image_file)
#             resized_image = cv2.resize(image, (image_width, image_height))
#             # stacked=np.vstack(())
#             stacked = np.hstack((stacked_vertical_resized, resized_image))
#             resized_images.append(stacked)

#         # Vertically stack the stacked images
#         output_final = np.vstack(resized_images)
#         cv2.imwrite('Collage/ticker.png', output_final)
#         return JsonResponse({'success': 'success'})
#     else:
#         return JsonResponse({'error': 'error'})
import io
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter
date_images=[]
time_images=[]
def make_image(date_live, saver_name, list_saver):
    image_size = (200, 100)  # Desired image size
    background_color = (255, 255, 255)  # RGB color for the background
    text_color = (0, 0, 0)  # RGB color for the text
    font_size = 35
    font_path = r"D:\ticker_new\Times New Roman\times new roman bold.ttf"  # Replace with the path to your desired font file

    if list_saver == 'date':
        date_images.clear()
    elif list_saver == 'time':
        time_images.clear()

    for i in range(len(date_live)):
        # Create a new image with the specified background color
        image = Image.new('RGB', image_size, background_color)

        # Create a draw object
        draw = ImageDraw.Draw(image)

        # Define the font and load it with the specified size
        font = ImageFont.truetype(font_path, font_size)

        # Calculate the position to center the text
        text_width, text_height = draw.textsize(date_live[i], font=font)
        position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)

        # Draw the text on the image
        draw.text(position, date_live[i], font=font, fill=text_color)

        # Apply contrast enhancement to the image
        enhancer = ImageEnhance.Contrast(image)
        enhanced_image = enhancer.enhance(1.5)  # Adjust the contrast factor as desired

        # Apply brightness enhancement to the image
        enhancer = ImageEnhance.Brightness(enhanced_image)
        brightened_image = enhancer.enhance(1.2)  # Adjust the brightness factor as desired

        # Apply sharpening filter to the image
        sharpened_image = brightened_image.filter(ImageFilter.SHARPEN)

        border_color = (0, 0, 255)  # RGB color for the border
        border_size = 5
        border_box = [(0, 0), (image_size[0] - 1, image_size[1] - 1)]
        draw = ImageDraw.Draw(sharpened_image)
        # draw.rectangle(border_box, outline=border_color, width=border_size)

        if list_saver == 'date':
            date_images.append(np.array(sharpened_image))
        elif list_saver == 'time':
            time_images.append(np.array(sharpened_image))
            # Save the image with a unique filename (e.g., based on the date)
            # image_filename = f'{saver_name}_{i}.png'
            
            # image.save(image_filename)
            
            # Optionally, you can perform further operations with the image here
            
            # Print the filename for verification
            # print(f'Saved image: {image_filename}')
@csrf_exempt

def getting_live_collage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        getting_name = data.get('channelNameValue')
        print('i am channel', getting_name)
        getting_live_collage_list = data.get('liveCollageList')
        all_images_files = []
        all_images_files.clear()

        time_live=data.get('timeLive')
        date_live=data.get('dateLive')
        print('time_live',time_live)
        print('date_live',date_live)
        # Size of the font
        date_list_maker=make_image(date_live=date_live,saver_name='date',list_saver='date')
        time_list_maker=make_image(date_live=time_live,saver_name='time',list_saver='time')
        print('date_images',date_images)
        print('time_images',time_images)



      
        # image_width = 700
        # image_height = 100
        for i in getting_live_collage_list:
            if getting_name == 'option1':
                logo = cv2.imread('image_detections/geo.png')
                # logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Geo_Ticker/' + os.path.basename(i))
            elif getting_name == 'option2':
                logo = cv2.imread('image_detections/ary.png')
                # logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Ary_Ticker/' + os.path.basename(i))
            elif getting_name == 'option3':
                logo = cv2.imread('image_detections/Samaa_logo.png')
                # logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Samaa_Ticker/' + os.path.basename(i))
            elif getting_name == 'option4':
                logo = cv2.imread('image_detections/Express.png')
                # logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Express_Ticker/' + os.path.basename(i))
            elif getting_name == 'option5':
                logo = cv2.imread('image_detections/mzl-ftpchoha.png')
                # logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Dunya_Ticker/' + os.path.basename(i))
            elif getting_name == 'option6':
                logo = cv2.imread('image_detections/ninety_two.png')
                # logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('NinetyTwo_Ticker/' + os.path.basename(i))

        # print('getting_live_collage_list', getting_live_collage_list)

        resized_images = []
        # date_image=cv2.imread('date.jpg')
        # logo = cv2.resize(logo, (100, 100)) 
        # date_image_resized = cv2.resize(date_image, (100, 100))

        # # Load the logo image and resize it
        # stacked_vertical = np.vstack((logo, date_image_resized))

        # stacked_vertical_resized = cv2.resize(stacked_vertical, (100, 100))
        stacked_vertical_images=[]
        for i in range(len(date_images)):
                # date_image_stack=cv2.imread(date_images[i])
                date_image_resized = cv2.resize(date_images[i], (200,90))

                # time_image_stack=cv2.imread(time_images[i])
                time_image_resized = cv2.resize(time_images[i], (200,90))

                logo = cv2.resize(logo, (200,150)) 
                stacked_vertical = np.vstack((logo, date_image_resized,time_image_resized))
                # cv2.imwrite('stacked.jpg',stacked_vertical)

                stacked_vertical_images.append(stacked_vertical)



        print('len_date_images',len(date_images))
        print('len_time_images',len(time_images))
        print('len_all_images_files',len(all_images_files))
        # Resize and horizontally stack the logo and each image
        for i in range(len(all_images_files)):
            image = cv2.imread(all_images_files[i])
            resized_image = cv2.resize(image, (730, 110))
            resized_stacked_image=cv2.resize(stacked_vertical_images[i],(80,110))
            # stacked=np.vstack(())
            stacked = np.hstack(( resized_image,resized_stacked_image))
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
        all_images_files.clear()
        
        time_offline=data.get('timeOffline')
        date_offline=data.get('dateOffline')
        print('time_offline',time_offline)
        print('date_offline',date_offline)
        # Size of the font
        date_list_maker=make_image(date_live=date_offline,saver_name='date',list_saver='date')
        time_list_maker=make_image(date_live=time_offline,saver_name='time',list_saver='time')

        image_width = 700
        image_height = 100
        for i in getting_live_collage_list:
            if getting_name == 'option1':
                logo = cv2.imread('image_detections/geo.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Geo_Ticker/' + os.path.basename(i))
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
                all_images_files.append('Dunya_Ticker/' + os.path.basename(i))
            elif getting_name == 'option6':
                logo = cv2.imread('image_detections/ninety_two.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('NinetyTwo_Ticker/' + os.path.basename(i))

        resized_images = []
        # date_image=cv2.imread('date.jpg')
        # logo = cv2.resize(logo, (100, 100)) 
        # date_image_resized = cv2.resize(date_image, (100, 100))

        # # Load the logo image and resize it
        # stacked_vertical = np.vstack((logo, date_image_resized))

        # stacked_vertical_resized = cv2.resize(stacked_vertical, (100, 100))
        stacked_vertical_images=[]
        for i in range(len(date_images)):
                # date_image_stack=cv2.imread(date_images[i])
                date_image_resized = cv2.resize(date_images[i], (200,90))

                # time_image_stack=cv2.imread(time_images[i])
                time_image_resized = cv2.resize(time_images[i], (200,90))

                logo = cv2.resize(logo, (200,150)) 
                stacked_vertical = np.vstack((logo, date_image_resized,time_image_resized))
                # cv2.imwrite('stacked.jpg',stacked_vertical)

                stacked_vertical_images.append(stacked_vertical)



        print('len_date_images',len(date_images))
        print('len_time_images',len(time_images))
        print('len_all_images_files',len(all_images_files))
        # Resize and horizontally stack the logo and each image
        for i in range(len(all_images_files)):
            image = cv2.imread(all_images_files[i])
            resized_image = cv2.resize(image, (730, 110))
            resized_stacked_image=cv2.resize(stacked_vertical_images[i],(80,110))
            # stacked=np.vstack(())
            stacked = np.hstack(( resized_image,resized_stacked_image))
            resized_images.append(stacked)

        # Vertically stack the stacked images
        output_final = np.vstack(resized_images)
        cv2.imwrite('Collage/ticker.png', output_final)
        return JsonResponse({'success': 'success'})
    else:
        return JsonResponse({'error': 'error'})
# Usage example

# import pywhatkit
# import keyboard

#     # whatsapp.close()
# @csrf_exempt
# def whatsapp_sender(request):

#     if request.method=="POST":

#         number=request.POST['numbersent']
#         print('number',number)
#         print('numbertype',type(number))
       
      
#         pywhatkit.sendwhats_image(number , r'Collage\ticker.png')
#         # time.sleep(5)
#         time.sleep(3)
#         keyboard.press_and_release('ctrl+w')
#         # pywhatkit.sendwhatmsg_instantly("+923119633700", "Test msg.", 10, tab_close=True)



#         return JsonResponse({'success':'success'})
#     else:
#         return JsonResponse({'error':'error'})





# Dictionary to store notifications


# views.py

# views.py

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print('user',user)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid username or password.'
    else:
        error_message = ''

    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if get_user_model().objects.filter(is_superuser=True).exists():
                # Additional users should not have superuser privileges
                user.is_superuser = False
            user.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
