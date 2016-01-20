from django.conf.urls import patterns, url
from django.views.generic.list import ListView

from fir_siem import views
from fir_siem.models import SIEMCase

urlpatterns = patterns('',
    url (r'^cases_list$', ListView.as_view(model=SIEMCase), name="cases_list"),
    url (r'^collect_mails$', views.collect_mail, name="collect_mail"),
)
