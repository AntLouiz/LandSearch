import zipfile


def check_uploaded_file(file):
    files_extensions = ['dbf', 'prj', 'qpj', 'shp', 'shx']
    try:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            for filename in zip_ref.namelist():
                if filename.split('.')[1] not in files_extensions:
                    return False

    except zipfile.BadZipFile:
        return False

    return True


def check_coordinates(latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)

    if not (latitude >= -180 and latitude <= 180):
        return False

    if not (longitude >= -90 and longitude <= 90):
        return False

    return True
