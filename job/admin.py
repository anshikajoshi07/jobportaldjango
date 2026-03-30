from django.contrib import admin
from .models import StuUser
from .models import recuraterUser
from .models import DashboardJob
from .models import applicatioForm
# Register your models here.


admin.site.register(StuUser)
admin.site.register(recuraterUser)
admin.site.register(DashboardJob)
admin.site.register(applicatioForm)

