from django.contrib import admin
from membership.models import *

class MembershipInline( admin.TabularInline ) :
	model = Membership
	extra = 0

class MembershipInfoAdmin( admin.ModelAdmin ) :
	inlines = [MembershipInline]
	list_display = ('firstname', 'lastname', 'email', 'user', 'active', 'inscription_date', 'laboratory_city', 'laboratory_cp', 'deleted')
	list_filter = ('active', 'deleted')

admin.site.register(MembershipInfo, MembershipInfoAdmin)

