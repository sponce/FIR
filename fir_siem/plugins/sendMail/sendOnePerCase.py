import json
from fir_siem.models import Email
from incidents.models import Attribute

def send_mail(case, incident):
    '''Send a mail to the user only if there was no previous mail exchange'''
    if Email.objects.filter(case=case).count() == 0:
        details = json.loads(Attribute.objects.filter(incident=incident, name='details')[0].value)
        return [('uniqueMailTemplate',
                 { 'sender' : 'sebastien.ponce@cern.ch',
                   'to' : details['userMail'],
                   'subject' : 'About security incident SIEMCase=%d' % case.id,
                   'body' : 'You should take action about this :\n%s' % (details['subject'])})]
    return []
