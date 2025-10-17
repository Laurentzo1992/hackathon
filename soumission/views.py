from django.shortcuts import render
from soumission.serializers  import UserSerializer
from rest_framework import viewsets
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from soumission.models import HackathonUser, Inscription, Hackaton, Programme, Partenaire
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

MAX_UPLOAD_SIZE = 2 * 1024 * 1024 


""" vu principal de la page d'acceuil """
def home(request):
    partenairs = Partenaire.objects.all()
    hackaton = (
        Hackaton.objects.filter(statut="active")
        .prefetch_related("programme_set")
        .first()
    )

    programmes = []
    if hackaton:
        programmes = hackaton.programme_set.all().order_by("dateProgramme")

    context = {
        "hackathon": hackaton,
        "programmes": programmes,
        "partenairs":partenairs,
    }
    return render(request, 'soumission/home.html', context)



#  api pour recuperer la liste des hackathon actifs
def hackathon_active(request):
    hackathon = Hackaton.objects.filter(statut="active").first()
    if hackathon:
        data = {
            "theme": hackathon.theme,
            "dateOuverture": hackathon.dateOuverture.isoformat() if hackathon.dateOuverture else None,
            "dateFermeture": hackathon.dateFermeture.isoformat() if hackathon.dateFermeture else None,
            "lieu": hackathon.lieu,
            "recompense": str(hackathon.montantRecompense) if hackathon.montantRecompense else None,
        }
    else:
        data = {"error": "Aucun hackathon actif"}
    return JsonResponse(data)



#  api pour recuperer la liste des hackathon 

def hackathon_list(request):
    hackathons = Hackaton.objects.all()
    data = [
        {
            "id": h.id,
            "theme": h.theme,
        }
        for h in hackathons
    ]
    return JsonResponse(data, safe=False)







#  api pour d'inscrire au hackathon 
@csrf_exempt
def inscription_hackathon(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        adresse = request.POST.get("adresse")
        birth_date = request.POST.get("birth_date")
        numeroCarteIdentite = request.POST.get("numeroCarteIdentite")
        dateDelivrance = request.POST.get("dateDelivrance")
        nationalite = request.POST.get("nationalite")
        competences = request.POST.get("competences")
        niveauEtude = request.POST.get("niveauEtude")
        equipe = request.POST.get("equipe")
        situationProfessionnelle = request.POST.get("situationProfessionnelle")
        projet = request.POST.get("projet")
        hackaton_id = request.POST.get("hackaton")
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        cv_file = request.FILES.get("cv")
        dossier_projet_file = request.FILES.get("dossier_projet")

        # Vérification des mots de passe
        if password != password2:
            return JsonResponse({"success": False, "message": "Les mots de passe ne correspondent pas."})

        # Vérification du hackathon
        try:
            hackaton = Hackaton.objects.get(id=hackaton_id)
        except Hackaton.DoesNotExist:
            return JsonResponse({"success": False, "message": "Hackathon introuvable."})

        # Vérification email unique
        if HackathonUser.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "Un compte avec cet email existe déjà."})

        # Vérification fichiers obligatoires
        if not cv_file or not dossier_projet_file:
            return JsonResponse({"success": False, "message": "CV et pièce d'identité sont obligatoires."})

        # Vérification taille max 2 Mo
        if cv_file.size > MAX_UPLOAD_SIZE:
            return JsonResponse({"success": False, "message": "Le CV dépasse 2 Mo."})
        if dossier_projet_file.size > MAX_UPLOAD_SIZE:
            return JsonResponse({"success": False, "message": "La pièce d'identité dépasse 2 Mo."})

        try:
            # Création de l'utilisateur
            achuser = HackathonUser.objects.create_user(
                email=email,
                phone=telephone,
                address=adresse,
                birth_date=birth_date,
                numeroCarteIdentite=numeroCarteIdentite,
                dateDelivrance=dateDelivrance,
                nationalite=nationalite,
                password=password,
                
            )

            # Enregistrement de l'inscription
            Inscription.objects.create(
                user=achuser,
                hackaton=hackaton,
                ideeProjet=projet,
                situationProfessionnelle=situationProfessionnelle,
                nomEquipe=equipe,
                niveauEtude=niveauEtude,
                competencePrincipale=competences,
                nomComplet=nom,
                cv=cv_file,  
                dossier_projet=dossier_projet_file
            )

            return JsonResponse({"success": True, "message": f"Merci {nom}, votre inscription a été enregistrée !"})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erreur lors de l'inscription : {str(e)}"})

    return JsonResponse({"success": False, "message": "Méthode non autorisée"})












    


