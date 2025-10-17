from django.test import TestCase
from django.urls import reverse
from .models import Hackaton, Programme
from datetime import date

class ProgrammeApiTest(TestCase):
    def setUp(self):
        self.hackathon = Hackaton.objects.create(
            theme="Hackathon Test",
            statut="active" 
        )
        Programme.objects.create(
            hackaton=self.hackathon,
            dateProgramme=date(2025, 3, 15),
            programme="Lancement officiel",
            description="Début du hackathon"
        )

    def test_api_programme(self):
        url = reverse("programme_actif")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("programmes", response.json())
        self.assertEqual(response.json()["programmes"][0]["programme"], "Lancement officiel")
