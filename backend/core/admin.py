from django.contrib import admin
from .models import Shapefile, Coordinates, ScrapingOrder


admin.site.register(Shapefile)
admin.site.register(Coordinates)
admin.site.register(ScrapingOrder)
