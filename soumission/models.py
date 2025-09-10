from django.db import models

class Inscription(models.Model):
    nom = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    competences = models.CharField(max_length=50, blank=True, null=True)
    equipe = models.CharField(max_length=100, blank=True, null=True)
    projet = models.TextField(blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.email}"
