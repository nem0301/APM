from django.conf.urls import url
from . import views
from views import MonitorView

urlpatterns = [
#     url(r'^', views.index, name='index'),
    url(r'^', MonitorView.as_view(), name='index'),
    ]     