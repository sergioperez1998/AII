import shelve
from django.shortcuts import render
from main.populate import populateDatabase
from main.models import Usuario, Libro, Puntuacion
from main.forms import UserForm, BookForm
from django.shortcuts import render, get_object_or_404
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, topMatches
from django.db.models.aggregates import Avg

# Create your views here.
def index(request): 
    return render(request,'index.html')
def populateDB(request):
    populateDatabase() 
    return render(request,'populate.html')


def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Puntuacion.objects.all() 
    for ra in ratings:
        user = int(ra.idUsuario.id)
        itemid = int(ra.bookId.id)
        rating = float(ra.puntuacion)
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
            idUsuario = form.cleaned_data['id']
            user = get_object_or_404(Usuario, pk=idUsuario)
            return render(request,'ratedBooks.html', {'usuario':user})
    form=UserForm()
    return render(request,'search_user.html', {'form':form })

#Apartado A
def apartadoB(request):
    
    libros=[]
    mejoresPuntuaciones=Puntuacion.objects.all().aggregate(avg_rating = Avg('puntuacion')).order_by('-avg_rating')[:3]
    for p in mejoresPuntuaciones:
        idLibro = p.bookId
        libro = get_object_or_404(Libro, bookId=idLibro)
        libros.append(libro)
    return render(request,'librosMejorPuntuacion.html',{"mejoresLibros":libros})

#Apartado C
def similarBooks(request):
    book = None
    if request.method=='GET':
        form = BookForm(request.GET, request.FILES)
        if form.is_valid():
            idBook = form.cleaned_data['id']
            book = get_object_or_404(Libro, pk=idBook)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idBook),n=2)
            books = []
            similar = []
            for re in recommended:
                books.append(Libro.objects.get(pk=re[1]))
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
            user = get_object_or_404(Usuario, pk=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idUser))
            recommended = rankings[:2]
            books = []
            scores = []
            for re in recommended:
                books.append(Libro.objects.get(pk=re[1]))
                scores.append(re[0])
            items= zip(books,scores)
            return render(request,'recommendationItems.html', {'user': user, 'items': items})
    form = UserForm()
    return render(request,'search_user.html', {'form': form})

