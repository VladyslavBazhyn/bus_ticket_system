from django.contrib import admin
from station.models import Buss, Ticket, Trip, Facility, Order


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInline, )


admin.site.register(Buss)

admin.site.register(Ticket)

admin.site.register(Trip)

admin.site.register(Facility)

admin.site.register(Order, OrderAdmin)
