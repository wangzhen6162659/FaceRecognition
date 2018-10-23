from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import myapp.models
import json
import myapp.facerec
from django.core import serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import JsonResponse
import numpy

from io import StringIO
from io import BytesIO
import os


# Create your views here.
# 设置跨域
@staticmethod
def get(request):
    response = JsonResponse(get_face, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


@staticmethod
def post(request):
    response = JsonResponse(get_face, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return HttpResponse()


@require_http_methods(["GET"])
def add_book(request):
    response = {}
    book = myapp.models.User(book_name=request.GET.get('book_name'))
    book.save()
    response['msg'] = 'success'
    response['error_num'] = 0
    # except  Exception,e:
    #     response['msg'] = str(e)
    #     response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def show_books(request):
    response = {}
    books = myapp.models.User.objects.filter()
    response['list'] = json.loads(serializers.serialize("json", books))
    response['msg'] = 'success'
    response['error_num'] = 0

    return JsonResponse(response)


@require_http_methods(["POST"])
def get_face(request):
    file = request.FILES.get('file')
    response = {}
    # 1.人脸关键点检测器
    predictor_path = 'E://pythonweb//myproject//myapp//1.dat'
    # 2.人脸识别模型
    face_rec_model_path = 'E://pythonweb//myproject//myapp//2.dat'
    img = file.read()
    # 5.获取用户表中的人脸数据信息
    users = myapp.models.User.objects.filter()
    # 文件保存测试
    target = "media/upload/avatar"  # 文件保存路径
    file_path = os.path.join('static', 'upload', file.name)
    f = open(file_path, 'wb')
    for chunk in file.chunks():
        f.write(chunk)
    f.close()


    id_labels = []
    descriptors = []
    # a = myapp.models.Vector(1,2,3)
    for user in users:
        if user.face_data != None:
            id_labels.append(user.id)
            arr = user.face_data.split(',')
            newArr = []
            for value in arr:
                newArr.append(float(value))
            descriptors.append(numpy.array(newArr))
    ret = myapp.facerec.getFace([predictor_path, face_rec_model_path, descriptors, id_labels], BytesIO(img))
    ret = list(filter(lambda x: x[1] < 0.35, ret))
    if len(ret) == 0:
        return JsonResponse({'target': None})
    return JsonResponse({'target': ret[0]})

@require_http_methods(["POST"])
def save_face(request):
    file = request.FILES.get('file')
    response = {}
    # 1.人脸关键点检测器
    predictor_path = 'E://pythonweb//myproject//myapp//1.dat'
    # 2.人脸识别模型
    face_rec_model_path = 'E://pythonweb//myproject//myapp//2.dat'
    img = file.read()
    # 5.获取用户表中的人脸数据信息
    users = myapp.models.User.objects.filter()
    id_labels = []
    descriptors = []
    # a = myapp.models.Vector(1,2,3)
    for user in users:
        if user.face_data != None:
            id_labels.append(user.id)
            arr = user.face_data.split(',')
            newArr = []
            for value in arr:
                newArr.append(float(value))
            descriptors.append(numpy.array(newArr))
    ret = myapp.facerec.getFace([predictor_path, face_rec_model_path, descriptors, id_labels], BytesIO(img))
    ret = list(filter(lambda x: x[1] < 0.35, ret))
    if len(ret) == 0:
        return JsonResponse({'target': None})
    return JsonResponse({'target': ret[0]})
