from django.http import HttpResponse
from .models import Ticker_Extraction_Model, words_to_be_searched_model
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter
import io
import base64
import numpy as np
from django.core.paginator import Paginator
from rapidfuzz import fuzz
import shutil
import datetime
import string
import random
import subprocess
import time
from .forms import word_to_be_searched_form
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
import pafy
import cv2
import uuid
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import glob
import os
import json
from django.views.decorators.csrf import csrf_exempt
from google_ocr.ocr import Drive_OCR
all_data_comparer = 0


def streamer(source, y1, y2, x1, x2, folder_save):
    video = pafy.new(source)
    best = video.getbest(preftype="mp4")

    # Open the video stream
    cap = cv2.VideoCapture(best.url)
    success, frame = cap.read()
    width = 640  # keep original width
    height = 360
    dim = (width, height)
    if success:
        image = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        # cv2.imwrite(f'frames/{folder_save}.jpg',image)
        ticker = image[y1:y2, x1:x2]
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
        cv2.imwrite(
            f"D:/Haseeb/ticker/public/{folder_save}/{characters}.jpg", ticker)
    cap.release()
    return characters


def index2(request):
    if request.method == "POST":
        global all_data_comparer
        all_data_comparer = 0
        searching_word = request.POST['wordsearched']

        channel_name_search = request.POST['channel_name']
        if channel_name_search == 'option1':
            channel_name_search = 'Geo'
        if channel_name_search == 'option2':
            channel_name_search = 'Ary'
        if channel_name_search == 'option3':
            channel_name_search = 'Samaa'
        if channel_name_search == 'option4':
            channel_name_search = 'Express'
        if channel_name_search == 'option5':
            channel_name_search = 'Dunya'
        if channel_name_search == 'option6':
            channel_name_search = 'HumNews'

        print('channel_name', channel_name_search)
        date_search = request.POST['gettingdate']
        date_search_end = request.POST['gettingdateend']
        time_search = request.POST['gettingtime']
        if time_search:
            time_search = convert_time_format(time_search)

        time_search_end = request.POST['gettingtimeend']
        if time_search_end:
            time_search_end = convert_time_format(time_search_end)
        print('date_search', date_search)
        print('time', time_search)
        if channel_name_search == 'option0' and date_search and not searching_word and date_search_end and not time_search and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                date__range=[date_search, date_search_end]).order_by('-id')
        if channel_name_search == 'option0' and not date_search and not searching_word and not date_search_end and time_search and time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                time__range=(time_search, time_search_end)).order_by('-id')

        if channel_name_search == 'option0' and date_search and not searching_word and not date_search_end and not time_search and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                date=date_search).order_by('-id')
        if channel_name_search == 'option0' and not date_search and not searching_word and date_search_end and not time_search and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                date=date_search_end).order_by('-id')
        if channel_name_search == 'option0' and not date_search and not searching_word and not date_search_end and time_search and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                time=time_search).order_by('-id')
        if channel_name_search == 'option0' and not date_search and not searching_word and not date_search_end and not time_search and time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                time=time_search_end).order_by('-id')
        if not searching_word and channel_name_search == 'option0' and date_search and date_search_end and time_search and time_search_end:
            result = Ticker_Extraction_Model.objects.filter(date__range=[
                                                            date_search, date_search_end], time__range=(time_search, time_search_end)).order_by('-id')

        if not searching_word and channel_name_search != 'option0' and date_search and date_search_end and time_search and time_search_end:
            result = Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search, date__range=[
                                                            date_search, date_search_end], time__range=(time_search, time_search_end)).order_by('-id')
        if not searching_word and channel_name_search != 'option0' and date_search and date_search_end and not time_search and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search, date__range=[
                                                            date_search, date_search_end]).order_by('-id')
        if not searching_word and channel_name_search != 'option0' and not date_search and not date_search_end and time_search and time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                channel_name=channel_name_search, time__range=(time_search, time_search_end)).order_by('-id')
        if searching_word and channel_name_search != 'option0' and date_search and date_search_end and not time_search and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search, date__range=[
                                                            date_search, date_search_end], text_ocr__icontains=searching_word).order_by('-id')
        if searching_word and channel_name_search == 'option0' and date_search and date_search_end and not time_search and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(date__range=[
                                                            date_search, date_search_end], text_ocr__icontains=searching_word).order_by('-id')
        if searching_word and channel_name_search != 'option0' and date_search and date_search_end and time_search and time_search_end:
            result = Ticker_Extraction_Model.objects.filter(channel_name=channel_name_search, date__range=[
                                                            date_search, date_search_end], time__range=(time_search, time_search_end), text_ocr__icontains=searching_word,).order_by('-id')

        if searching_word and channel_name_search == 'option0' and date_search and date_search_end and time_search and time_search_end:
            result = Ticker_Extraction_Model.objects.filter(date__range=[date_search, date_search_end], time__range=(
                time_search, time_search_end), text_ocr__icontains=searching_word,).order_by('-id')
        if not searching_word and channel_name_search != 'option0' and date_search and not time_search and not date_search_end and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                channel_name=channel_name_search, date=date_search).order_by('-id')
            print('result', result)
        if not searching_word and channel_name_search != 'option0' and time_search and not date_search and not date_search_end and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                channel_name=channel_name_search, time=time_search).order_by('-id')

        if not searching_word and channel_name_search != 'option0' and time_search and date_search and not date_search_end and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                channel_name=channel_name_search, time=time_search, date=date_search).order_by('-id')
        if not searching_word and channel_name_search == 'option0' and not date_search and not time_search and not date_search_end and not time_search_end:
            # return render(request,'index.html')
            result = Ticker_Extraction_Model.objects.all().order_by('-id')
        if not searching_word and channel_name_search != 'option0' and not searching_word and not date_search and not date_search_end and not time_search and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                channel_name=channel_name_search).order_by('-id')
        if searching_word and channel_name_search != 'option0' and not date_search and not date_search_end and not time_search and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                text_ocr__icontains=searching_word, channel_name=channel_name_search).order_by('-id')

        if searching_word and channel_name_search != 'option0' and date_search and date_search_end and time_search and time_search_end:
            result = Ticker_Extraction_Model.objects.filter(text_ocr__icontains=searching_word, channel_name=channel_name_search, date__range=[
                                                            date_search, date_search_end], time__range=(time_search, time_search_end)).order_by('-id')
        if searching_word and channel_name_search != 'option0' and date_search and date_search_end and not time_search and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(text_ocr__icontains=searching_word, channel_name=channel_name_search, date__range=[
                                                            date_search, date_search_end]).order_by('-id')
        if searching_word and channel_name_search != 'option0' and not date_search and not date_search_end and time_search and time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                text_ocr__icontains=searching_word, channel_name=channel_name_search, time__range=(time_search, time_search_end)).order_by('-id')

        if searching_word and channel_name_search != 'option0' and date_search and not time_search and not date_search_end and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                text_ocr__icontains=searching_word, channel_name=channel_name_search, date=date_search).order_by('-id')
            print('result', result)
        if searching_word and channel_name_search != 'option0' and time_search and not date_search and not date_search_end and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                text_ocr__icontains=searching_word, channel_name=channel_name_search, time=time_search).order_by('-id')

        if searching_word and channel_name_search != 'option0' and time_search and date_search and not date_search_end and not time_search_end:
            result = Ticker_Extraction_Model.objects.filter(
                text_ocr__icontains=searching_word, channel_name=channel_name_search, time=time_search, date=date_search).order_by('-id')

        if channel_name_search == 'option0' and searching_word and not date_search and not time_search and not date_search_end and not time_search_end:
            # else :
            result = Ticker_Extraction_Model.objects.filter(
                text_ocr__icontains=searching_word).order_by('-id')

        if channel_name_search == 'option0' and not searching_word and not date_search and not time_search and not date_search_end and not time_search_end:
            # return render(request,'index.html')
            result = Ticker_Extraction_Model.objects.all().order_by('-id')

            # paginator = Paginator(result, 10)  # Show 10 items per page

        global data_result
        data_result = result
        return render(request, 'index.html', {'result': result[:10], 'channel_name': channel_name_search, })
    else:

        return render(request, 'index.html', {'data': 'data', })


