import csv
from datetime import datetime
from django.shortcuts import render
from terrier.settings import BASE_DIR
from datetime import datetime, timedelta
from .models import Location, Technician, WorkOrder


def time_in_range(start, end, x):
    if start <= end:
        return start <= x < end
    else:
        return start <= x or x <= end


def daterange(start_date, end_date):
    delta = timedelta(hours=1)
    while start_date < end_date:
        yield start_date
        start_date += delta


def home_view(request):
    load_csvs()
    work_orders = WorkOrder.objects.all()
    time_list = []

    # Use any year to generate hh:mm times for the day, in the format 00, 01, 02, ..., 23 
    start_date = datetime(2013, 1, 1, 00, 00)
    end_date = datetime(2013, 1, 1, 23, 59)
    time_list = [single_date.strftime(
        "%H:%M") for single_date in daterange(start_date, end_date)]

    # Create an object (to be passed to the home template), which'll hold the scheduling grid
    # # It'll have a format {
    #   hour: {technician1: '', technician2: '', ....}
    # } 
    # Initializing all technician values to empty string 
    scheduling_obj = {}
    for i in range(len(time_list)):
        technicians = {}
        for technician in Technician.objects.all():
            technicians[technician.pk] = ''

        scheduling_obj[i] = technicians

    # Loop through the time list, technicians, and workorders to find times where a technicians
    # workorder is within the range of any two time_list values. If it is found to be in range, 
    # use the iterating index (i) and technician id to update the scheduling_obj dictionary to X.
    for i in range(len(time_list)):
        for technician in Technician.objects.all():
            technician_orders = work_orders.filter(
                work_order_technician=technician)
            for order in technician_orders:
                if i + 1 < len(time_list):
                    if time_in_range(time_list[i], time_list[i+1], datetime.strftime(order.time, "%H:%M")):
                        scheduling_obj[i][technician.pk] = 'X'

    context = {
        "work_orders": work_orders,
        "technicians": Technician.objects.all(),
        "scheduling_obj": scheduling_obj
    }

    return render(request, template_name="home.html", context=context)


def load_csvs():
    locations_file = BASE_DIR / 'scheduler' / 'csvs' / 'locations.csv'
    technicians_file = BASE_DIR / 'scheduler' / 'csvs' / 'technicians.csv'
    work_orders_file = BASE_DIR / 'scheduler' / 'csvs' / 'work_orders.csv'

    with open(locations_file) as csv_locations:
        csvreader = csv.reader(csv_locations)
        _ = next(csvreader)

        for row in csvreader:
            _, created = Location.objects.get_or_create(
                location_name=row[1],
                city=row[2]
            )

            if created:
                print(
                    "{} - {} inserted to the database".format(row[1], row[2]))

    with open(technicians_file) as csv_technicians:
        csvreader = csv.reader(csv_technicians)
        _ = next(csvreader)

        for row in csvreader:
            _, created = Technician.objects.get_or_create(
                technician_name=row[1],
            )

            if created:
                print("{} inserted to the database".format(row[1]))

    with open(work_orders_file) as csv_work:
        csvreader = csv.reader(csv_work)
        _ = next(csvreader)
        locations = Location.objects.all()
        technicians = Technician.objects.all()

        for row in csvreader:
            technician = technicians[int(row[1]) - 1]
            location = locations[int(row[2]) - 1]
            row[3] = row[3][:5] + "20" + row[3][5:]
            original_datetime = datetime.strptime(row[3], "%m/%d/%Y %H:%M")
            converted_date_time = datetime.strftime(
                original_datetime, "%Y-%m-%d %H:%M")

            _, created = WorkOrder.objects.get_or_create(
                work_order_location=location,
                work_order_technician=technician,
                time=converted_date_time,
                duration=row[4],
                price=row[5]
            )

            if created:
                print("Work order created for {} at {}".format(
                    technician.technician_name, row[3]))
