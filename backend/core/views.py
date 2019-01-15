from django.http import HttpResponseRedirect
from django.shortcuts import render
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from .models import Shapefile, Coordinates, ScrapingOrder
from .utils import check_uploaded_file, check_coordinates
from .forms import OrderForm


gauth = GoogleAuth()

gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)


def upload_file(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST, request.FILES)
        if order_form.is_valid():
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']

            if not check_coordinates(latitude, longitude):
                return HttpResponseRedirect('/')

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
                    latitude=request.POST['latitude'],
                    longitude=request.POST['longitude'],
                    shapefile=shapefile
                )

                ScrapingOrder.objects.create(
                    coordinates=coordinates
                )

                return HttpResponseRedirect('/')

    else:
        order_form = OrderForm()

    context = {
        'form': order_form
    }
    return render(request, 'core/index.html', context)
