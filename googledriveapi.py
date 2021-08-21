from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

g_auth = GoogleAuth()
g_auth.LocalWebserverAuth()  # starts browser and asks for authentication
drive = GoogleDrive(g_auth)  # create a google drive object to handle file, used to list and create file

# view files/folders in drive
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file in file_list:
    print('Title: %s, ID: %s' % (file['title'], file[id]))
    # get folder ID to upload to
    if file['title'] == "Key Logs":
        fileID = file['id']

file1 = drive.CreateFile({"mimeType": "text/csv", "parents": [{"kind": "drive#fileLink", "id": fileID}]})  # initialize a google drive file
file1.SetContentFile("small_file.csv")
file1.Upload()
print('Created file %s with mimeType %s' %(file1['title'], file1['mimeType']))


