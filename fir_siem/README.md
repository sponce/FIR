## Install

Follow the generic plugin installation instructions in [the FIR wiki](https://github.com/certsocietegenerale/FIR/wiki/Plugins).
Make sure the following line is included in the `urlpatterns` variable in `fir/urls.py`:

```
url(r'^siem/', include('fir_siem.urls', namespace='siem')),
```

The line should already be there if you've copied the `fir/urls.py.sample` to `fir/urls.py`.

You should also make sure to configure your FIR instance so that it is able to send emails (see `EMAIL_HOST`, `EMAIL_PORT` and `REPLY_TO` in the configuration file) and receive emails (see 'IMAP_USER', 'IMAP_HOST' and 'IMAP_PASSWD').

## Usage

This plugin allows to manage your security events and handle the user interaction via mails.
It defines the notion of SIEMCase that allows to group a set of incidents and a set of mail exchanges with the user into a single entity. It allows to send mails to users and to receive their replies.
It also allows to define plugins handling the grouping of incidents into cases (incomingIncident directory below plugins), when to send mails (sendMail directory below plugins) and when to answer to incoming emails (incomingMail directory below plugins).
The interface of the plugin system is described in details in plugins/__init__.py