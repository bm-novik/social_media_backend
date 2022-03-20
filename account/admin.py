from django.contrib import admin

from account.models import Country, City, Profile

admin.site.register(City)
admin.site.register(Country)
admin.site.register(Profile)