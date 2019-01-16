from django.contrib import admin
from .models import (
    Shapefile,
    Coordinates,
    Raster,
    ScrapingOrder
)


admin.site.register(Shapefile)
admin.site.register(Coordinates)
admin.site.register(ScrapingOrder)
admin.site.register(Raster)
