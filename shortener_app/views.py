from analytics.models import ClickEvent
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View

from .forms import SubmitURLForm
from .models import WinURL


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitURLForm()
        context = {
            'title': 'url2.win shortener',
            'form': the_form
        }
        return render(request, 'shortener_app/home.html', context)


    def post(self, request, *args, **kwargs):
        form = SubmitURLForm(request.POST)
        template = 'shortener_app/home.html'
        context = {
            'title': 'url2.win shortener',
            'form': form
        }
        if form.is_valid():
            new_url = form.cleaned_data.get('url')
            obj, created = WinURL.objects.get_or_create(winurl=new_url)
            context = {
                'object': obj,
                'created': created
            }
            if created:
                template = 'shortener_app/success.html'
            else:
                template = 'shortener_app/already_exists.html'
        return render(request, template, context)


class WinRedirectView(View):
    def get(self, request, shortcode, *args, **kwargs):
        obj = get_object_or_404(WinURL, shortcode=shortcode)
        print('Count: ', ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.winurl)