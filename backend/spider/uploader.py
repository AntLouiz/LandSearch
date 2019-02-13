from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from .config import temp_dir
from .decompressor import decompress_zip_file
from backend.core.models import Raster


gauth = GoogleAuth()

gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)


def upload_file(filename, file_path, order):
    f_list = drive.ListFile({
        'q': "'root' in parents and trashed=false"
    }).GetList()
    folder_id = [f['id'] for f in f_list if f['title'] == 'rasters'][0]

    file = drive.CreateFile({
        'parents': [{
            'kind': "drive#fileLink",
            'id': folder_id
        }],
        'title': filename
    })

    file.SetContentFile(file_path)
    file.Upload()

    file.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'
    })

    order.raster.file_id = file['id']
    order.raster.thumbnail_link = file['thumbnailLink']
    order.raster.download_link = file['webContentLink']
    order.raster.download_date = datetime.now()
    order.raster.is_active = True

    order.raster.save()


def get_folder_id(parent, folder_id='root'):
    f_list = get_folder_files(folder_id)
    folder_id = [f['id'] for f in f_list if f['title'] == parent][0]
    return folder_id


def get_folder_files(folder_id='root'):
    f_list = drive.ListFile({
        'q': "'{}' in parents and trashed=false".format(
            folder_id
        )
    }).GetList()
    return f_list


def get_shapefile(file_id, output_dir):
    folder_id = get_folder_id('shapefiles')
    shapefiles = get_folder_files(folder_id)

    if not len(shapefiles):
        raise Exception('No shapefiles founded.')

    for shp in shapefiles:
        shp_id = shp['id']

        if shp_id == file_id:
            file_ext = shp['fileExtension']
            file_path = "{}/{}.{}".format(
                output_dir,
                shp_id,
                file_ext
            )
            shapefile = drive.CreateFile({'id': shp_id})

            shapefile.GetContentFile(file_path)

            decompress_zip_file(
                file_path,
                output_dir
            )
