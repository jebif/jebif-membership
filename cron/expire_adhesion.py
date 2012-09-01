#!/usr/bin/env python
# -*- coding: utf-8

import datetime

ALERT_1 = datetime.timedelta(30)
ALERT_2 = datetime.timedelta(2)

import subprocess

from django.conf import settings
from django.core.mail import send_mail

from jebif.membership.models import *

expired = []
expire = []

for info in MembershipInfo.objects.filter(active=True) :
	m = info.latter_membership()
	if m.has_expired() :
		expired.append(m)
	elif m.expire_delta() in [ALERT_1, ALERT_2] :
		expire.append(m)

for m in expired :
	try :
		subprocess.call(["/usr/lib/mailman/bin/remove_members", "Membres", m.info.email])
	except :
		pass
	m.info.active = False
	m.info.save()

	data = m.info.get_contact_data()

	msg_from = "NO-REPLY@jebif.fr"
	msg_to = [m.info.email]
	msg_subj = u"Expiration de ton adhésion à JeBiF"
	msg_txt = u"""
Bonjour %(firstname)s,

Ton adhésion à l'association JeBiF *vient de se terminer*.
Tu peux la renouveller pour un an, gratuitement, en te rendant sur
	%(url_renew)s
avec ton identifiant '%(login)s'%(passwd_setup)s.

En espérant te revoir très bientôt,
L’équipe du RSG-France (JeBiF)
""" % data
	send_mail(msg_subj, msg_txt, msg_from, msg_to)

for m in expire :
	data = m.info.get_contact_data()
	data["expire_date"] = m.date_end.strftime(settings.DATE_INPUT_FORMAT)

	msg_from = "NO-REPLY@jebif.fr"
	msg_to = [m.info.email]
	msg_subj = u"Expiration de ton adhésion à JeBiF"
	msg_txt = u"""
Bonjour %(firstname)s,

Ton adhésion à l'association JeBiF se termine le *%(expire_date)s*.
Tu peux la renouveller pour un an, gratuitement, en te rendant sur
	%(url_renew)s
avec ton identifiant '%(login)s'%(passwd_setup)s.

À bientôt,
L’équipe du RSG-France (JeBiF)
""" % data
	send_mail(msg_subj, msg_txt, msg_from, msg_to)


