from django.shortcuts import render
from django.http import JsonResponse
from task1.services.scrapper import crawl_and_index, search
base_url = "https://pureportal.coventry.ac.uk/en/organisations/ihw-centre-for-health-and-life-sciences-chls"
index_path = "storage"

def hello_world(request):
    return render(request, 'index.html')

def setup(request):
    response = crawl_and_index(base_url, index_path)
    return JsonResponse(response)

def searchQuery(request):
    query = request.GET.get('query')
    response = search(query, index_path)
    return JsonResponse(response)

