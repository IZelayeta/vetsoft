from datetime import date

from django.shortcuts import reverse
from django.test import TestCase

from app.models import Client, Medicine, Pet, Provider, Specialty, Vet


class HomePageTest(TestCase):
    def test_use_home_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ClientsTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_user_with_valid_data(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        response = self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Guido Carrillo",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Guido Carrillo")
        self.assertEqual(editedClient.phone, client.phone)
        self.assertEqual(editedClient.address, client.address)
        self.assertEqual(editedClient.email, client.email)

class ProvidersTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("providers_repo"))
        self.assertTemplateUsed(response, "providers/repository.html")

    def test_repo_display_all_providers(self):
        response = self.client.get(reverse("providers_repo"))
        self.assertTemplateUsed(response, "providers/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("providers_form"))
        self.assertTemplateUsed(response, "providers/form.html")

    def test_can_create_provider(self):
        response = self.client.post(
            reverse("providers_form"),
            data={
                "name": "katerina mariescurrena",
                "email": "katy@gmail.com",
                "address": "17 y 166",
            },
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "katerina mariescurrena")
        self.assertEqual(providers[0].email, "katy@gmail.com")
        self.assertEqual(providers[0].address, "17 y 166")

        self.assertRedirects(response, reverse("providers_repo"))

    def test_validation_errors_create_provider(self):
        response = self.client.post(
            reverse("providers_form"),
             data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "")
    
    def test_should_response_with_404_status_if_providers_doesnt_exists(self):
        response = self.client.get(reverse("providers_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("providers_form"),
            data={
                "name": "katerina mariescurrena",
                "email": "katy",
                "address": "17 y 166",
            },
        )

        self.assertContains(response, "")

    def test_edit_user_with_valid_data(self):
        provider = Provider.objects.create(
            name="katerina mariescurrena",
            email= "katy@gmail.com",
            address="17 y 166",
        )

        response = self.client.post(
            reverse("providers_form"),
            data={
                "id": provider.id,
                "name": "Bruno Santillan",
                          },
        )
        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedProvider= Provider.objects.get(pk=provider.id)
        self.assertEqual(editedProvider.name, "Bruno Santillan")
        self.assertEqual(editedProvider.address, provider.address)
        self.assertEqual(editedProvider.email, provider.email)

class VetTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("vets_repo"))
        self.assertTemplateUsed(response, "vets/repository.html")

    def test_repo_display_all_vets(self):
        response = self.client.get(reverse("vets_repo"))
        self.assertTemplateUsed(response, "vets/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("vets_form"))
        self.assertTemplateUsed(response, "vets/form.html")

    def test_can_create_vet(self):
        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Carlos Chaplin",
                "phone": "2284563542",
                "email": "carlix@gmail.com",
                "specialty": Specialty.GENERAL.value,
            },
        )

        vets = Vet.objects.all()
        self.assertEqual(len(vets), 1)
        self.assertEqual(vets[0].name, "Carlos Chaplin")
        self.assertEqual(vets[0].phone, "2284563542")
        self.assertEqual(vets[0].email, "carlix@gmail.com")
        self.assertEqual(vets[0].specialty, Specialty.GENERAL.value)

        self.assertRedirects(response, reverse("vets_repo"))

    def test_validation_errors_create_vet(self):
        response = self.client.post(
            reverse("vets_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese una especialidad")

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Carlos Chaplin",
                "phone": "2284563542",
                "email": "carlix",
                "specialty": Specialty.GENERAL.value,
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")
    
    def test_edit_vet_with_valid_data(self):
        vet = Vet.objects.create(
            name="Carlos Chaplin",
            phone="2284563542",
            email="carlix@gmail.com",
            specialty=Specialty.GENERAL.value,
        )

        response = self.client.post(
            reverse("vets_form"),
            data={
                "id": vet.id,
                "name": "Diogenes Sinope",
                "specialty": Specialty.SURGERY.value,
            },
        )

        self.assertEqual(response.status_code, 302)
        editedVet = Vet.objects.get(pk=vet.id)
        self.assertEqual(editedVet.name, "Diogenes Sinope")
        self.assertEqual(editedVet.phone, vet.phone)
        self.assertEqual(editedVet.email, vet.email)
        self.assertEqual(editedVet.specialty, Specialty.SURGERY.value)

    def test_404_if_vet_doesnt_exists(self):
        response = self.client.get(reverse("vets_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

class MedicineTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("medicine_repo"))
        self.assertTemplateUsed(response, "medicine/repository.html")

    def test_repo_display_all_medicines(self):
        response = self.client.get(reverse("medicine_repo"))
        self.assertTemplateUsed(response, "medicine/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("medicine_form"))
        self.assertTemplateUsed(response, "medicine/form.html")

    def test_can_create_medicine(self):
        response = self.client.post(
            reverse("medicine_form"),
            data={
                "name": "ibuprofeno",
                "description": "analgesico",
                "dose": "4",
            },
        )
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "ibuprofeno")
        self.assertEqual(medicines[0].description, "analgesico")
        self.assertEqual(medicines[0].dose, 4)

        self.assertRedirects(response, reverse("medicine_repo"))

    def test_validation_errors_create_medicie(self):
        response = self.client.post(
            reverse("medicine_form"),
            data={},
        )
        self.assertContains(response, "Por favor ingrese una descripcion")
        self.assertContains(response, "Por favor ingrese una dosis")

    def test_should_response_with_404_status_if_medicine_doesnt_exists(self):
        response = self.client.get(reverse("medicine_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_dose(self):
        response = self.client.post(
            reverse("medicine_form"),
            data={
                "name": "ibuprofeno",
                "description": "analgesico",
                "dose": -1,
            },
        )

        self.assertContains(response, "Por favor ingrese una dosis")

    def test_edit_medicine_with_valid_data(self):
        medicine = Medicine.objects.create(
            name="ibuprofeno",
            description="analgesico",
            dose= 4,
        )

        response = self.client.post(
            reverse("medicine_form"),
            data={
                "id": medicine.id,
                "name": "ibuprofeno",
                      },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedMedicine = Medicine.objects.get(pk=medicine.id)
        self.assertEqual(editedMedicine.name, "ibuprofeno")
        self.assertEqual(editedMedicine.description, medicine.description)
        self.assertEqual(editedMedicine.dose, medicine.dose)
 
          
class PetsTest(TestCase):
    def test_can_create_pet(self):

        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )

        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Loki",
                "breed": "Border Collie",
                "birthday": date(2024,5,5),
                "weight": 10,
                "client":1
            },
        )

        pets = Pet.objects.all()
        self.assertEqual(len(pets), 1)

        self.assertEqual(pets[0].name, "Loki")
        self.assertEqual(pets[0].breed, "Border Collie")
        self.assertEqual(pets[0].birthday, date(2024,5,5))
        self.assertEqual(pets[0].weight, 10)
        self.assertEqual(pets[0].client, Client.objects.get(pk=1))

        self.assertRedirects(response, reverse("pets_repo"))

    def test_validation_errors_create_pet(self):
        response = self.client.post(
            reverse("pets_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese una raza")
        self.assertContains(response, "Por favor ingrese la fecha de cumpleaños")
        self.assertContains(response, "Por favor ingrese un peso")

    def test_validation_invalid_weight(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Loki",
                "breed": "Border Collie",
                "birthday": date(2024,5,5),
                "weight": 0,
                "client":1
            },
        )
        self.assertContains(response, "Por favor ingrese un peso mayor que 0")