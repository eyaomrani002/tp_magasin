# Generated by Django 4.1.7 on 2023-03-07 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0005_remove_commande_produits_delete_produitnc_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProduitNC',
            fields=[
                ('produit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='magasin.produit')),
                ('Duree_garantie', models.CharField(max_length=100, null=True)),
            ],
            bases=('magasin.produit',),
        ),
    ]
