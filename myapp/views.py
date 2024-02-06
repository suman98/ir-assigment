from django.shortcuts import render
from django.http import JsonResponse
from myapp.services.scrapper import crawl_and_index, search
base_url = "https://pureportal.coventry.ac.uk/en/organisations/centre-for-health-and-life-sciences"
index_path = "storage"

def hello_world(request):
    return render(request, 'index.html')

def setup(request):
    response = crawl_and_index(base_url, index_path)
    return JsonResponse(response)

def searchQuery(request):
    query = request.GET.get('query')
    print(query)
    query = 'Barriers'
    response = search(query, index_path)
    print(response)
    return JsonResponse(response)