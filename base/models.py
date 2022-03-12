from django.db import models

# Create your models here.
'''
1. create databse modelroommember and store user name, uid and room name.
2. on join , create roommember in database
3. On handleuserlogin events, query db for room member name by uid and room name 
4. on leave, delete room member
'''

class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name