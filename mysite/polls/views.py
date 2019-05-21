import json

import requests
from django.http import HttpResponse
from django.shortcuts import render
from . import settings

from .forms import ReadFileForm

from .models import User, FacebookLabel, FacebookPage

users = {}


def read_file(request):
    form = ReadFileForm()
    if request.method == 'POST':
        form = ReadFileForm(request.POST, request.FILES)

        if form.is_valid():

            content = request.FILES['file'].read().decode("utf-8")
            page_id = form.data["page_id"]
            token = form.data["access_token"]
            settings.ACCESS_TOKEN = token
            settings.PAGE_ID = page_id

            page = FacebookPage(access_token=settings.ACCESS_TOKEN, original_id=settings.PAGE_ID) # fill database table FacebookPage
            page.save()


            lines = content.split("\n")
            for row in lines[1:len(lines) - 1]:
                created = User(user_id=row[:len(row) - 2]) #fill database User
                created.save()
                data = {"user": row[:len(row) - 2]}
                headers = {'Content-Type': 'application/json', }
                response = requests.post(
                    'https://graph.facebook.com/v3.0/{}/label?access_token={}'.format(settings.CUSTOM_LABEL_ID,
                                                                                      settings.ACCESS_TOKEN),
                    headers=headers, data=data)
                print(response.text)
                if ("success" in response.text):
                    users[row[:len(row) - 2]] = "success"
                    label = FacebookLabel(owner=created, page=page, label_id=settings.CUSTOM_LABEL_ID) #fill database table FacebookLabel
                    label.save()
                else:
                    users[row[:len(row) - 2]] = "None"
            return HttpResponse(json.dumps(users), content_type="application/json") # return json result

    return render(request, 'read_file.html', locals())
