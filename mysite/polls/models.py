from django.db import models
import requests


class User(models.Model):
    user_id = models.TextField(unique=True)

    def __str__(self):
        return self.user_id


class FacebookPage(models.Model):
    access_token = models.TextField()
    original_id = models.TextField()

    def __str__(self):
        return self.original_id


class FacebookLabel(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, )
    page = models.ForeignKey("FacebookPage", on_delete=models.CASCADE)
    label_id = models.TextField()

    def __str__(self):
        return "owner {} \npage {} \n label_id {}".format(self.owner, self.page, self.label_id)


class facebookrequest:
    def __init__(self, access_token, users_id, custom_label_id,page_id):
        self.data = {'access_token': access_token}
        self.headers = {'Content-Type': 'application/json', }
        self.batch = []
        self.users_id1 = users_id
        self.label_id = custom_label_id
        for user_id in self.users_id1:
            self.batch.append({
                'method': 'POST',
                'relative_url': f'v3.3/{self.label_id}/label',
                'body': f'user={user_id}'
            })
        self.data['batch'] = str(self.batch)
        self.length = len(users_id)
        if not FacebookPage.objects.filter(original_id=page_id).exists():
            self.page = FacebookPage(access_token=access_token, original_id=page_id)  # fill database table FacebookPage
            self.page.save()
        else:
           self.page = FacebookPage.objects.get(original_id=str(page_id))



    def multipleRequests(self):
        response = requests.post('https://graph.facebook.com', self.data, headers=self.headers)
        dectResult = {}
        for i in range(0, self.length):
            print(i)
            if "success" in response.json()[i]['body']:
                dectResult[self.users_id1[i]] = True

                if not FacebookLabel.objects.filter(owner=User.objects.get(user_id = str(self.users_id1[i])),page=self.page,label_id = self.label_id).exists():
                    label = FacebookLabel(owner=User.objects.get(user_id = str(self.users_id1[i])),page=self.page,label_id = self.label_id)
                    label.save()
            else:
                dectResult[self.users_id1[i]] = "Null"
        return dectResult
