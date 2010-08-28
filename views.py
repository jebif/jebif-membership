
from django.shortcuts import *
from django.views.generic.simple import direct_to_template

from membership.forms import *

def subscription( request ) :
	if request.method == 'POST' :
		form = MembershipInfoForm(request.POST)
		if form.is_valid() :
			form.save()
			return HttpResponseRedirect("ok")
	else :
		form = MembershipInfoForm()
	return direct_to_template(request, "membership/subscription.html", {"form": form})