# @login_required(login_url=reverse_lazy('login'))
@csrf_exempt
def index(request):
    if request.method == 'POST':
        wordnotification = request.POST['wordname']
        checking = words_to_be_searched_model.objects.filter(
            word=wordnotification).exists()
        if checking:
            pass
        else:
            words_to_be_searched_model.objects.create(
                word=wordnotification, user=request.user)

        print('word_notification', wordnotification)
        # form=word_to_be_searched_form(request.POST)
        # if form.is_valid():
        #     form.save()

        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        return render(request, 'index.html',)
    else:
        form = word_to_be_searched_form()
        return render(request, 'index.html', {'data': 'data', })


counter_dunya = 0
full_report_dunya = []
all_files_with_names = []
time_data = []
# GEO NEWS IS RUNNING IN PLACE OF DUNYA NOW


def generate_unique_filename():
    unique_id = str(uuid.uuid4())
    valid_chars = string.ascii_letters + string.digits + "_-"
    filename = ''.join(c for c in unique_id if c in valid_chars)
    return filename


def file_remover(folder_name, extension_name, appended_file_name):
    # jpg_files = glob.glob('headline_checker/*.jpg')
    jpg_files = glob.glob(f'{folder_name}/*.jpg')

    sorted_files = sorted(jpg_files, key=lambda x: os.path.getctime(x))

    for i in sorted_files:
        print('os.path.basename(i[0:3])', os.path.basename(i)[0:3])
        # if os.path.basename(i)[0:3]=='Geo':
        if os.path.basename(i)[0:3] == extension_name:

            # geo_ticker_remove.append(i)
            appended_file_name.append(i)
    # print('geo_ticker_remove',geo_ticker_remove)
    if len(appended_file_name) >= 100:
        for i in appended_file_name[0:96]:
            os.remove(i)


