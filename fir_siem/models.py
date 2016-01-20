from django.db import models
from django import forms
import datetime

from incidents.models import Incident

class SIEMCase(models.Model):
    related_incidents = models.ManyToManyField(Incident)

    def __unicode__(self):
        return 'Case %d' % self.id

class Email(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    sender = models.TextField(null=True, blank=True)
    to = models.TextField(null=True, blank=True)
    cc = models.TextField(null=True, blank=True)
    bcc = models.TextField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    case = models.ForeignKey(SIEMCase)

    def __unicode__(self):
        return '[' + self.to + '] ' + self.subject
