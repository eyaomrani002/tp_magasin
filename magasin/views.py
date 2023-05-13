from django.http import HttpResponse, HttpResponseRedirect
from . models import Produit,Commande,Fournisseur,Categorie
from .forms import ProduitForm,CommandeForm,CategorieForm
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProduitForm,UserCreationForm,FournisseurForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render


from rest_framework.views import APIView
from rest_framework.response import Response
from magasin.serializers import CategorySerializer,ProduitSerializer

from rest_framework import viewsets

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail


class ProductViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = ProduitSerializer

    def get_queryset(self):
        queryset = Produit.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset



class CategoryAPIView(APIView):
 
    def get(self, *args, **kwargs):
        categories = Categorie.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProduitAPIView(APIView):
    def get(self, *args, **kwargs):
        produits = Produit.objects.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)

@login_required
def index(request):
    if request.user.is_authenticated:
        request.session['username'] = request.user.username
    return render(request, 'index.html')

def index(request):
    list=Produit.objects.all()
    return render(request,'magasin/vitrine.html',{'list':list})
def register(request):
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
            return redirect('home')
    else :
        form = UserCreationForm()
    return render(request,'registration/register.html',{'form' : form})

def home(request):
    context={'val':"Menu Acceuil"}
    return render (request,'home.html',context)
def nouveau_produit(request):
 if request.method == "POST" :
    form = ProduitForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse('/magasin')
 else :
        form = ProduitForm() #créer formulaire vide
 return render(request,'magasin/majProduits.html',{'form':form})


def indexA(request):
     return render(request,'magasin/indexA.html' )


# vue pour modifier un produit existant
def modifier_produit(request, pk):
    produit = get_object_or_404(Produit,pk=pk)

    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProduitForm(instance=produit)

    return render(request,'magasin/majProduits.html', {'form': form})

# vue pour supprimer un produit existant
def supprimer_produit(request,pk):
    produit = get_object_or_404(Produit, pk=pk)

    if request.method == "POST":
        produit.delete()
        return redirect('index')

    return render(request, 'magasin/supprimerProduit.html', {'produit': produit})

def  nouveauFournisseur(request):
    if request.method == "POST" :
        form = FournisseurForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else :
        form = FournisseurForm() #créer formulaire vide
    return render(request,'magasin/fournisseur.html',{'form':form})


def search(request):
    query = request.GET.get('q')
    if query:
        try:
            # Essayez de convertir la chaîne de requête en float pour la recherche par prix
            query = float(query)
            produits = Produit.objects.filter(prix=query)
        except ValueError:
            # Si la conversion en float échoue, recherchez par libellé, type ou catégorie
            produits = Produit.objects.filter(Q(type__icontains=query) )
        context = {'query': query, 'produits': produits}
        return render(request, 'magasin/search_results.html', context)
    else:
        return render(request, 'magasin/search_results.html')
   
def product_detail(request, pk):
    product = get_object_or_404(Produit, pk=pk)
    return render(request, 'magasin/detail_product.html', {'product': product})



#commande
def create_commande(request):
       if request.method == "POST" :
         form = CommandeForm(request.POST)
         if form.is_valid():
              form.save() 
              commandes=Commande.objects.all()
              
              return render(request,'magasin/Commandes/mesCommandes.html',{'commandes':commandes})
       else : 
            form = CommandeForm() #créer formulaire vide 
            commandes=Commande.objects.all()
            return render(request,'magasin/Commandes/create_commande.html',{'form':form,'commandes':commandes})

def edit_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('ListCommande')
    else:
        form = CommandeForm(instance=commande)
    return render(request, 'magasin/Commandes/edit_commande.html', {'form': form})

def delete_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        commande.delete()
        return redirect('ListCommande')
    return render(request, 'magasin/Commandes/delete_commande.html', {'commande': commande})

def detail_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    context = {'commande': commande}
    return render(request, 'magasin/Commandes/detail_commande.html', context)

def ListCommande(request):
        commandes= Commande.objects.all()
        context={'commandes':commandes}
        return render( request,'magasin/Commandes/mesCommandes.html',context )

from django.shortcuts import redirect, render, get_object_or_404


#fournisseur

def ListFournisseur(request):
    fournisseurs = Fournisseur.objects.all()
    context = {'fournisseurs': fournisseurs}
    return render(request, 'magasin/Fournisseurs/mesFournisseurs.html', context)

