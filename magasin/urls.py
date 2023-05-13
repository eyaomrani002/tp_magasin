from django.urls import path,include
from . import views
from .views import CategoryAPIView
from rest_framework import routers
from magasin.views import  CategoryAPIView,ProduitAPIView,shop

from magasin.views import ProductViewset, CategoryAPIView
 
# Ici nous créons notre routeur
router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’
router.register('produit', ProductViewset, basename='produit')


urlpatterns = [ 
               
               
               
                path('contact.html',views.contact,name="contact"),
                
                path('api/category/', CategoryAPIView.as_view()),
                path('api/produits/', ProduitAPIView.as_view()),
                path('api-auth/', include('rest_framework.urls')),

                path('api/', include(router.urls)),
                
                path('', views.index,name='index'),
                path('',views.home,name='home'),
                path('indexA', views.indexA, name='indexA'),
                
               
                path('nouveau_produit/',views.nouveau_produit, name='nouveau_produit'),
                path('nouveauFournisseur/',views. nouveauFournisseur, name='nouveauFournisseur'),
                path('modifier_produit/<int:pk>/', views.modifier_produit, name='modifier_produit'),
                path('supprimer_produit/<int:pk>/', views.supprimer_produit, name='supprimer_produit'),

                
                path('fournisseurs/', views.ListFournisseur, name='fournisseurs'),
                path('nouvFournisseur/',views.nouveauFournisseur,name='nouvFournisseur'),
                path('editFournisseur/<int:fk>/', views.edit_Fournisseur, name='edit_Fournisseur'),
                path('deleteFournisseur/<int:fk>/', views.delete_Fournisseur, name='delete_Fournisseur'),
                path('Fournisseur/<int:for_id>/', views.detail_Fournisseur, name='detail_Fournisseur'),

                #categorie 

                path('ListCategorie/', views.ListCategorie, name='ListCategorie'),
                path('create_categorie/',views.create_categorie,name='create_categorie'),
                path('editCategorie/<int:pk>/', views.edit_categorie, name='edit_categorie'),
                path('deleteCategorie/<int:pk>/', views.delete_categorie, name='delete_categorie'),
                path('Categorie/<int:categorie_id>/', views.detail_categorie, name='detail_categorie'),






                path('ListCommande/', views.ListCommande, name='ListCommande'),
                path('create_commande/',views.create_commande,name='create_commande'),
                path('editCommande/<int:pk>/', views.edit_commande, name='edit_commande'),
                path('deleteCommande/<int:pk>/', views.delete_commande, name='delete_commande'),
                path('Commande/<int:commande_id>/', views.detail_commande, name='detail_commande'),


                path('registurls.pyer/',views.register, name = 'register'),
                path('magasin/search/', views.search, name='search'),
                path('magasin/<int:pk>/', views.product_detail, name='product_detail'),
                
                path('shop/', shop, name='shop'),
                
            ]