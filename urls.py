
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from membership.views import *

urlpatterns = patterns('',
	('^subscription/$', subscription),
	('^subscription/ok$', direct_to_template, {"template": "membership/subscription-ok.html"}),
)

