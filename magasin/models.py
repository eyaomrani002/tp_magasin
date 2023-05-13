from datetime import date
from django.db import models

class Produit(models.Model):
    TYPE_CHOICES=[('em','emballé'),
              ('fr','frais'),
              ('cs','conservé')
              ]
    libellé = models.CharField(max_length=100)
    description = models.TextField(default='non definie')
    prix = models.DecimalField(max_digits=10, decimal_places=3)
    type = models.CharField(max_length=2,choices=TYPE_CHOICES,default='em')
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE, null=True)
    fournisseur=models.ForeignKey('Fournisseur',on_delete=models.CASCADE,null=True)
    img=models.ImageField(blank=True,upload_to='media/')
    def __str__(self):
        return (self.libellé +","+self.description+","+str(self.prix)+"," +self.type )

class Categorie(models.Model):
    TYPE_CHOICES=[('AL','Alimentaire'),
                  ('Mb','Meuble'),
                  ('Sn','Sanitaire'),
                  ('Vs','Vaisselle'),
                  ('Vt','Vêtement'),
                  ('Jx','Jouets'),
                  ('Lg','Linge de Maison'),
                  ('Bj','Bijoux'),
                  ('Dc','Décor')
                  ]
    name=models.CharField(max_length=50,default='AL',choices=TYPE_CHOICES)
    
    def __str__(self):
        return self.name
    
class Fournisseur(models.Model):
    nom=models.CharField(max_length=100,null=True)
    adresse=models.TextField(null=True)
    email=models.EmailField(null=True)
    telephone=models.CharField(max_length=8,null=True)

    def __str__(self):
        return (self.nom+','+self.adresse+','+self.email+','+self.telephone)
    
class ProduitNC(Produit):
    Duree_garantie=models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return "objet ProduitNC:%s"%(self.Duree_garantie)

class Commande(models.Model):
    dateCde=models.DateField(null=True,default=date.today)
    totalCde=models.DecimalField(max_digits=10,decimal_places=3)
    produits=models.ManyToManyField('Produit')
    
    def __str__(self):
        return"objet Produit :%s,%s"% (self.dateCde+','+self.totalCde)
    
"""class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    totalCde = models.DecimalField(max_digits=10, decimal_places=3)
    produits = models.ManyToManyField('Produit')

    def __str__(self):
        return str(self.dateCde) + ' - ' + str(self.totalCde)"""
# python manage.py migrate
#python manage.py makemigrations


# Create your models here.
