from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db import IntegrityError
from core.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from core.models import *
import json

# Create your views here.

# This view registers the user
@csrf_protect
def register(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        username = request.POST['username']
        try:
            User.objects.get(username=username)
            d = 'True'
            return render(request, 'registration/register.html', {'userpresent': d})

        except ObjectDoesNotExist:
            if password1 == password2:
                user = User.objects.create(
                    username=username,
                    email=request.POST['emailid'],
                    is_staff=request.POST.get('is_staff', False),
                )
                user.set_password(password1)
                user.save()
                return HttpResponseRedirect('/register/success/')
            else:
                d = 'True'
                return render(request, 'registration/register.html', {'nomatch': d})
    else:
        return render(request, 'registration/register.html')

# This view will be generated on successful registration
def register_success(request):
    return render_to_response(
        'registration/success.html',
    )

# This view logs out the user
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

# Forgot password view
def forgotpwd_page(request):
    return render_to_response(
        'forgotpwd.html'
    )
# Login view
@csrf_protect
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if request.user.is_staff:
                classob = FClass.objects.filter(username=request.user.username)
                userob = AuthUser.objects.get(username=request.user.username)
                request.session['userob'] = userob.username
                return HttpResponseRedirect('/home/')
            else:
                userob = AuthUser.objects.get(username=request.user.username)
                request.session['userob'] = userob.username
                return HttpResponseRedirect('studentHome/')
        else:
            d = 'True'
            return render(request, 'registration/login.html', {'notlogin':d})
    return render(request, 'registration/login.html')

@login_required
# Faculty Home Page
def home(request):
    if request.method == 'POST':
        classob = FClass.objects.filter(username=request.user.username)
        return render(request,
                      'home.html',
                      {'classob': classob},
                      )
    else:
        classob = FClass.objects.filter(username=request.user.username)
        return render(request,
                      'home.html',
                      {'classob': classob},
                      )
# Student Home page
def stuhome(request):
    if request.method == 'POST':
        userob = AuthUser.objects.filter(username=request.user.username)
        return render(request,
                      'studentHome.html',
                      {'userob': userob},
                      )
    else:
        userob = AuthUser.objects.filter(username=request.user.username)
        return render(request,
                      'studentHome.html',
                      {'userob': userob},
                      )

# View Class for Faculty
def viewclass(request, class_id):
    if request.method == 'POST':
        try:
            classob = FClass.objects.get(id=class_id)
            return render(request, 'ShowClass.html', {"classob":classob})
        except ObjectDoesNotExist:
            classob = FClass.objects.filter(username=request.user.username)
            return render(request, 'home.html', {'classob':classob})
    else:
        classob = FClass.objects.get(id=class_id)
        return render(request, 'ShowClass.html', {"classob": classob})





@csrf_protect
def addclass(request):
    if request.method == 'POST':
        true = 'True'
        try:
            class1 = FClass.objects.create(
                id=request.POST['classid'],
                username_id=request.user.username,
                c_style=request.POST['style'],
                c_topic=request.POST['topic'],
                c_duedate=request.POST['duedate']
            )
            d = true
            return render(request, 'addclass.html', {"record_added":d})
        except IntegrityError:
            d = true
            return render(request, 'addclass.html', {"record_found":d})

    else:
        return render(request, 'addclass.html')

# View/Edit Profile
def profile(request):
    try:
        facultyob = UFaculty.objects.get(username=request.user.username)
        authuserob = AuthUser.objects.get(username=request.user.username)
        d = {'first_name': authuserob.first_name, 'last_name':authuserob.last_name, 'school': facultyob.f_school, 'faculty': facultyob.f_faculty, 'major': facultyob.f_major, 'emailid':authuserob.email}
        if request.method == 'POST':
            if UFaculty.objects.get(username=request.user.username):
                faculty1 = UFaculty.objects.filter(username=request.user.username).update(
                    f_school=request.POST['school'],
                    f_faculty=request.POST['faculty'],
                    f_major=request.POST['major']
                )
            authuser = AuthUser.objects.filter(username=request.user.username).update(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['emailid']
            )
            facultyob = UFaculty.objects.get(username=request.user.username)
            authuserob = AuthUser.objects.get(username=request.user.username)
            d = {'first_name': authuserob.first_name, 'last_name': authuserob.last_name, 'school': facultyob.f_school,
                 'faculty': facultyob.f_faculty, 'major': facultyob.f_major, 'emailid': authuserob.email}
            d1 = 'True'
            return render(request, 'profile.html', {"values":d, "record_added":d1})
        else:
            return render(request, 'profile.html', {"values":d})

    except ObjectDoesNotExist:
        authuserob = AuthUser.objects.get(username=request.user.username)
        d = {'first_name': authuserob.first_name, 'last_name': authuserob.last_name, 'emailid': authuserob.email}
        if request.method == 'POST':
                facultyob = UFaculty.objects.create(
                    username_id=request.user.username,
                    f_school=request.POST['school'],
                    f_faculty=request.POST['faculty'],
                    f_major=request.POST['major']
                )
                authuser = AuthUser.objects.filter(username=request.user.username).update(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['emailid']
                )
                facultyob = UFaculty.objects.get(username=request.user.username)
                authuserob = AuthUser.objects.get(username=request.user.username)
                d = {'first_name': authuserob.first_name, 'last_name': authuserob.last_name,
                     'school': facultyob.f_school,
                     'faculty': facultyob.f_faculty, 'major': facultyob.f_major, 'emailid': authuserob.email}
                d1 = 'True'
                return render(request, 'profile.html', {"values":d, "record_added":d1})
        else:
            return render(request, 'profile.html', {"values":d})


def registerclass(request):
    if request.method == 'POST':
        classob = stuClass.objects.create(
            username_id=request.user.username,
            classid_id = int(request.POST['classid'])
        )
        return HttpResponseRedirect('/studentHome/')
    else:
        return HttpResponseRedirect('/studentHome/')


def checkclass(request):
    from core.models import FClass
    from django.http import HttpResponse
    classid = request.POST.get('classid', False)
    if classid:
        try:
            classob = FClass.objects.filter(id=classid).count()
            stuclassob = stuClass.objects.filter(username_id=request.user.username, classid_id=classid).count()
            if classob and not stuclassob:
                responce = "You can register to this class"
            elif stuclassob:
                responce = "You are already registered to this class"
            else:
                responce = "Class not Present. Please check the class ID"
        except ValueError:
            responce = "Class ID should be in numbers"
    else:
        responce = ""

    return HttpResponse(responce)

def validateclass(request):
    from core.models import FClass
    from django.http import HttpResponse
    classid = request.POST.get('classid', False)
    if classid:
        try:
            classob = FClass.objects.filter(id=classid).count()
            if classob:

                responce = "true"
            else:
                responce = "false"
        except ValueError:
            responce = "false"
    else:
        responce = "false"

    return HttpResponse(responce)

def stuprofile(request):
    try:
        studentob = UStudent.objects.get(username=request.user.username)
        authuserob = AuthUser.objects.get(username=request.user.username)
        d = {'first_name': authuserob.first_name, 'last_name': authuserob.last_name, 'school': studentob.s_school,
             'faculty': studentob.s_faculty, 'major': studentob.s_major, 'emailid': authuserob.email}
        if request.method == 'POST':
            if UStudent.objects.get(username=request.user.username):
                studentob = UStudent.objects.filter(username=request.user.username).update(
                    s_school=request.POST['school'],
                    s_faculty=request.POST['faculty'],
                    s_major=request.POST['major']
                )
            authuserob = AuthUser.objects.filter(username=request.user.username).update(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['emailid']
            )
            studentob = UStudent.objects.get(username=request.user.username)
            authuserob = AuthUser.objects.get(username=request.user.username)
            d = {'first_name': authuserob.first_name, 'last_name': authuserob.last_name, 'school': studentob.s_school,
                 'faculty': studentob.s_faculty, 'major': studentob.s_major, 'emailid': authuserob.email}
            d1 = 'True'
            return render(request, 'stuprofile.html', {"values": d, "record_added": d1})
        else:
            return render(request, 'stuprofile.html', {"values": d})

    except ObjectDoesNotExist:
        authuserob = AuthUser.objects.get(username=request.user.username)
        d = {'first_name': authuserob.first_name, 'last_name': authuserob.last_name, 'emailid': authuserob.email}
        if request.method == 'POST':
            studentob = UStudent.objects.create(
                username_id=request.user.username,
                s_school=request.POST['school'],
                s_faculty=request.POST['faculty'],
                s_major=request.POST['major']
            )
            authuser = AuthUser.objects.filter(username=request.user.username).update(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['emailid']
            )
            studentob = UStudent.objects.get(username=request.user.username)
            authuserob = AuthUser.objects.get(username=request.user.username)
            d = {'first_name': authuserob.first_name, 'last_name': authuserob.last_name,
                 'school': studentob.s_school,
                 'faculty': studentob.s_faculty, 'major': studentob.s_major, 'emailid': authuserob.email}
            d1 = 'True'
            return render(request, 'stuprofile.html', {"values": d, "record_added": d1})
        else:
            return render(request, 'stuprofile.html', {"values": d})