timedata_dunya = []
all_files_with_names_dunya = []
# @login_required(login_url=reverse_lazy('login'))


def dunya_ticker(request):

    # start_time = time.time()  # Get the current time

    date = datetime.datetime.now().date()
    timeticker = datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")

    timedata_dunya.clear()
    all_files_with_names_dunya.clear()
    start_time = time.time()  # Get the current time

    characters = streamer(source="https://www.youtube.com/watch?v=C6Se87yOvrk",
                          y1=297, y2=335, x1=89, x2=550, folder_save='Dunya_Ticker')

    text_ticker = Drive_OCR(
        f"D:/Haseeb/ticker/public/Dunya_Ticker/{characters}.jpg")

    text_ticker = text_ticker.main()
    # print('text_ticker',text_ticker)
    all_objects = Ticker_Extraction_Model.objects.filter(
        channel_name='Dunya').order_by('-id')[:20]

    if len(text_ticker) >= 16:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        ticker_write = True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)

            if similarity_ratio >= 80:
                # os.remove(f"Dunya_Ticker/{characters}.jpg")
                print('I am similarity')
                ticker_write = False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Dunya", channel_image="mzl-ftpchoha.png",
                                                   ticker_image=f"{characters}.jpg", date=date, time=formatted_time, text_ocr=text_ticker)

    # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Dunya').order_by('-id')[:10]

    for i in all_objects[:10]:
        # file_name=os.path.basename(i)
        all_files_with_names_dunya.append(i.ticker_image)
        timedata_dunya.append(i.time)

    return JsonResponse({'all_tickers': all_files_with_names_dunya, 'date': date, 'time': formatted_time, 'timedata': timedata_dunya})


timedata_geo = []
all_files_with_names_geo = {}
# @login_required(login_url=reverse_lazy('login'))


