import zipfile


def check_uploaded_file(file):
    extension_to_check = 'shp'
    try:
        file_extension = file.name.lower().split('.')[1]
    except:
        file_extension = None

    if file_extension == extension_to_check:
        return True

    return False
