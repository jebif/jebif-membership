
from django.forms import ModelForm

import membership.models

class MembershipInfoForm( ModelForm ) :
	class Meta :
		model = membership.models.MembershipInfo
		fields = ("firstname", "lastname", "email", 
						"laboratory_name", "laboratory_city", "laboratory_country",
						"position", "motivation")


