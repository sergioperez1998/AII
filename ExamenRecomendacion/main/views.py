import shelve
from django.shortcuts import render
from main.populate import populateDatabase
from main.models import UserInformation, Book, Rating
from main.forms import UserForm, BookForm
from django.shortcuts import render, get_object_or_404
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, topMatches

# Create your views here.
def index(request): 
    return render(request,'index.html')
def populateDB(request):
    populateDatabase() 
    return render(request,'populate.html')

def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all() 
    for ra in ratings:
        user = int(ra.user.id)
        itemid = int(ra.book.id)
        rating = float(ra.rating)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()

#Apartado A
def apartadoA(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(UserInformation, pk=idUser)
            return render(request,'ratedBooks.html', {'usuario':user})
    form=UserForm()
    return render(request,'search_user.html', {'form':form })

#Apartado C
def similarBooks(request):
    book = None
    if request.method=='GET':
        form = BookForm(request.GET, request.FILES)
        if form.is_valid():
            idBook = form.cleaned_data['id']
            book = get_object_or_404(Book, pk=idBook)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idBook),n=2)
            books = []
            similar = []
            for re in recommended:
                books.append(Book.objects.get(pk=re[1]))
                similar.append(re[0])
            items= zip(books,similar)
            return render(request,'similarBooks.html', {'book': book,'books': items})
    form = BookForm()
    return render(request,'search_book.html', {'form': form})

#Apartado D
def recommendedBooksUser(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(UserInformation, pk=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idUser))
            recommended = rankings[:2]
            books = []
            scores = []
            for re in recommended:
                books.append(Book.objects.get(pk=re[1]))
                scores.append(re[0])
            items= zip(books,scores)
            return render(request,'recommendationItems.html', {'user': user, 'items': items})
    form = UserForm()
    return render(request,'search_user.html', {'form': form})