@csrf_exempt
def geo_ticker(request):

    start_time = time.time()  # Get the current time

    date = datetime.datetime.now().date()
    timeticker = datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")

    timedata_geo.clear()
    all_files_with_names_geo.clear()

    global geo_ticker_remove
    geo_ticker_remove = []

    # file_remover(folder_name='headline_checker',extension_name='Geo',appended_file_name=geo_ticker_remove)

    # characters,image=streamer(source="https://www.youtube.com/watch?v=O3DPVlynUM0",y1=262,y2=287,x1=162,x2=401,folder_save='Geo_Ticker')
    characters = streamer(source="https://www.youtube.com/watch?v=O3DPVlynUM0",
                          y1=305, y2=344, x1=1, x2=520, folder_save='Geo_Ticker')

    # text_ticker = Drive_OCR(f"D:/Haseeb/ticker/public/headline_checker/{'Geo'+characters}.jpg")
    text_ticker = Drive_OCR(
        f"D:/Haseeb/ticker/public/Geo_Ticker/{characters}.jpg")

    text_ticker = text_ticker.main()
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
    all_objects = Ticker_Extraction_Model.objects.filter(
        channel_name='Geo').order_by('-id')[:20]

    if len(text_ticker) >= 16:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        ticker_write = True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)

            if similarity_ratio >= 80:
                # os.remove(f"Dunya_Ticker/{characters}.jpg")
                # print('I am similarity')
                ticker_write = False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            # print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Geo", channel_image="geo.png",
                                                   ticker_image=f"{characters}.jpg", date=date, time=formatted_time, text_ocr=text_ticker)

    # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Geo').order_by('-id')[:10]
    all_objects_ten = all_objects[:10]
    for v, i in enumerate(all_objects_ten):
        # file_name=os.path.basename(i)
        all_files_with_names_geo[f'data_{v}'] = {
            'id': i.id, 'channel_image': i.channel_image, 'ticker_image': i.ticker_image, 'date': i.date, 'time': i.time}

    # time_data.append(i.time)
    # print('all_ocr_result',all_ocr_result)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers': all_files_with_names_geo})


result_all = []


# @login_required(login_url=reverse_lazy('login'))
@csrf_exempt
def convert_time_format(time_str):
    # Parse the time string into a datetime object
    time_obj = datetime.datetime.strptime(time_str, "%H:%M")

    # Convert the time to 12-hour format with AM/PM indicator
    formatted_time = time_obj.strftime("%I:%M %p")

    return formatted_time


# @login_required(login_url=reverse_lazy('login'))


@csrf_exempt
def table_view(request):
    global all_data_comparer

    data = data_result[10:]
    lenght_of_data = len(data_result)
    if all_data_comparer <= lenght_of_data:
        paginator = Paginator(data, 10)  # Display 10 entries per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        all_data_comparer += 10

        return render(request, 'index.html', {'result': page_obj, 'clear': 'True'})

    elif all_data_comparer > lenght_of_data:
        paginator = Paginator(data, 0)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        all_data_comparer = 0

        return render(request, 'index.html',)


timedata_ary = []
all_files_with_names_ary = []
# @login_required(login_url=reverse_lazy('login'))


@csrf_exempt
def ary_ticker(request):

    start_time = time.time()  # Get the current time

    date = datetime.datetime.now().date()
    timeticker = datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")

    timedata_ary.clear()
    all_files_with_names_ary.clear()

    characters = streamer(source="https://www.youtube.com/watch?v=sUKwTVAc0Vo",
                          y1=302, y2=359, x1=0, x2=531, folder_save='Ary_Ticker')
    text_ticker = Drive_OCR(
        f"D:/Haseeb/ticker/public/Ary_Ticker/{characters}.jpg")

    text_ticker = text_ticker.main()
    print('text_ticker', text_ticker)
    all_objects = Ticker_Extraction_Model.objects.filter(
        channel_name="Ary").order_by('-id')[:20]

    if len(text_ticker) >= 16:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        ticker_write = True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)

            if similarity_ratio >= 80:
                # os.remove(f"Dunya_Ticker/{characters}.jpg")
                print('I am similarity')
                ticker_write = False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Ary", channel_image="ary.png",
                                                   ticker_image=f"{characters}.jpg", date=date, time=formatted_time, text_ocr=text_ticker)

    # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Ary').order_by('-id')[:10]

    for i in all_objects[:10]:
        # file_name=os.path.basename(i)
        all_files_with_names_ary.append(i.ticker_image)
        timedata_ary.append(i.time)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers': all_files_with_names_ary, 'date': date, 'time': formatted_time, 'timedata': timedata_ary})


timedata_samaa = []
all_files_with_names_samaa = []
# @login_required(login_url=reverse_lazy('login'))


