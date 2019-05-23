import json

from django.http import HttpResponse
from django.shortcuts import render

from .forms import ReadFileForm

from .models import User, FacebookLabel, FacebookPage, facebookrequest

users = {}


def read_file(request):
    form = ReadFileForm()
    if request.method == 'POST':
        form = ReadFileForm(request.POST, request.FILES)

        if form.is_valid():

            content = request.FILES['file'].read().decode("utf-8")
            page_id = form.data["page_id"]
            token = form.data["access_token"]
            label_id = form.data["custom_label_id"]

            lines = content.split("\n")

            for row in lines[1:len(lines) - 1]:
                if not User.objects.filter(user_id=row[:len(row) - 2]).exists():
                 createdUser = User(user_id=row[:len(row) - 2])  # fill database User
                 createdUser.save()
            result = []
            for top in range(0, len(User.objects.all()), 50):
                user = User.objects.values_list('user_id', flat=True)[top:top + 50]
                api = facebookrequest(access_token=token, users_id=user, custom_label_id=label_id,page_id=page_id)
                result.append(api.multipleRequests())

            return HttpResponse(json.dumps(result),
                                content_type="application/json")  # return json result

    return render(request, 'read_file.html', locals())
