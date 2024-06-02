import os
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import Browser, expect, sync_playwright

from app.models import Client, Medicine, Provider, Specialty, Vet

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser: Browser = playwright.firefox.launch(
            headless=headless, slow_mo=int(slow_mo)
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    def test_should_have_navbar_with_links(self):
        self.page.goto(self.live_server_url)

        navbar_home_link = self.page.get_by_test_id("navbar-Home")

        expect(navbar_home_link).to_be_visible()
        expect(navbar_home_link).to_have_text("Home")
        expect(navbar_home_link).to_have_attribute("href", reverse("home"))

        navbar_clients_link = self.page.get_by_test_id("navbar-Clientes")

        expect(navbar_clients_link).to_be_visible()
        expect(navbar_clients_link).to_have_text("Clientes")
        expect(navbar_clients_link).to_have_attribute("href", reverse("clients_repo"))

    def test_should_have_home_cards_with_links(self):
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="221232555",
            email="goleador@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

    def test_should_show_client_delete_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente"
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class ClientCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_client(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido")
        ).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.get_by_label("Email").fill("goleador@gmail.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()
        expect(self.page.get_by_text("221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

class ProvidersRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).to_be_visible()

    def test_should_show_providers_data(self):
        Provider.objects.create(
            name="katerina mariescurrena",
            email="katy@gmail.com",
            address="17 y 166",
        )

        Provider.objects.create(
            name="Bruno Santillan",
            email="bsantillan@gmail.com",
            address="16 y 50",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("No existen providers")).not_to_be_visible()

        expect(self.page.get_by_text("katerina mariescurrena")).to_be_visible()
        expect(self.page.get_by_text("katy@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("17 y 166")).to_be_visible()

        expect(self.page.get_by_text("Bruno Santillan")).to_be_visible()
        expect(self.page.get_by_text("bsantillan@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("16 y 50")).to_be_visible()

    def test_should_show_add_provider_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        add_provider_action = self.page.get_by_role(
            "link", name="Nuevo proveedor", exact=False
        )
        expect(add_provider_action).to_have_attribute("href", reverse("providers_form"))

    def test_should_show_provider_edit_action(self):
        provider = Provider.objects.create(
            name="katerina mariescurrena",
            email="katy@gmail.com",
            address="17 y 166",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("providers_edit", kwargs={"id": provider.id})
        )

    def test_should_show_provider_delete_action(self):
        provider = Provider.objects.create(
            name="katerina mariescurrena",
            email="katy@gmail.com",
            address="17 y 166",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de proveedor"
        )
        provider_id_input = edit_form.locator("input[name=provider_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("providers_delete"))
        expect(provider_id_input).not_to_be_visible()
        expect(provider_id_input).to_have_value(str(provider.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_provider(self):
        Provider.objects.create(
            name="katerina mariescurrena",
            email="katy@gmail.com",
            address="17 y 166",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("katerina mariescurrena")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("providers_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
          self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)
        
        expect(self.page.get_by_text("katerina mariescurrena")).not_to_be_visible()
        
class ProviderCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_provider(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("katerina mariescurrena")
        self.page.get_by_label("Email").fill("katy@gmail.com")
        self.page.get_by_label("Dirección").fill("17 y 166")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("katerina mariescurrena")).to_be_visible()
        expect(self.page.get_by_text("katy@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("17 y 166")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()

        self.page.get_by_label("Nombre").fill("katerina mariescurrena")
        self.page.get_by_label("Email").fill("katy@gmail.com")
        self.page.get_by_label("Dirección").fill("17 y 166")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()

    def test_should_be_able_to_edit_a_provider(self):
        provider = Provider.objects.create(
            name="katerina mariescurrena",
            address="17 y 166",
            email="katy@gmail.com",
        )

        path = reverse("providers_edit", kwargs={"id": provider.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Bruno Santillan")
        self.page.get_by_label("Email").fill("bsantillan@gmail.com")
        self.page.get_by_label("Dirección").fill("16 y 50")
            
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("katerina mariescurrena")).not_to_be_visible()
        expect(self.page.get_by_text("katy@gmail.com")).not_to_be_visible()
        expect(self.page.get_by_text("17 y 166")).not_to_be_visible()

        expect(self.page.get_by_text("Bruno Santillan")).to_be_visible()
        expect(self.page.get_by_text("bsantillan@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("16 y 50")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute("href", reverse("providers_edit", kwargs={"id": provider.id}))

class VetsRepoTestCase(PlaywrightTestCase):
    
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        expect(self.page.get_by_text("No existen veterinarios")).to_be_visible()
    
    def test_should_show_vets_data(self):
        Vet.objects.create(
            name="Carlos Chaplin",
            phone="2284563542",
            email="carlix@gmail.com",
            specialty=Specialty.GENERAL.value,
        )

        Vet.objects.create(
            name="Diogenes Sinope",
            phone="221232555",
            email="diogeneselperro@gmail.com",
            specialty=Specialty.SURGERY.value,
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        expect(self.page.get_by_text("No existen veterinarios")).not_to_be_visible()

        expect(self.page.get_by_text("Carlos Chaplin")).to_be_visible()
        expect(self.page.get_by_text("2284563542")).to_be_visible()
        expect(self.page.get_by_text("carlix@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("General")).to_be_visible()

        expect(self.page.get_by_text("Diogenes Sinope")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("diogeneselperro@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("Cirugía")).to_be_visible()

    def test_should_show_add_vet_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        add_vet_action = self.page.get_by_role(
            "link", name="Nuevo veterinario", exact=False
        )
        expect(add_vet_action).to_have_attribute("href", reverse("vets_form"))
    
    def test_should_show_vet_edit_action(self):
        vet = Vet.objects.create(
            name="Carlos Chaplin",
            phone="2284563542",
            email="carlix@gmail.com",
            specialty=Specialty.GENERAL.value,
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("vets_edit", kwargs={"id": vet.id})
        )

    def test_should_show_vet_delete_action(self):
        vet = Vet.objects.create(
            name="Carlos Chaplin",
            phone="2284563542",
            email="carlix@gmail.com",
            specialty=Specialty.GENERAL.value,
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")
        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de veterinario"
        )
        vet_id_input = edit_form.locator("input[name=vet_id]")
        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("vets_delete"))
        expect(vet_id_input).not_to_be_visible()
        expect(vet_id_input).to_have_value(str(vet.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_vet(self):
        Vet.objects.create(
            name="Carlos Chaplin",
            phone="2284563542",
            email="carlix@gmail.com",
            specialty=Specialty.GENERAL.value,
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")
        expect(self.page.get_by_text("Carlos Chaplin")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("vets_delete"))
          
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)
       
        expect(self.page.get_by_text("Carlos Chaplin")).not_to_be_visible()

    
class PetCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_pet(self):
        client = Client.objects.create(
        name="Juan Sebastian Veron",
        email="juan.veron@example.com",
        phone="123456789"
        )
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()
        self.page.select_option("select[name=client]", str(client.id))
        self.page.get_by_label("Nombre").fill("Loki")
        self.page.get_by_label("Raza").fill("Border Collie")
        fecha_nacimiento = date(2024, 5, 5).strftime('%Y-%m-%d')
        self.page.get_by_label("Cumpleaños").fill(fecha_nacimiento)
        self.page.locator('input[type="number"][name="weight"]').fill('10')


        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Loki")).to_be_visible()
        expect(self.page.get_by_text("Border Collie")).to_be_visible()
        expect(self.page.get_by_text("May 5, 2024")).to_be_visible()
        expect(self.page.get_by_text("10")).to_be_visible()
        expect(self.page.get_by_text("Juan Sebastian Veron")).to_be_visible()
        expect(self.page.get_by_text("Sin Medicinas")).to_be_visible()

class MedicineRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicine_repo')}")

        expect(self.page.get_by_text("No existen medicinas")).to_be_visible()

    def test_should_show_medicine_data(self):
        Medicine.objects.create(
            name="ibuprofeno",
            description="analgesico1",
            dose=4,
        )

        Medicine.objects.create(
            name="paracetamol",
            description="analgesico2",
            dose=5,
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicine_repo')}")

        expect(self.page.get_by_text("No existen medicinas")).not_to_be_visible()

        expect(self.page.get_by_text("ibuprofeno")).to_be_visible()
        expect(self.page.get_by_text("analgesico1")).to_be_visible()
        expect(self.page.get_by_text("4")).to_be_visible()

        expect(self.page.get_by_text("paracetamol")).to_be_visible()
        expect(self.page.get_by_text("analgesico2")).to_be_visible()
        expect(self.page.get_by_text("5")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicine_repo')}")

        add_medicine_action = self.page.get_by_role(
            "link", name="Nueva medicina", exact=False
        )
        expect(add_medicine_action).to_have_attribute("href", reverse("medicine_form"))

    def test_should_show_client_edit_action(self):
        medicine = Medicine.objects.create(
            name="ibuprofeno",
            description="analgesico",
            dose=4,
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicine_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("medicine_edit", kwargs={"id": medicine.id})
        )

    def test_should_show_client_delete_action(self):
        medicine = Medicine.objects.create(
            name="ibuprofeno",
            description="analgesico",
            dose=4,
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicine_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de la medicina"
        )
        medicine_id_input = edit_form.locator("input[name=medicine_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("medicine_delete"))
        expect(medicine_id_input).not_to_be_visible()
        expect(medicine_id_input).to_have_value(str(medicine.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_medicine(self):
        Medicine.objects.create(
            name="ibuprofeno",
            description="analgesico",
            dose=4,
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicine_repo')}")

        expect(self.page.get_by_text("ibuprofeno")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("medicine_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
          self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)
        
        expect(self.page.get_by_text("ibuprofeno")).not_to_be_visible()
       
class VetCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_vet(self):
        self.page.goto(f"{self.live_server_url}{reverse('vets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Carlos Chaplin")
        self.page.get_by_label("Teléfono").fill("2284563542")
        self.page.get_by_label("Email").fill("carlix@gmail.com")
        self.page.get_by_label("Especialidad").select_option("General")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Carlos Chaplin")).to_be_visible()
        expect(self.page.get_by_text("2284563542")).to_be_visible()
        expect(self.page.get_by_text("carlix@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("General")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('vets_form')}")
        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una especialidad")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Carlos Chaplin")
        self.page.get_by_label("Teléfono").fill("2284563542")
        self.page.get_by_label("Email").fill("carlix")
        self.page.get_by_label("Especialidad").select_option("General")
        
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email valido")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una especialidad")).not_to_be_visible()
        
    def test_should_be_able_to_edit_a_vet(self):
        vet = Vet.objects.create(
            name="Carlos Chaplin",
            phone="2284563542",
            email="carlix@gmail.com",
            specialty=Specialty.GENERAL.value,
        )

        path = reverse("vets_edit", kwargs={"id": vet.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Diogenes Sinope")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.get_by_label("Email").fill("diogeneselperro@gmail.com")
        self.page.get_by_label("Especialidad").select_option("Cirugía")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Carlos Chaplin")).not_to_be_visible()
        expect(self.page.get_by_text("2284563542")).not_to_be_visible()
        expect(self.page.get_by_text("carlix@gmail.com")).not_to_be_visible()
        expect(self.page.get_by_text("General")).not_to_be_visible()

        expect(self.page.get_by_text("Diogenes Sinope")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("diogeneselperro@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("Cirugía")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("vets_edit", kwargs={"id": vet.id})
        )
     
class MedicineCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_medicine(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("ibuprofeno")
        self.page.get_by_label("Descripcion").fill("analgesico")
        self.page.get_by_label("Dosis").fill("4")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("ibuprofeno")).to_be_visible()
        expect(self.page.get_by_text("analgesico")).to_be_visible()
        expect(self.page.get_by_text("4")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una descripcion")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dosis")).to_be_visible()

        self.page.get_by_label("Nombre").fill("ibuprofeno")
        self.page.get_by_label("Descripcion").fill("analgesico")
        self.page.get_by_label("Dosis").fill("4")

        expect(self.page.get_by_text("Por favor ingrese una descripcion")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dosis")).not_to_be_visible()

    def test_should_be_able_to_edit_a_medicine(self):
        medicine = Medicine.objects.create(
            name="ibuprofeno",
            description="analgesico1",
            dose=4,
        )

        path = reverse("medicine_edit", kwargs={"id": medicine.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("paracetamol")
        self.page.get_by_label("Descripcion").fill("analgesico2")
        self.page.get_by_label("Dosis").fill("5")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("ibuprofeno")).not_to_be_visible()
        expect(self.page.get_by_text("analgesico1")).not_to_be_visible()
        expect(self.page.get_by_text("4")).not_to_be_visible()

        expect(self.page.get_by_text("paracetamol")).to_be_visible()
        expect(self.page.get_by_text("analgesico2")).to_be_visible()
        expect(self.page.get_by_text("5")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("medicine_edit", kwargs={"id": medicine.id})
        )
