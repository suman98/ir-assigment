from django.shortcuts import render
from django.http import JsonResponse
from myapp.services.prediction import assign_to_cluster
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


def predictIndex(request):
    # new_document = "The company launched a new product line."
    # cluster = assign_to_cluster(new_document)
    # print("The new document belongs to cluster:", cluster)
    return render(request, 'predict.html')

def predictCategory(request):
    query = request.GET.get('query')
    cluster = assign_to_cluster(query)
    return JsonResponse({
        "result": cluster
    })
