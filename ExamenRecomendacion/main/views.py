from django.shortcuts import render
from main.populate import populateDatabase

# Create your views here.
def index(request): 
    return render(request,'index.html')
def populateDB(request):
    populateDatabase() 
    return render(request,'populate.html')