@csrf_exempt
def samaa_ticker(request):

    start_time = time.time()  # Get the current time

    date = datetime.datetime.now().date()
    timeticker = datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")

    timedata_samaa.clear()
    all_files_with_names_samaa.clear()
    global samaa_ticker_remove
    samaa_ticker_remove = []

    # file_remover(folder_name='headline_checker',extension_name='Sam',appended_file_name=samaa_ticker_remove)

    # characters,image=streamer(source="https://www.youtube.com/watch?v=yHi3yIkPcLE",y1=257,y2=341,x1= 2,x2=514,folder_save='Samaa_Ticker')
    characters = streamer(source="https://www.youtube.com/watch?v=yHi3yIkPcLE",
                          y1=304, y2=345, x1=1, x2=515, folder_save='Samaa_Ticker')

    # text_ticker = Drive_OCR(f"D:/Haseeb/ticker/public/headline_checker/{'Samaa'+characters}.jpg")
    text_ticker = Drive_OCR(
        f"D:/Haseeb/ticker/public/Samaa_Ticker/{characters}.jpg")

    text_ticker = text_ticker.main()
    # if 'Headlines' in str(text_ticker) or "ہیڈلائنز" in str(text_ticker):
    # face=image[281:335,2:514]
    # cv2.imwrite(f'Samaa_Ticker/{characters}.jpg',face)
    # else:
    # face = image[305:345, 1:515]
    # cv2.imwrite(f'Samaa_Ticker/{characters}.jpg',face)

    # print('text_ticker',text_ticker)
    all_objects = Ticker_Extraction_Model.objects.filter(
        channel_name="Samaa").order_by('-id')[:20]

    if len(text_ticker) >= 16:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        ticker_write = True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)

            if similarity_ratio >= 80:
                # os.remove(f"Dunya_Ticker/{characters}.jpg")
                print('I am similarity')
                ticker_write = False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Samaa", channel_image="Samaa_logo.png",
                                                   ticker_image=f"{characters}.jpg", date=date, time=formatted_time, text_ocr=text_ticker)

    # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Samaa').order_by('-id')[:10]

    for i in all_objects[:10]:
        # file_name=os.path.basename(i)
        all_files_with_names_samaa.append(i.ticker_image)
        timedata_samaa.append(i.time)
        # print('all_ocr_result',all_ocr_result)

    end_time = time.time()  # Get the current time after the task is completed
    execution_time = end_time - start_time  # Calculate the execution time

    print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers': all_files_with_names_samaa, 'date': date, 'time': formatted_time, 'timedata': timedata_samaa})


timedata_express = []
all_files_with_names_express = []
# @login_required(login_url=reverse_lazy('login'))


@csrf_exempt
def express_ticker(request):

    # start_time = time.time()  # Get the current time

    date = datetime.datetime.now().date()
    timeticker = datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")

    timedata_express.clear()
    all_files_with_names_express.clear()

    characters = streamer(source="https://www.youtube.com/watch?v=muBr6a3Xi2c",
                          y1=310, y2=358, x1=0, x2=495, folder_save='Express_Ticker')

    text_ticker = Drive_OCR(
        f"D:/Haseeb/ticker/public/Express_Ticker/{characters}.jpg")

    text_ticker = text_ticker.main()
    all_objects = Ticker_Extraction_Model.objects.filter(
        channel_name='Express').order_by('-id')[:20]

    # print('text_ticker',text_ticker)
    if len(text_ticker) >= 16:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():
        ticker_write = True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)

            if similarity_ratio >= 70:
                # os.remove(f"Dunya_Ticker/{characters}.jpg")
                # print('I am similarity')
                ticker_write = False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            # print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="Express", channel_image="express.png",
                                                   ticker_image=f"{characters}.jpg", date=date, time=formatted_time, text_ocr=text_ticker)

    # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='Express').order_by('-id')[:10]

    for i in all_objects[:10]:
        # file_name=os.path.basename(i)
        all_files_with_names_express.append(i.ticker_image)
        timedata_express.append(i.time)

    # end_time = time.time()  # Get the current time after the task is completed
    # execution_time = end_time - start_time  # Calculate the execution time

    # print(f"Function executed in {execution_time:.2f} seconds")
    return JsonResponse({'all_tickers': all_files_with_names_express, 'date': date, 'time': formatted_time, 'timedata': timedata_express})

# inside geo the dunya is running and inside dunya the geo is running


timedata_hum_news = []
all_files_with_names_hum_news = []
# @login_required(login_url=reverse_lazy('login'))


