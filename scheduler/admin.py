from django.contrib import admin
from .models import Technician, Location, WorkOrder

admin.site.register(Technician)
admin.site.register(Location)
admin.site.register(WorkOrder)