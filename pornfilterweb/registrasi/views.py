from django.shortcuts import render
from django.http import HttpResponse
from registrasi.models import Registrasi
from registrasi.forms import RegistrasiForm
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
import subprocess
import json
#from ipware.ip import get_real_ip
def registrasi(req):
    tmpl_vars = {
        'form': RegistrasiForm()
    }
    return render(req, 'registrasi/index.html',tmpl_vars)

def save_registration(request):
    if request.method == 'POST':
        mode = request.POST.get('mode')
        print mode
        ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ip:
            ip = ip.split(", ")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        print ip
        #ip = '127.0.0.1'
        registrasicount = Registrasi.objects.filter(ip = ip).count()
        if (registrasicount==0):
            registrasi = Registrasi(mode=mode, ip=ip)
            registrasi.save()
        elif (registrasicount>0):
            Registrasi.objects.get(ip=ip).delete()
            registrasi = Registrasi(mode=mode, ip=ip)
            registrasi.save()
        response_data = {}
        response_data['result'] = 'IP ' + registrasi.ip + ' Registration mode ' + registrasi.mode + ' successful'
        print response_data['result']
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
def user_list(request):
    users = Registrasi.objects.all().order_by('id')
    return render_to_response('registrasi/user_list.html',
                              {'users': users},
                              context_instance=RequestContext(request))
def user_search(request):
    user_field = request.POST.get('user_field','default')
    if user_field:
        users = Registrasi.objects.filter(ip__contains=user_field)
    else:
        users = Registrasi.objects.all().order_by('id')
    return render_to_response('registrasi/user_search.html',
                              {'users': users},
                              context_instance=RequestContext(request))

def user_edit(request, user_id=None):
    if user_id:
        user = get_object_or_404(Registrasi, pk=user_id)
    else:
        user = Registrasi()
    
    if request.method == 'POST':
        form = RegistrasiForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('registrasi:user_list')
    else:
        form = RegistrasiForm(instance=user)
        
    return render_to_response('registrasi/user_edit.html',
                              dict(form=form, user_id=user_id),
                              context_instance=RequestContext(request))

def user_del(request, user_id):
    user = get_object_or_404(Registrasi, pk=user_id)
    user.delete()
    return redirect('cms:user_list')