@csrf_exempt
def hum_news_ticker(request):

    # start_time = time.time()  # Get the current time

    date = datetime.datetime.now().date()
    timeticker = datetime.datetime.now().time()
    formatted_time = timeticker.strftime("%I:%M %p")

    timedata_hum_news.clear()
    all_files_with_names_hum_news.clear()
    start_time = time.time()  # Get the current time

    characters = streamer(source="https://www.youtube.com/watch?v=yBTnEiKy63o",
                          y1=313, y2=348, x1=33, x2=543, folder_save='HumNews_Ticker')

    text_ticker = Drive_OCR(
        f"D:/Haseeb/ticker/public/HumNews_Ticker/{characters}.jpg")

    text_ticker = text_ticker.main()
    # print('text_ticker',text_ticker)
    all_objects = Ticker_Extraction_Model.objects.filter(
        channel_name='HumNews').order_by('-id')[:20]
    if len(text_ticker) >= 16:
        # if Ticker_Extraction_Model.objects.filter(text_ocr__iexact=text_ticker).exists():

        ticker_write = True
        # Compare text similarity with each object
        for obj in all_objects:
            similarity_ratio = fuzz.ratio(text_ticker, obj.text_ocr)

            if similarity_ratio >= 0:
                # os.remove(f"Dunya_Ticker/{characters}.jpg")
                print('I am similarity')
                ticker_write = False
                break
                # matching_objects.append(obj)
                # ticker_write=True
        if ticker_write:
            print('I am writing in database')
            Ticker_Extraction_Model.objects.create(channel_name="HumNews", channel_image="HumNews.png",
                                                   ticker_image=f"{characters}.jpg", date=date, time=formatted_time, text_ocr=text_ticker)

    # all_tickers_files=Ticker_Extraction_Model.objects.filter(channel_name='NinetyTwo').order_by('-id')[:10]

    for i in all_objects[:10]:
        # file_name=os.path.basename(i)
        all_files_with_names_hum_news.append(i.ticker_image)
        timedata_hum_news.append(i.time)
        # print('all_ocr_result',all_ocr_result)

    return JsonResponse({'all_tickers': all_files_with_names_hum_news, 'date': date, 'time': formatted_time, 'timedata': timedata_hum_news})


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
date_images = []
time_images = []


