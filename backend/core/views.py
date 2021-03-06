from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy as r
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.core import serializers
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from .models import (
    Shapefile,
    Coordinates,
    ScrapingOrder,
    Raster
)
from .utils import check_uploaded_file
from .forms import OrderForm
from backend.spider.tasks import crawl_order

gauth = GoogleAuth()

gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)


class HomeView(TemplateView):
    template_name = "core/home.html"


def upload_file(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST, request.FILES)
        if order_form.is_valid():
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']

            uploaded_file = request.FILES['file'].temporary_file_path()
            uploaded_filename = request.FILES['file'].name

            if check_uploaded_file(request.FILES['file']):
                f_list = drive.ListFile({
                    'q': "'root' in parents and trashed=false"
                }).GetList()
                folder_id = None
                for f in f_list:
                    if f['title'] == 'shapefiles':
                        folder_id = f['id']

                file = drive.CreateFile({
                    'parents': [{
                        'kind': "drive#fileLink",
                        'id': folder_id
                    }],
                    'title': uploaded_filename
                })

                file.SetContentFile(uploaded_file)
                file.Upload()

                shapefile = Shapefile.objects.create(
                    key=file['id']
                )

                coordinates = Coordinates.objects.create(
                    title=request.POST['title'],
                    latitude=request.POST['latitude'],
                    longitude=request.POST['longitude'],
                    shapefile=shapefile
                )

                order = ScrapingOrder.objects.create(
                    coordinates=coordinates,
                    raster=Raster.objects.create()
                )

                order = serializers.serialize("json", [order])
                crawl_order.delay(order)

                messages.success(
                    request,
                    'The order {} added successfull.'.format(
                        request.POST['title']
                    )
                )
                return HttpResponseRedirect(r('core:orders'))
        else:
            context = {'form': order_form}
            return render(request, 'core/new_order.html', context)
    else:
        order_form = OrderForm()

    context = {
        'form': order_form
    }
    return render(request, 'core/new_order.html', context)


class OrdersListView(ListView):

    template_name = 'core/orders.html'
    model = ScrapingOrder
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = ScrapingOrder.objects.filter(is_active=True).all()

        context['orders'] = orders

        return context


class OrderDeleteView(DeleteView):
    model = ScrapingOrder
    template_name = 'core/order_confirm_delete.html'
    success_url = r('core:orders')

    def delete(self, request, *args, **kwargs):
        success_url = self.success_url
        self.object = self.get_object()
        shapefile_id = self.object.coordinates.shapefile.key
        raster = self.object.raster

        shapefile = drive.CreateFile({'id': shapefile_id})
        shapefile.Trash()

        if raster:
            raster_file = drive.CreateFile({'id': raster.file_id})
            raster_file.Trash()

        self.object.disable()

        return HttpResponseRedirect(success_url)
