# -*- coding: utf-8 -*-

from common.mymako import render_mako_context

from django.http import JsonResponse

import datetime
import json

from home_application.service import cc_search_biz,cc_search_host_ByBizId,cc_search_user

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os


def home(request):
    """
    首页
    """
    id = request.GET.get('id')
    return render_mako_context(request, '/home_application/home.html',{ "id":id})

def search_biz(request):
    data = cc_search_biz(request.user.username)
    data = data['data']
    selectData = []
    if data:
        for obj in data['info']:
            selectData.append({'label': obj['bk_biz_name'], 'value': obj['bk_biz_id']})
    return JsonResponse({'data': selectData})

def search_host(request,bizId):
    data = cc_search_host_ByBizId(bizId)
    data = data['data']
    hostList = []
    for obj in data['info']:
        host = obj['host']
        hostData = {}
        hostData['innerip'] = host['bk_host_innerip']
        hostData['host_name'] = host['bk_host_name']
        hostData['os_name'] = host['bk_os_name']
        cloud = host['bk_cloud_id']
        cloud_area = ''
        for c in cloud:
            cloud_area += (c['bk_inst_name'] + ',')
        hostData['cloud_name'] = cloud_area[0:cloud_area.__len__() - 1]

        hostData['bk_cloud_id'] = cloud[0]['id']
        hostList.append(hostData)
    return JsonResponse({'data': hostList})


def search_users(request):
    return JsonResponse(cc_search_user(), safe=False)


# 列表查询
def list(request):
    # name = request.GET.get('name')
    # if name:
    #     data = Custom.objects.filter(name__contains=name)
    # else:
    #     data = Custom.objects.filter(name__contains='')
    #
    # type = request.GET.get('type')
    # if type:
    #     data = Custom.objects.filter(type=type)

    listData = []
    # for obj in data:
    #     listData.append(obj.toJson())
    return JsonResponse({'data': listData})

# 添加数据
def add(request):
    data = json.loads(request.body)
    # exam = HostMonitor(business=data['business'],name=data['name'],exam_type=data['exam_type'],principal=data['principal'],phone=data['phone'],exam_date=datetime.datetime.strptime(str(data['exam_date']).split('T')[0], '%Y-%m-%d'),site=data['site'],filePath=data['filePath'])
    # exam.save()
    return JsonResponse({'result': 'true'})

# 删除数据
def delete(request,id):
    # Montitor.objects.filter(id=id).delete()
    return JsonResponse({'result': 'true'})

#修改数据
def update(request):
    """
        更新
        """
    params = json.loads(request.body)

    return JsonResponse({'result': True})

#查询数据
def one(request,id):
    #work = Work.objects.get(id=id)
    return JsonResponse({'data':{}}, safe=False)

# 上传文件
def upload(request):
    filedata = request.FILES.get('file')
    path = default_storage.save(os.getcwd()+"/static/"+filedata.name,ContentFile(filedata.read()))
    return JsonResponse({'data':path})