def make_image(date_live, saver_name, list_saver):
    image_size = (200, 100)  # Desired image size
    background_color = (255, 255, 255)  # RGB color for the background
    text_color = (0, 0, 0)  # RGB color for the text
    font_size = 35
    # Replace with the path to your desired font file
    font_path = r"D:\ticker_new\Times New Roman\times new roman bold.ttf"

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
        position = ((image_size[0] - text_width) // 2,
                    (image_size[1] - text_height) // 2)

        # Draw the text on the image
        draw.text(position, date_live[i], font=font, fill=text_color)

        # Apply contrast enhancement to the image
        enhancer = ImageEnhance.Contrast(image)
        # Adjust the contrast factor as desired
        enhanced_image = enhancer.enhance(1.5)

        # Apply brightness enhancement to the image
        enhancer = ImageEnhance.Brightness(enhanced_image)
        # Adjust the brightness factor as desired
        brightened_image = enhancer.enhance(1.2)

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

        time_live = data.get('timeLive')
        date_live = data.get('dateLive')
        print('time_live', time_live)
        print('date_live', date_live)
        # Size of the font
        date_list_maker = make_image(
            date_live=date_live, saver_name='date', list_saver='date')
        time_list_maker = make_image(
            date_live=time_live, saver_name='time', list_saver='time')
        print('date_images', date_images)
        print('time_images', time_images)

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
                all_images_files.append(
                    'Express_Ticker/' + os.path.basename(i))
            elif getting_name == 'option5':
                logo = cv2.imread('image_detections/mzl-ftpchoha.png')
                # logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Dunya_Ticker/' + os.path.basename(i))
            elif getting_name == 'option6':
                logo = cv2.imread('image_detections/ninety_two.png')
                # logo = cv2.resize(logo, (100, image_height))
                all_images_files.append(
                    'NinetyTwo_Ticker/' + os.path.basename(i))

        # print('getting_live_collage_list', getting_live_collage_list)

        resized_images = []
        # date_image=cv2.imread('date.jpg')
        # logo = cv2.resize(logo, (100, 100))
        # date_image_resized = cv2.resize(date_image, (100, 100))

        # # Load the logo image and resize it
        # stacked_vertical = np.vstack((logo, date_image_resized))

        # stacked_vertical_resized = cv2.resize(stacked_vertical, (100, 100))
        stacked_vertical_images = []
        for i in range(len(date_images)):
            # date_image_stack=cv2.imread(date_images[i])
            date_image_resized = cv2.resize(date_images[i], (200, 90))

            # time_image_stack=cv2.imread(time_images[i])
            time_image_resized = cv2.resize(time_images[i], (200, 90))

            logo = cv2.resize(logo, (200, 150))
            stacked_vertical = np.vstack(
                (logo, date_image_resized, time_image_resized))
            # cv2.imwrite('stacked.jpg',stacked_vertical)

            stacked_vertical_images.append(stacked_vertical)

        print('len_date_images', len(date_images))
        print('len_time_images', len(time_images))
        print('len_all_images_files', len(all_images_files))
        # Resize and horizontally stack the logo and each image
        for i in range(len(all_images_files)):
            image = cv2.imread(all_images_files[i])
            resized_image = cv2.resize(image, (730, 110))
            resized_stacked_image = cv2.resize(
                stacked_vertical_images[i], (80, 110))
            # stacked=np.vstack(())
            stacked = np.hstack((resized_image, resized_stacked_image))
            resized_images.append(stacked)

        # Vertically stack the stacked images
        output_final = np.vstack(resized_images)
        cv2.imwrite('Collage/ticker.png', output_final)
        return JsonResponse({'success': 'success'})
    else:
        return JsonResponse({'error': 'error'})


@csrf_exempt
def getting_offline_collage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        getting_name = data.get('channelNameValue')
        print('i am channel', getting_name)
        getting_live_collage_list = data.get('liveCollageList')
        all_images_files = []
        all_images_files.clear()

        time_offline = data.get('timeOffline')
        date_offline = data.get('dateOffline')
        print('time_offline', time_offline)
        print('date_offline', date_offline)
        # Size of the font
        date_list_maker = make_image(
            date_live=date_offline, saver_name='date', list_saver='date')
        time_list_maker = make_image(
            date_live=time_offline, saver_name='time', list_saver='time')

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
                all_images_files.append(
                    'Express_Ticker/' + os.path.basename(i))
            elif getting_name == 'option5':
                logo = cv2.imread('image_detections/mzl-ftpchoha.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append('Dunya_Ticker/' + os.path.basename(i))
            elif getting_name == 'option6':
                logo = cv2.imread('image_detections/ninety_two.png')
                logo = cv2.resize(logo, (100, image_height))
                all_images_files.append(
                    'NinetyTwo_Ticker/' + os.path.basename(i))

        resized_images = []
        # date_image=cv2.imread('date.jpg')
        # logo = cv2.resize(logo, (100, 100))
        # date_image_resized = cv2.resize(date_image, (100, 100))

        # # Load the logo image and resize it
        # stacked_vertical = np.vstack((logo, date_image_resized))

        # stacked_vertical_resized = cv2.resize(stacked_vertical, (100, 100))
        stacked_vertical_images = []
        for i in range(len(date_images)):
            # date_image_stack=cv2.imread(date_images[i])
            date_image_resized = cv2.resize(date_images[i], (200, 90))

            # time_image_stack=cv2.imread(time_images[i])
            time_image_resized = cv2.resize(time_images[i], (200, 90))

            logo = cv2.resize(logo, (200, 150))
            stacked_vertical = np.vstack(
                (logo, date_image_resized, time_image_resized))
            # cv2.imwrite('stacked.jpg',stacked_vertical)

            stacked_vertical_images.append(stacked_vertical)

        print('len_date_images', len(date_images))
        print('len_time_images', len(time_images))
        print('len_all_images_files', len(all_images_files))
        # Resize and horizontally stack the logo and each image
        for i in range(len(all_images_files)):
            image = cv2.imread(all_images_files[i])
            resized_image = cv2.resize(image, (730, 110))
            resized_stacked_image = cv2.resize(
                stacked_vertical_images[i], (80, 110))
            # stacked=np.vstack(())
            stacked = np.hstack((resized_image, resized_stacked_image))
            resized_images.append(stacked)

        # Vertically stack the stacked images
        output_final = np.vstack(resized_images)
        cv2.imwrite('Collage/ticker.png', output_final)
        return JsonResponse({'success': 'success'})
    else:
        return JsonResponse({'error': 'error'})


def download_image(request):
    image_path = os.path.join(settings.BASE_DIR, 'Collage', 'ticker.png')
    # Replace 'Collage/ticker.png' with the actual path to your image file
    with open(image_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='image/png')

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        response['Content-Disposition'] = f'attachment; filename="ticker_{timestamp}.png"'
        return response


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


@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print('user', user)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid username or password.'
    else:
        error_message = ''

    return render(request, 'login.html', {'error_message': error_message})


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('login')


@csrf_exempt
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


counter_for_notifications = 0
official_result = []
official_word = []
notificationsList = []
clear_list_and_word = False


@csrf_exempt
def notifications(request):
    global clear_list_and_word
    global notificationsList
    print('notificationList', notificationsList)
    print('clear_list_and_word', clear_list_and_word)
    # if request.method=="GET":
    notification_increment = True
    # oldNotificationsViewButton=0

    length = 0
    length_all = 0
    date = datetime.datetime.now().date()

    # data=json.loads(request.body)
    get_words = words_to_be_searched_model.objects.filter(user=request.user)
    get_words_dict = get_words.values()
    # print('get_words',get_words)
    # words_list = get_words.split(',')
    # print('words_list',words_list)
    # print('newcount')
    # print('get_words_len',len(get_words))
    # print('get_words',get_words)
    if len(get_words) >= 1:
        results_dict = {}

        # if len(get_words)>1:
        for i in get_words:
            # print('words_list[words]',get_words[words])
            results = Ticker_Extraction_Model.objects.filter(
                text_ocr__icontains=i.word, date=date).order_by('-id').values()

            length_all += len(results)
            # results_all = results

            # results=results
        # data = list(results)
            data = list(results)
            # print('data',data)

            # Store the data for the current word in the results_dict
            results_dict[i.word] = data
        # length_all=len(results_dict)
        print('length_all', length_all)
        # for key,val in results_dict.items():

        #         #  print('key',key)
        #         #  print('val',val)
        #      for  i in val:
        #           length_all=len(val)
        #           print('length_all',len(val))
        #  length+=int(len(val))

        for word, data_list in results_dict.items():
            # print('data_list',data_list)
            if data_list:  # Make sure the data_list is not empty
                # first_data_for_word = data_list[0]
                all_words_list_of_dict = data_list
                for i in all_words_list_of_dict:

                    print('i am i ', i['id'])
        # print(f"First value of '{word}':", first_data_for_word)
                    if i not in official_result and i['id'] not in notificationsList:
                        print('data_appended')
                        official_result.append(i)
                        official_word.append(word)

            else:
                print(f"No data found for '{word}'")

        length = len(official_result)

        # print('results_dict_if',results_dict)

        # else:
        #         results = Ticker_Extraction_Model.objects.filter(text_ocr__icontains=get_words,date=date).values()
        #     # data = list(results)
        #  = list(results)

        #             # Store the data for the current word in the results_dict
        # results_dict[get_words] = data
        #         print('results_dict_else',results_dict)
        # notifications_count=len(results_dict)

        return JsonResponse({'official_word': official_word, 'notification_increment': notification_increment, 'get_words_dict': list(get_words_dict), 'success': 'success', 'notification_data': official_result, 'data_length': length_all, 'data_length_all': length}, safe=False)
    else:
        return JsonResponse({'error': 'error'})


@csrf_exempt
def list_clearer(request):
    global clear_list_and_word
    global notificationsList
    if request.method == "POST":
        data = json.loads(request.body)
        clear_list_and_word = data['clearList']
        notificationsList = data['notificationsList']
        if clear_list_and_word == True:
            official_result.clear()
            official_word.clear()
            clear_list_and_word = False

        # print('valueLoading',counted_value)

        # counter_for_notifications=counted_value
        return JsonResponse({'success': 'success'})
    else:
        return JsonResponse({'error': 'error'})
