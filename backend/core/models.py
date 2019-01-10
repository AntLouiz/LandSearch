import uuid
from django.db import models


class Shapefile(models.Model):
    key = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Shapefile"
        verbose_name_plural = "Shapefiles"

    def __str__(self):
        return self.key


class Coordinates(models.Model):
    key = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    shapefile = models.ForeignKey(
        Shapefile,
        on_delete=models.CASCADE
    )
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        verbose_name = "Coordinates"
        verbose_name_plural = "Coordinates"

    def __str__(self):
        return "Lat: {}, Long: {}".format(
            self.latitude,
            self.longitude
        )


class ScrapingOrder(models.Model):
    key = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    coordinates = models.ForeignKey(
        Coordinates,
        on_delete=models.CASCADE
    )
    is_scraped = models.BooleanField(default=False)
    scraped_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Scraping Order"
        verbose_name_plural = "Scraping Orders"

    def __str__(self):
        return "{}, scraped: {}".format(
            self.key,
            self.is_scraped
        )
