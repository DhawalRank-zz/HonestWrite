from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from core.models import UStudent, UFaculty


@login_required
def superuser(request):
    stuob = UStudent.objects.filter(username__username=request.user.username)
    facob = UFaculty.objects.filter(username__username=request.user.username)
    if stuob:
        for stu in stuob:
            profilepic = [stu.profilepic.url]
            return {'profilepic': profilepic }
    elif facob:
        for fac in facob:
            profilepic = fac.profilepic.url
            return {'profilepic': profilepic }
    else:
        return HttpResponseRedirect('/')