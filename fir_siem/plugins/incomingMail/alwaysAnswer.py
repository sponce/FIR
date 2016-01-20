def answer_mail(case, email):
    '''answers to incoming mail whatever happens, thanking the user'''
    return [('uniqueMailTemplate',
             {'sender' : 'sebastien.ponce@cern.ch',
              'to' : email.sender,
              'subject' : 'Re:%s' % email.subject,
              'body' : 'Thank you for having taken action'})]
