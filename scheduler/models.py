from django.db import models

class Location(models.Model):
    location_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

class Technician(models.Model):
    technician_name = models.CharField(max_length=255)

class WorkOrder(models.Model):
    work_order_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    work_order_technician = models.ForeignKey(Technician, on_delete=models.CASCADE, related_name="technician")
    time = models.DateTimeField()
    duration = models.IntegerField()
    price = models.IntegerField()
