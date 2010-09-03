from django.contrib import admin
from membership.models import *

#class MembershipInline( admin.TabularInline ) :
#	model = Membership

class MembershipInfoAdmin( admin.ModelAdmin ) :
#	inlines = [MembershipInline]
	list_display = ('firstname', 'lastname', 'email', 'user', 'active', 'inscription_date', 'deleted')
	list_filter = ('active', 'deleted')

#admin.site.register(Membership)
admin.site.register(MembershipInfo, MembershipInfoAdmin)

