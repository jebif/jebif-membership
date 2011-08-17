#!/usr/bin/env python
# -*- coding: utf-8

import datetime

ALERT_1 = datetime.timedelta(30)
ALERT_2 = datetime.timedelta(2)

import subprocess

from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from jebif.membership.models import *
from jebif.membership.views import subscription_renew

expired = []
expire = []
expire = []

for info in MembershipInfo.objects.filter(active=True) :
	m = info.latter_membership()
	if info.email == "loic.pauleve@irccyn.ec-nantes.fr" :
		expired.append(m)
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

for m in expire :
	url_renew = reverse(subscription_renew, kwargs={"info_id": m.info.id})
	url_renew = "/%s%s" % (settings.ROOT_URL, url_renew[1:])
	new_passwd = m.info.make_user()

	data = {
		"firstname" : m.info.firstname,
		"expire_date" : m.date_end.strftime(settings.DATE_INPUT_FORMAT),
		"url_renew" : "%s%s" % (settings.HTTP_DOMAIN, url_renew),
		"login" : m.info.user.username,
		"passwd_setup" : "",
	}
	if new_passwd is not None :
		data["passwd_setup"] = " et ton mot de passe '%s'" % new_passwd

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