def nouveauFournisseur(request):
    if request.method == "POST" :
         form = FournisseurForm(request.POST,request.FILES)
         if form.is_valid():
               # Récupérer l'instance du modèle produit
            frns = form.save(commit=False)
            # Récupérer la nouvelle image téléchargée
            nouvelle_image = form.cleaned_data['logo']
            # Si une nouvelle image a été téléchargée, la sauvegarder
            if nouvelle_image:
                frns.logo= nouvelle_image
            # Sauvegarder le produit
            form.save() 
            fournisseurs=Fournisseur.objects.all()
            return render(request,'magasin/Fournisseurs/mesFournisseurs.html',{'fournisseurs':fournisseurs})
    else : 
            form = FournisseurForm() #créer formulaire vide 
            fournisseurs=Fournisseur.objects.all()
            return render(request,'magasin/Fournisseurs/create_For.html',{'form':form,'fournisseurs':fournisseurs})

"""def Fournisseur_index(request):
    fournisseurs = Fournisseur.objects.all()
    context = {'fournisseurs': fournisseurs}
    return render(request, 'magasin/mesFournisseurs.html', context)
    if request.method == "POST" :
        form = FournisseurForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else :
        form = FournisseurForm() #créer formulaire vide
    return render(request,'magasin/mesFournisseurs.html',{'form':form})"""
def edit_Fournisseur(request, fk):
    fournisseur = get_object_or_404(Fournisseur, id=fk)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, request.FILES, instance=fournisseur)
        if form.is_valid():
            # Récupérer l'instance du modèle produit
            frns = form.save(commit=False)
            # Récupérer la nouvelle image téléchargée
            nouvelle_image = form.cleaned_data['logo']
            # Si une nouvelle image a été téléchargée, la sauvegarder
            if nouvelle_image:
                frns.logo= nouvelle_image
            # Sauvegarder le produit
            frns.save()
            return redirect('fournisseurs')
    else:
        form = FournisseurForm(instance=fournisseur)
        return render(request, 'magasin/Fournisseurs/edit_For.html', {'form': form})

def delete_Fournisseur(request, fk):
    fournisseur = get_object_or_404(Fournisseur, id=fk)
    if request.method == 'POST':
        fournisseur.delete()
        return redirect('fournisseurs')
    return render(request,'magasin/Fournisseurs/delete_For.html', {'fournisseur': fournisseur})

def detail_Fournisseur(request, for_id):
    fournisseur = get_object_or_404(Fournisseur, id=for_id)
    context = {'fournisseur': fournisseur}
    return render(request, 'magasin/Fournisseurs/detail_For.html', context)



#categorie

def create_categorie(request):
       if request.method == "POST" :
         form = CategorieForm(request.POST)
         if form.is_valid():
              form.save() 
              categories=Categorie.objects.all()
              
              return render(request,'magasin/Categories/mesCategories.html',{'categories':categories})
       else : 
            form = CategorieForm() #créer formulaire vide 
            categories=Categorie.objects.all()
            return render(request,'magasin/Categories/create_categorie.html',{'form':form,'categories':categories})

def edit_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            categorie.save()
            return redirect('ListCategorie')
    else:
        form = CategorieForm(instance=categorie)
        return render(request, 'magasin/Categories/edit_categorie.html', {'form': form})

def delete_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        categorie.delete()
        return redirect('ListCategorie')
    return render(request, 'magasin/Categories/delete_categorie.html', {'categorie': categorie})

def detail_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    context = {'categorie': categorie}
    return render(request, 'magasin/Categories/detail_categorie.html', context)

def ListCategorie(request):
        categories= Categorie.objects.all()
        context={'categories':categories}
        return render( request,'magasin/Categories/mesCategories.html',context )


def shop(request):
    produits = Produit.objects.all()
    categories = Categorie.objects.all()
    context = {
        'produits': produits,
        'categories': categories,
    }
    return render(request, 'magasin/shop.html', context)



def contact(request):
    if request.method =="POST":
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        
        #envoyer email
        send_mail(
            name,#subject
            message,#message
            email,#from email
            ['ayaomrani002@gmail.com'],#to email
            
        )
        
        return render(request,'contact.html',{'name':name})
    
    return render(request, 'magasin/contact.html', {})