# list all available "plugins" for
#  - finding cases related to an incoming incident
#      + these plugins are located in directory plugins/incomingIncident
#      + there main function has the following signature :
#          find_cases(incident)
#        and returns a set of cases
#      + all functions of all plugins will be called and the results merged
#  - deciding whether to send a mail after arrival of a new incident
#      + these plugins are located in directory plugins/sendMail
#      + there main function has the following signature :
#          send_mail(case, incident)
#        and returns a list of tuple (template, dict) giving the template
#        to be used and a dictionnary of parameters
#      + all functions of all plugins will be called and the results merged
#  - reacting to an incoming mail
#      + these plugins are located in directory plugins/incomingMail
#      + there main function has the following signature :
#          answer_mail(case, mail)
#        and returns a set of tuple (template, dict) giving the mail template
#        to be used for replying by mail and a dictionnary of parameters
#      + all functions of all plugins will be called and the results merged
#
# Note that plugins are loaded in alphabetical order if it matters

import os, importlib

def loadPlugins(folder, function_name):
    '''Generic function loading all python files in the given folder
       and checking that they contain the given function.
       Returns the list of loaded modules'''
    modules = []
    possibleplugins = os.listdir(os.path.join('fir_siem', 'plugins', folder))
    for plugin_file in possibleplugins:
        module_name, ext = os.path.splitext(plugin_file)
        if ext != '.py' and not module_name.startswith('.'):
            continue
        full_module_name = '.'.join(['fir_siem', 'plugins', folder, module_name])
        print 'Loading plugin %s' % full_module_name
        module = importlib.import_module(full_module_name)
        try:
            getattr(module, function_name)
        except AttributeError:
            print 'Unloaded plugin %s as it does not contain a %s function' % (full_module_name, function_name)
            del module
        else:
            modules.append(module)
    return modules

# load incomingIncident plugins
incoming_incidents_plugins = loadPlugins('incomingIncident', 'find_cases')

# load sendMail plugins
send_mail_plugins = loadPlugins('sendMail', 'send_mail')

# load incomingMail plugins
incoming_mail_plugins = loadPlugins('incomingMail', 'answer_mail')
