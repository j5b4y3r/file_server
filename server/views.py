from django.shortcuts import render
from django.http import HttpResponse
import os, time, json
from . import tests


def get_data(requested_path= os.path.expanduser( '~' ), file=None):
    fobject = []
    if os.path.exists(requested_path):  
        tests.list_files_and_folders(requested_path, fobject) 
    return fobject

def home(request):
    return render(request, 'home.html', {'data': get_data()})

def download_file(request, file_path):
    print("Downloaded in " + file_path)
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as fh:
            file_data = fh.read()
            response = HttpResponse(file_data, content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            print(response)
            return response
    else:
        return HttpResponse("File not found")

def send_ff(request, path):
    check = path.split("/")
    if check[0] == "download":
        return download_file(request, path[9:])

    if path == 'home' or "":
        return render(request, 'home.html', {'data': get_data()})
    return render(request, 'home.html', {'data': get_data(path)})


