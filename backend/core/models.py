import uuid
from django.db import models


class Shapefile(models.Model):
    key = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Shapefile"
        verbose_name_plural = "Shapefiles"

    def disable(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.key


class Raster(models.Model):
    key = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    thumbnail_link = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    download_link = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    acquisition_date = models.DateField(
        blank=True,
        null=True,
        auto_now_add=False
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Raster"
        verbose_name_plural = "Rasters"

    def disable(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return "{}".format(self.key)


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
    title = models.CharField(max_length=100)
    description = models.TextField(
        max_length=200,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Coordinates"
        verbose_name_plural = "Coordinates"

    def disable(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return "{}, Lat: {}, Long: {}".format(
            self.title,
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

    raster = models.ForeignKey(
        Raster,
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(default=True)

    choices = (
        ('Waiting', 'waiting'),
        ('Executing', 'executing'),
        ('Finished', 'finished'),
        ('No result', 'no_result')
    )

    status = models.CharField(
        max_length=100,
        choices=choices,
        default=choices[0][1]
    )
    scraped_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Scraping Order"
        verbose_name_plural = "Scraping Orders"

    def disable(self):
        self.is_active = False
        if self.raster:
            self.raster.disable()

        self.coordinates.disable()
        self.coordinates.shapefile.disable()
        self.save()

    def __str__(self):
        return "{}, Status: {}".format(
            self.key,
            self.status
        )
