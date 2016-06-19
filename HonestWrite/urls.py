"""HonestWrite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import *
from django.contrib.auth.admin import *
from core.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login_user),
    url(r'^logout/$', logout_page),
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
    url(r'^studentHome/$', stuhome),
    url(r'^studentHome/registerclass/$', registerclass),
    url(r'^forgotpwd/$', forgotpwd_page),
    url(r'^addclass/$', addclass),
    url(r'^addclass/addclass1/$', addclass),
    url(r'^profile/$', profile),
    url(r'^home/class/(?P<class_id>[0-9]+?)/$', viewclass),
    url(r'^studentHome/checkclass/$', checkclass),
    url(r'^studentHome/validateclass/$', validateclass),
    url(r'^studentHome/profile/$', stuprofile)
]
