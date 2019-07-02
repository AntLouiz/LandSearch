from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def auth_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    return drive
