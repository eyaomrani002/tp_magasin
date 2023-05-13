from .models import Produit,Categorie
from rest_framework.serializers import ModelSerializer
class ProduitSerializer(ModelSerializer):
    class Meta:
        model=Produit
        fields='__all__'
        

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'name']