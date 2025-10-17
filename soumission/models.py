from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile

class UtilisateurManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('L\'email doit être renseigné')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
class HackathonUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Téléphone')
    address = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True, verbose_name='Date de naissance')
    numeroCarteIdentite = models.CharField(max_length=50, blank=True, null=True, verbose_name='Numero CNIB/PASSPORT')
    dateDelivrance = models.DateField(blank=True, null=True, verbose_name='Date de delivrance')
    nationalite = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nationalité')

    USERNAME_FIELD = 'email'      
    REQUIRED_FIELDS = []
   
    objects = UtilisateurManager()



    
    


class Hackaton(models.Model):
    stattu_liste = (
        ("active", "active"),
        ("fermer", "fermer"),
    )
    description = models.TextField(null=True, blank=True)
    theme = models.CharField(max_length=150, null=True, blank=True)
    dateOuverture = models.DateTimeField(null=True, blank=True)
    dateFermeture = models.DateTimeField(null=True, blank=True) 
    publicCible = models.CharField(max_length=150, null=True, blank=True)
    lieu = models.CharField(max_length=150, null=True, blank=True)
    montantRecompense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    statut = models.CharField(max_length=150, null=True, blank=True, choices=stattu_liste)

    def __str__(self):
        return f"Hackaton: {self.theme} ({self.dateOuverture} - {self.dateFermeture})"

    
    
    
    
class Inscription(models.Model):
    user = models.OneToOneField(HackathonUser, null=True, blank=True, on_delete=models.CASCADE)
    hackaton = models.ForeignKey(Hackaton, null=True, blank=True, on_delete=models.CASCADE)
    nomComplet = models.CharField(null=True, blank=True, max_length=255)
    niveauEtude = models.CharField(max_length=100, blank=True, null=True)
    situationProfessionnelle = models.CharField(max_length=150, blank=True, null=True)
    competencePrincipale = models.CharField(max_length=150, blank=True, null=True)
    nomEquipe = models.CharField(max_length=150, blank=True, null=True)
    ideeProjet = models.TextField(blank=True, null=True)
    cv = models.FileField(upload_to='cv/', null=True, blank=True)
    dossier_projet = models.FileField(upload_to='dossier_projet/', null=True, blank=True)
    

    def __str__(self):
        return f"Inscription de {self.nomComplet}"
    
    
    
    
class Programme(models.Model):
    hackaton = models.ForeignKey(Hackaton, null=True, blank=True, on_delete=models.CASCADE)
    dateProgramme = models.DateField(null=True, blank=True)
    programme = models.CharField(null=True, blank=True, max_length=200)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Inscription de {self.programme}"
    
    
    


class Partenaire(models.Model):
    nom = models.CharField(null=True, blank=True, max_length=200)
    icon = models.ImageField(upload_to='icon_partenaire/', null=True, blank=True)

    def __str__(self):
        return f"Inscription de {self.nom}"

    def save(self, *args, **kwargs):
        # Sauvegarde initiale pour obtenir un fichier icon
        super().save(*args, **kwargs)

        if self.icon:
            # Ouvrir l'image existante
            img = Image.open(self.icon.path)
            
            # Taille cible
            taille = (75, 75)

            # Redimensionner
            img = img.resize(taille, Image.LANCZOS)

            # Sauvegarder en remplaçant le fichier existant
            img.save(self.icon.path)
