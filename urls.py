
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from jebif.membership.views import *

urlpatterns = patterns('',
	('^subscription/$', subscription),
	('^subscription/ok$', direct_to_template, {"template": "membership/subscription-ok.html"}),
	('^subscription/(?P<info_id>\d+)/renew/$', subscription_renew),
	('^subscription/(?P<info_id>\d+)/update/$', subscription_update),
	('^subscription/me/update/$', subscription_self_update),
	('^subscription/update/$', subscription_preupdate),
	('^admin/export/csv/$', admin_export_csv),
	('^admin/subscription/$', admin_subscription),
	('^admin/subscription/accept/(?P<info_id>\d+)/$', admin_subscription_accept),
	('^admin/subscription/reject/(?P<info_id>\d+)/$', admin_subscription_reject),
)

