# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.contrib.auth.models import User

#def end_membership() :
#	return datetime.date.today() + datetime.timedelta(365)


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
	active = models.BooleanField(default=True)

#	def latter_membership( self ) :
#		ms = self.membership_set
#		if ms.count() == 0 :
#			return None
#		else :
#			return ms.order_by('-date_begin')[0]

	def __unicode__( self ) :
		return "%s %s <%s>%s" % (self.firstname, self.lastname,
								self.email, "" if self.active else " (inactive)")

#class Membership( models.Model ) :
#	date_begin = models.DateField() #default=datetime.date.today)
#	date_end = models.DateField() #default=end_membership)
#	info = models.ForeignKey(MembershipInfo, unique=True)

#	def __unicode__( self ) :
#		return "%s/%s %s" % (self.date_begin, self.date_end,
#								self.info)
	

	


