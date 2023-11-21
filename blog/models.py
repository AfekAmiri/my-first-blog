from django.db import models
from django.core.exceptions import ValidationError

class Lieu(models.Model):
    DISPONIBILITE_CHOICES = [
        ('Disponible', 'Disponible'),
        ('Occupé', 'Occupé'),
    ]
    id_lieu = models.CharField(max_length=100, primary_key=True)
    disponibilite = models.CharField(max_length=20, choices=DISPONIBILITE_CHOICES)
    photo = models.ImageField(upload_to='ImagesLieux/')
    def __str__(self):
        return self.id_lieu
    class Meta:
        verbose_name_plural = "Lieux"
    def get_occupants(self):
        return Pokemon.objects.filter(lieu=self)
 
 
class Pokemon(models.Model):
    ETAT_CHOICES = [
        ('Libre', 'Libre'),
        ('Affamé', 'Affamé'),
        ('Repus', 'Repus'),
        ('Blessé','Blessé'),
    ]
    TYPE_CHOICES =[
        ('Plante', 'Plante'),
        ('Sol', 'Sol'),
        ('Eau', 'Eau'),
        ('Feu','Feu'), 
     ]
    NIVEAU_CHOICES =[
        ('Faible', 'Faible'),
        ('Moyen', 'Moyen'),
        ('Fort', 'Fort'), 
     ]
    nom= models.CharField(max_length=100, primary_key=True)
    etat = models.CharField(max_length=20,choices=ETAT_CHOICES)
    type = models.CharField(max_length=20,choices=TYPE_CHOICES)
    niveau=models.CharField(max_length=20,choices=NIVEAU_CHOICES)
    photo =models.ImageField(upload_to='ImagesPokemons/')
    lieu = models.ForeignKey('blog.Lieu', on_delete=models.CASCADE)
    def clean(self):
        # Cohérence du lieu et de l'état
        if self.lieu.id_lieu == 'Parc':
            if self.etat not in ['Libre', 'Blessé']:
                raise ValidationError("Dans le parc, les pokemons sont soit libres soit blessés")
        elif self.lieu.id_lieu in ['Infirmerie', 'Ball']:
            if self.etat != 'Affamé':
                raise ValidationError("Le Pokémon doit être affamé quand il est dans l'infirmerie ou dans la ball")
        elif self.lieu.id_lieu == 'Restaurant' and self.etat != 'Repus':
            raise ValidationError("Le Pokémon doit être repus quand il est au restaurant")

        # Vérifier la capacité du lieu avant de sauvegarder le Pokémon
        if self.lieu.id_lieu == 'Parc':
            parc_pokemons = Pokemon.objects.filter(lieu__id_lieu='Parc').count()
            if parc_pokemons >= 2:
                raise ValidationError("Le Parc est plein. Impossible d'ajouter plus de Pokémon.")
            elif parc_pokemons == 1:
                self.lieu.disponibilite = 'Occupé'
                self.lieu.save()
                if (Pokemon.objects.filter(lieu__id_lieu='Infirmerie').count()==0):
                    inf=Lieu.objects.get(id_lieu='Infirmerie')
                    inf.disponibilite='Disponible'
                    inf.save()
        elif self.lieu.id_lieu == 'Infirmerie':
            infirmerie_pokemons = Pokemon.objects.filter(lieu__id_lieu='Infirmerie').count()
            if infirmerie_pokemons >= 1:
                raise ValidationError("L'Infirmerie est occupée. Impossible d'ajouter plus de Pokémon.")
            else:
                self.lieu.disponibilite = 'Occupé'
                self.lieu.save()
                if (Pokemon.objects.filter(lieu__id_lieu='Restaurant').count()<=1):
                    resto=Lieu.objects.get(id_lieu='Restaurant')
                    resto.disponibilite='Disponible'
                    resto.save()
    def ajout(self):
        self.clean()
        self.save()
    def suppression(self):
        try:
        # Vérifier si le Pokémon est dans l'infirmerie ou le parc
            if self.lieu.id_lieu in ['Infirmerie', 'Parc']:
            # Supprimer le Pokémon de la base de données
                self.lieu.disponibilite='Disponible'
                self.lieu.save()
                self.delete()
            else:
                raise ValidationError(f"Impossible de supprimer {self.nom}.")
        except Pokemon.DoesNotExist:
                raise ValueError(f"Le Pokémon {self.nom} n'existe pas.")
    def __str__(self):
        return self.nom