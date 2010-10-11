# -*- coding: utf-8

from django.core.mail import *
from django.shortcuts import *
from django.views.generic.simple import direct_to_template

from django.contrib.auth.decorators import user_passes_test

import codecs
import csv

from membership.models import *
from membership.forms import *

from jebif import settings

import datetime

def subscription( request ) :
	if request.method == 'POST' :
		form = MembershipInfoForm(request.POST)
		if form.is_valid() :
			form.save()

			msg_subj = "Demande d'adhésion"
			msg_txt = """Bonjour,

Une demande d'adhésion vient d'être postée sur le site. Pour la modérer :
	%s
""" % ("http://jebif.fr/%smembership/admin/subscription/" % settings.ROOT_URL)
			mail_managers(msg_subj, msg_txt, fail_silently=True)

			return HttpResponseRedirect("ok")
	else :
		form = MembershipInfoForm()

	return direct_to_template(request, "membership/subscription.html", {"form": form})


def is_admin() :
	def validate( u ) :
		return u.is_authenticated() and u.is_staff
	return user_passes_test(validate)

@is_admin()
def admin_subscription( request ) :
	infos = MembershipInfo.objects.filter(active=False, deleted=False)
	return direct_to_template(request, "membership/admin_subscription.html", {"infos": infos})

@is_admin()
def admin_subscription_accept( request, info_id ) :
	info = MembershipInfo.objects.get(id=info_id)
	info.active = True
	info.inscription_date = datetime.date.today()
	info.save()

	msg_from = "NO-REPLY@jebif.fr"
	msg_to = [info.email]
	msg_subj = "Bienvenue dans l'association JeBiF"
	msg_txt = u"""
Bonjour %s,

Nous avons bien pris en compte ton adhésion à l’association JeBiF. N’hésite pas à nous contacter si tu as des questions, des commentaires, des idées, etc…

Tu connais sans doute déjà notre site internet http://jebif.fr. Tu peux aussi faire un tour sur notre page internationale du RSG-France.
http://www.iscbsc.org/rsg/rsg-france

Tu vas être inscrit à la liste de discussion des membres de l’association. Tu pourras y consulter les archives si tu le souhaites.
http://lists.jebif.fr/mailman/listinfo/membres

A bientôt,
L’équipe du RSG-France (JeBiF)
""" % info.firstname
	send_mail(msg_subj, msg_txt, msg_from, msg_to)

	return HttpResponseRedirect("../../")

@is_admin()
def admin_subscription_reject( request, info_id ) :
	info = MembershipInfo.objects.get(id=info_id)
	info.deleted = True
	info.save()
	return HttpResponseRedirect("../../")

@is_admin()
def admin_export_csv( request ) :
	charset = 'utf-8'
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=membres_jebif.csv'

	writer = csv.writer(response)
	writer.writerow(['Nom', 'Prénom', 'Laboratoire', 'Ville',
		'Pays', 'Poste actuel', 'Motivation', 'Date inscription'])

	infos = MembershipInfo.objects.filter(active=True).order_by('lastname')
	e = lambda s : s.encode(charset)
	for i in infos :
		writer.writerow(map(e, [i.lastname, i.firstname, 
			i.laboratory_name, i.laboratory_city,
			i.laboratory_country, i.position,
			i.motivation.replace("\r\n", " -- "),
			i.inscription_date.isoformat()]))

	return response


