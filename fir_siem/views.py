import re, imaplib, email, email.utils, time, datetime, json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail

from incidents.models import Incident, Attribute

from fir_siem.models import SIEMCase, Email
import fir_siem.plugins 

def find_cases_for_incident(incident):
    cases = set([])
    for plugin in fir_siem.plugins.incoming_incidents_plugins:
        cases = cases.union(plugin.find_cases(incident))
    return cases

def create_and_send_mail(case, template, params):    
    mail = Email(sender=params['sender'], to=params['to'], subject=params['subject'],
                 body=params['body'], case=case)
    mail.save()
    # fake mail fields for now, template is not used
    send_mail(params['subject'], params['body'], params['sender'],
              [params['to']], fail_silently=False)

def send_mail_if_needed(case, incident):
    mails = []
    for plugin in fir_siem.plugins.send_mail_plugins:
        mails += plugin.send_mail(case, incident)
    for template, params in mails:
        create_and_send_mail(case, template, params)

def add_incident_to_case(case, incident):
    case.related_incidents.add(incident)
    send_mail_if_needed(case, incident)

@receiver(post_save, sender=Incident)
def incident_to_case(sender, **kwargs):
    incident = kwargs['instance']
    # add some details to the incident
    # XXX to be passed properly from the security framework
    details = Attribute(name='details',
                        value=json.dumps({'subject':incident.subject,
                                          'userMail':'sebastien.ponce@cern.ch'}),
                        incident=incident)
    details.save()
    # try to associate it to existing cases
    cases = find_cases_for_incident(incident)
    if cases:
        for case in cases:
            add_incident_to_case(case, incident)
    else:
        # create a new case
        new_case = SIEMCase()
        new_case.save()
        add_incident_to_case(new_case, incident)

email_pattern = re.compile('SIEMCase=(\d*)')

def find_case_for_email(subject):
    match = re.search(email_pattern, subject)
    if match:
        try:
            caseId = int(match.group(1))
            print caseId
            print 'a', SIEMCase.objects.get(id=caseId)
            return SIEMCase.objects.get(id=caseId)
        except Exception, e:
            print e
            pass
    return None

def handle_new_mail(case, email):
    mails = []
    for plugin in fir_siem.plugins.incoming_mail_plugins:
        mails += plugin.answer_mail(case, email)
    for template, params in mails:
        create_and_send_mail(case, template, params)

def collect_mail(request):
    user = getattr(settings, "IMAP_USER", None)
    passwd = getattr(settings, "IMAP_PASSWD", None)
    host = getattr(settings, "IMAP_HOST", None)
    port = int(getattr(settings, "IMAP_PORT", "993"))
    log = ""
    if user and passwd and host:
        m = imaplib.IMAP4_SSL(host, port)
        m.login(user, passwd)
        m.select("SecurityTest")
        resp, items = m.search(None, 'ALL')
        items = items[0].split()
        nbNewMailObjects = 0
        for emailid in items[::-1]:
            resp, data = m.fetch(emailid, "(RFC822)")
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    log += ("%d " % nbNewMailObjects) + str(msg['subject']) + "<br>"
                    case = find_case_for_email(msg['subject'])
                    log += str(case) + "<br>"
                    if case:
                        date = datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate(msg["Date"])))
                        mailObject = Email(date=date,
                                           sender=msg["From"],
                                           to=msg["To"],
                                           cc=msg["cc"],
                                           bcc=msg["bcc"],
                                           subject=msg['subject'],
                                           body=msg.get_payload(),
                                           case=case)
                        mailObject.save()
                        handle_new_mail(case, mailObject)
                        nbNewMailObjects += 1
        m.close()
        m.logout()
        # XXX provide better output and translation of it
        return HttpResponse(log+"<html><body>Read %d mails and attached %d to cases</body></html>" % (len(items), nbNewMailObjects))
    else:
        # XXX provide better output and translation of it
        return HttpResponse("<html><body>Unable to find IMAP user or password</br>Giving up</body></html>")
