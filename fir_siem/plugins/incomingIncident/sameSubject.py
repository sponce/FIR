from fir_siem.models import SIEMCase

def find_cases(incident):
    '''Find cases having another incident with identical subject'''
    return set(SIEMCase.objects.filter(related_incidents__subject__iexact=incident.subject)[:])
