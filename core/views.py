from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db import IntegrityError
from core.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from core.models import *
from django.core.mail import send_mail
# Create your views here.

def handle_uploaded_file(f):
    with open(settings.MEDIA_ROOT + settings.MEDIA_URL + str(f), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return f

@login_required
def superuser(request):
    stuob = UStudent.objects.get(username__username=request.user.username)
    facob = UFaculty.objects.get(username__username=request.user.username)
    if stuob:
        return {'profilepic': stuob.profilepic.url}
    elif facob:
        return {'profilepic': facob.profilepic.url}
    else:
        return {'profilepic': 'No Image'}

# This view registers the user
@csrf_protect
def register(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        try:
            User.objects.get(username=username)
            d = 'True'
            return render(request, 'registration/register.html', {'userpresent': d})

        except ObjectDoesNotExist:
            if password1 == password2:
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=request.POST['emailid'],
                    is_staff=request.POST.get('is_staff', False),
                )
                user.set_password(password1)
                user.save()
                if user.is_staff:
                    facob = UFaculty.objects.create(
                        username_id=username,
                    )
                    facob.save()
                else:
                    stuob = UStudent.objects.create(
                        username_id=username,
                    )
                    stuob.save()
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
@csrf_protect
# Forgot password view
def forgotpwd_page(request):

    if request.method == 'POST':
        username = request.POST['username']
        userob = AuthUser.objects.get(username=username)
        send_mail(
            'HonestWrite Password',
            'Your Password is:' + userob.password,
            'sojitradhawal@gmail.com',
            [userob.email],
        )
        return render(request, 'registration/login.html', {'emailSent': True})
    else:
        return render(request, 'forgotpwd.html')



# Login view

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if request.user.is_staff:
                facultyob = UFaculty.objects.get(username__username=request.user.username)
                userob = AuthUser.objects.get(username=request.user.username)
                request.session['userob'] = userob.username
                if facultyob.profilepic.url:
                    request.session['profilepic'] = str(facultyob.profilepic.url)
                return HttpResponseRedirect('/home/')
            else:
                stuob = UStudent.objects.get(username__username=request.user.username)
                userob = AuthUser.objects.get(username=request.user.username)
                request.session['userob'] = userob.username
                if stuob.profilepic:
                    request.session['profilepic'] = str(stuob.profilepic.url)
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
@login_required
def stuhome(request):
        classob = stuClass.objects.filter(username_id=request.user.username, classid__c_duedate__gt=datetime.datetime.now().date())
        userob = AuthUser.objects.filter(username=request.user.username)
        classid = stuClass.objects.values('classid_id').distinct()
        return render(request,
                      'studentHome.html',
                      {'userob': userob, 'classob': classob, 'classid': classid},
                      )
# View Class for Faculty
@login_required
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
@login_required
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
@login_required
def profile(request):
    try:
        facultyob = UFaculty.objects.get(username=request.user.username)
        authuserob = AuthUser.objects.get(username=request.user.username)
        d = {'first_name': authuserob.first_name, 'last_name':authuserob.last_name, 'school': facultyob.f_school, 'faculty': facultyob.f_faculty, 'major': facultyob.f_major, 'emailid':authuserob.email, 'profilepic': facultyob.profilepic.url}
        if request.method == 'POST':
            if UFaculty.objects.filter(username=request.user.username):
                faculty1 = UFaculty.objects.filter(username=request.user.username).update(
                    f_school=request.POST['school'],
                    f_faculty=request.POST['faculty'],
                    f_major=request.POST['major'],
                )
                if request.FILES.get('profilepic', False):
                    faculty1 = UFaculty.objects.filter(username=request.user.username).update(
                        profilepic = handle_uploaded_file(request.FILES['profilepic'])
                    )
                    facultyob = UFaculty.objects.get(username=request.user.username)
                    request.session['profilepic'] = facultyob.profilepic.url
            authuser = AuthUser.objects.filter(username=request.user.username).update(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['emailid']
            )
            facultyob = UFaculty.objects.get(username=request.user.username)
            authuserob = AuthUser.objects.get(username=request.user.username)
            d = {'first_name': authuserob.first_name, 'last_name': authuserob.last_name, 'school': facultyob.f_school,
                 'faculty': facultyob.f_faculty, 'major': facultyob.f_major, 'emailid': authuserob.email, 'profilepic': facultyob.profilepic}
            d1 = 'True'
            return render(request, 'profile.html', {"values": d, "record_added": d1})
        else:
            return render(request, 'profile.html', {"values": d})

    except ObjectDoesNotExist:
        authuserob = AuthUser.objects.get(username=request.user.username)
        d = {'first_name': authuserob.first_name, 'last_name': authuserob.last_name, 'emailid': authuserob.email}
        if request.method == 'POST':
                facultyob = UFaculty.objects.create(
                    username_id=request.user.username,
                    f_school=request.POST['school'],
                    f_faculty=request.POST['faculty'],
                    f_major=request.POST['major'],
                )
                if request.FILES['profilepic']:
                    facultyob.profilepic = handle_uploaded_file(request.FILES['profilepic'])
                authuser = AuthUser.objects.filter(username=request.user.username).update(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['emailid']
                )
                facultyob = UFaculty.objects.get(username=request.user.username)
                authuserob = AuthUser.objects.get(username=request.user.username)
                request.session['profilepic'] = facultyob.profilepic.url
                d = {'first_name': authuserob.first_name, 'last_name': authuserob.last_name,
                     'school': facultyob.f_school,
                     'faculty': facultyob.f_faculty, 'major': facultyob.f_major, 'emailid': authuserob.email, 'profilepic': facultyob.profilepic}
                d1 = 'True'
                return render(request, 'profile.html', {"values": d, "record_added": d1})
        else:
            return render(request, 'profile.html', {"values": d})

@login_required
def registerclass(request):
    if request.method == 'POST':
        classid = int(request.POST['classid'])
        userid = request.user.username
        classob = stuClass.objects.create(
            username_id=userid,
            classid_id=classid
        )
        resultob = CResults.objects.create(
            classid_id=classid,
            username_id=userid,
            grade='TBD',
            subdate=datetime.datetime.now().date()
        )
        return HttpResponseRedirect('/studentHome/')
    else:
        return HttpResponseRedirect('/studentHome/')

@login_required
def checkclass(request):
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
@login_required
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
                if request.FILES.get('profilepic', False):
                    stuob = UStudent.objects.filter(username=request.user.username).update(
                        profilepic = handle_uploaded_file(request.FILES['profilepic'])
                    )
                    stuob = UStudent.objects.get(username=request.user.username)
                    request.session['profilepic'] = stuob.profilepic.url
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
            if request.FILES['profilepic']:
                studentob.profilepic = handle_uploaded_file(request.FILES['profilepic'])
            authuser = AuthUser.objects.filter(username=request.user.username).update(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['emailid']
            )
            studentob = UStudent.objects.get(username=request.user.username)
            request.session['profilepic'] = studentob.profilepic.url
            authuserob = AuthUser.objects.get(username=request.user.username)
            d = {'first_name': authuserob.first_name, 'last_name': authuserob.last_name,
                 'school': studentob.s_school,
                 'faculty': studentob.s_faculty, 'major': studentob.s_major, 'emailid': authuserob.email}
            d1 = 'True'
            return render(request, 'stuprofile.html', {"values": d, "record_added": d1})
        else:
            return render(request, 'stuprofile.html', {"values": d})
@login_required
def myclass(request, class_id):
    questionob = CQuestions.objects.filter(classid_id=class_id)
    questions = serializers.serialize('json', questionob)
    return render(request, 'myclass.html', {'questionob': questionob, 'questions': questions})

@login_required
def getquestions(request, class_id):
    questionob = CQuestions.objects.filter(classid_id=class_id)
    data = serializers.serialize('json', questionob)
    return HttpResponse(data)

@login_required
@csrf_protect
def checkuname(request):
    username = request.POST.get('username', False)
    if username:
        userob = AuthUser.objects.filter(username=username).count()
        if userob:
            responce = "Your password will be sent your email."
        else:
            responce = "Username not present."
    else:
        responce = ""

    return HttpResponse(responce)
@login_required
def reports(request):
    classid = FClass.objects.filter(username__username=request.user.username)
    return render(request, 'reports.html', {'classid': classid})

@login_required
def reportgen(request):
    if request.method == 'POST':
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import PropertySet
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_CENTER

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reportforclass.pdf"'
        elements = []
        doc = SimpleDocTemplate(response, pagesize=letter)
        p = ParagraphStyle(PropertySet)
        p.textColor = 'black'
        p.alignment = TA_CENTER
        p.fontSize = 25
        p.spaceAfter = 25
        p.spaceBefore = 0
        para = Paragraph("Student Report", p)
        elements.append(para)
        p = ParagraphStyle('Normal')
        para = Paragraph(" ", p)
        elements.append(para)
        data = [['ClassID', 'Student', 'Result', 'Due Date', 'Submitted On']]
        classid = request.POST['classid']
        cresults = CResults.objects.filter(classid=classid).select_related('username')
        for result in cresults:
            temp = [result.classid_id, result.username.first_name + " " + result.username.last_name, result.grade, result.classid.c_duedate, result.subdate]
            data.append(temp)

        row = int(len(cresults)+1)

        t = Table(data, 5 * [1.5 * inch], row * [0.4 * inch])
        t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
                                ('FONTSIZE', (0, 0), (-1, 0), 13),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                            ]))

        elements.append(t)
        # write the document to disk
        doc.build(elements)
        return response
    else:
        return HttpResponseRedirect('/reports/')
    
def submitquiz(request):
    classid = request.POST['classid']
    CResults.objects.filter(classid_id=classid,username_id=request.user.username).update(grade='PASS', subdate=datetime.datetime.now().date())
    stuClass.objects.filter(classid_id=classid, username_id=request.user.username).delete()
    return HttpResponseRedirect('/studentHome/')
    
    