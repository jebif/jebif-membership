# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.contrib.auth.models import User

VERSION = 1

class MembershipInfo( models.Model ) :
	user = models.ForeignKey(User, blank=True, null=True)
	email = models.EmailField()
	firstname = models.CharField("Prénom", max_length=75)
	lastname = models.CharField("Nom", max_length=75)
	laboratory_name = models.CharField("Laboratoire", max_length=75)
	laboratory_city = models.CharField("Ville", max_length=75)
	laboratory_country = models.CharField("Pays", max_length=75)
	position = models.CharField("Poste actuel", max_length=75)
	motivation = models.TextField("Motivation pour adhérer", blank=True)

	inscription_date = models.DateField(default=datetime.date.today)
	active = models.BooleanField(default=False)
	deleted = models.BooleanField(default=False)

	def __unicode__( self ) :
		return "%s %s <%s>%s" % (self.firstname, self.lastname,
								self.email, "" if self.active else " (inactive)")

def end_membership(base=None) :
	d = base
	if d is None :
		d = datetime.date.today()
	try :
		return datetime.date(d.year+1,d.month,d.day)
	except ValueError :
		return datetime.date(d.year+1,d.month,d.day-1)


class Membership( models.Model ) :
	info = models.ForeignKey(MembershipInfo)
	date_begin = models.DateField(default=datetime.date.today)
	date_end = models.DateField(default=end_membership)

	@classmethod
	def current_objects( celf ) :
		today = datetime.date.today
		return celf.objects.filter(info__active=True,
					date_begin__lte=today, date_end__gt=today)

	def __unicode__( self ) :
		return "%s/%s %s" % (self.date_begin, self.date_end, self.info)


class DatabaseInfo( models.Model ) : 
	""" 
	Version de la structure de la base de données.
	Utilisé pour migrer les données.
	"""
	version = models.SmallIntegerField()

	@classmethod
	def instance( celf ) : 
		try :
			return celf.objects.all()[0]
		except IndexError :
			celf.objects.create(version=0)
			return celf.objects.all()[0]

