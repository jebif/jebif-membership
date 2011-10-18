
from django.db import connection
from django.db.transaction import commit_on_success
import django.core.management

from jebif.membership.models import *

def syncdb() :
	django.core.management.call_command("syncdb")

def upgrade_2() :
	unique_field(MembershipInfo, "email")

def upgrade_1() :
	for info in MembershipInfo.objects.filter(active=True) :
		if info.membership_set.count() == 0 :
			m = Membership(info=info)
			m.date_begin = info.inscription_date
			m.date_end = end_membership(m.date_begin)
			m.save()

def unique_field( model, field_name ) :
	sqls = []
	field = [f for f in model._meta.fields if f.name == field_name][0]
	qn = connection.ops.quota_name
	db_table = model._meta.db_table
	if connection.vendor != "sqlite" :
		cursor = connection.cursor()
		cursor.execute("ALTER TABLE %s ADD CONSTRAINT UNIQUE (%s)" % (qn(db_table),
			qn(field.column))
		cursor.close()

@commit_on_success
def run() :
	info = DatabaseInfo.instance()
	if info.version < VERSION :
		for i in range(info.version+1, VERSION+1) :
			globals()["upgrade_%d"%i]()
			info.version = VERSION
			info.save()

if __name__ == "__main__" :
	run()


