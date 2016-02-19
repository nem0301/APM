from django.conf.urls import url
from . import views
from views import MonitorView, ProcessView

urlpatterns = [    
    url(r'^$', MonitorView.as_view(), name='overall'),
    url(r'^(?P<pid>[0-9]+)/$', ProcessView.as_view(), name='process'),
    ]     