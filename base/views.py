from django.shortcuts import render, redirect
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
import base64
# from . models import *
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.template.loader import render_to_string

# Create your views here.

def home(request):
    return render(request, 'base/index.html')

def about(request):
    return render(request, 'base/about.html')

def contact(request):
    return render(request, 'base/contact.html')

def error(request):
    return render(request, 'base/404.html')

def getToken(request):
    #Build token with uid
    appId = 'e431994303bd4a92b37465d302e98306'
    appCertificate = '6f9d2b7ef3a045db94f36ebc50d1e3b2'
    channelName = request.GET.get('channel')
    uid = random.randint(1,230)
    expirationTimeInSeconds = 3600*24
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    print(("token"))

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token' : token, 'uid': uid}, safe=False)


def lobby(request):
    if request.session.has_key('username'):
        return render(request, 'base/lobby.html')
    else:
        return redirect("/lobby")

def room(request):
    if request.session.has_key('username'):
        return render(request, 'base/room.html')
    else:
        return redirect("/room")


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)


def login(request):
    if request.session.has_key('username'):
        return redirect("/")
    elif request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['username'] = username
            return redirect("/")
        else:
            messages.info(request,"Invalid credentials")
            return redirect("/login")
    else:
        # messages.info(request,"login successful")
        return render(request, 'base/login.html')

def logout(request):
    
    if request.session.has_key('username'):
        del request.session['username']
        auth.logout(request)
        return redirect("/")
    else:
        return redirect("/login")


def register(request):
    print("start register")
    if request.session.has_key('username'):
        return redirect("/")

    elif request.method == 'POST':
        print("register post")
        username = request.POST["name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if(password1 != password2):
            messages.info(request,"passowrd and confirm password are not same")

        if User.objects.filter(username=username).exists():
            messages.info(request,"Username alreay exists")
            return redirect("/login")
        elif User.objects.filter(email=email).exists():
            messages.info(request,"email already exists")
            return redirect("/login")
        else:
            user = User.objects.create_user(username=username,email=email,password=password1)
            user.save()
            messages.info(request,"User Created successfully please login now")
            return redirect('/login')
    else:
        return render(request, 'base/register.html')