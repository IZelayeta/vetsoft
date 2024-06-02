from datetime import date

from django.shortcuts import get_object_or_404, redirect, render, reverse
from pyexpat.errors import messages

from .models import Client, Medicine, Pet, Product, Provider, Specialty, Vet


def home(request):
    return render(request, "home.html")

def providers_repository(request):
    providers = Provider.objects.all()
    return render(request, "providers/repository.html", {"providers": providers})


def providers_form(request, id=None):
    if request.method == "POST":
        provider_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if provider_id == "":
            saved, errors = Provider.save_provider(request.POST)
        else:
            provider = get_object_or_404(Provider, pk=provider_id)
            provider.update_provider(request.POST)

        if saved:
            return redirect(reverse("providers_repo"))

        return render(
            request, "providers/form.html", {"errors": errors, "provider": request.POST}
        )

    provider = None
    if id is not None:
        provider = get_object_or_404(Provider, pk=id)

    return render(request, "providers/form.html", {"provider": provider})

def providers_delete(request):
    provider_id = request.POST.get("provider_id")
    provider = get_object_or_404(Provider, pk=int(provider_id))
    provider.delete()

    return redirect(reverse("providers_repo"))

def clients_repository(request):
    vacioP = bool(Product.objects.all())
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients, "vacioP":vacioP})


def clients_form(request, id=None):
    if request.method == "POST":
        client_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if client_id == "":
            saved, errors = Client.save_client(request.POST)
        else:
            client = get_object_or_404(Client, pk=client_id)
            client.update_client(request.POST)

        if saved:
            return redirect(reverse("clients_repo"))

        return render(
            request, "clients/form.html", {"errors": errors, "client": request.POST}
        )

    client = None
    if id is not None:
        client = get_object_or_404(Client, pk=id)

    return render(request, "clients/form.html", {"client": client})


def clients_delete(request):
    client_id = request.POST.get("client_id")
    client = get_object_or_404(Client, pk=int(client_id))
    client.delete()

    return redirect(reverse("clients_repo"))

#VETERINARIO

def vets_repository(request):
    vets = Vet.objects.all()
    
    return render(request, "vets/repository.html", {"vets": vets})

def vets_form(request, id=None):
    specialties = Specialty.choices()
    if request.method == "POST":
        vet_id = request.POST.get("id", "")
        errors = {}
        saved = True
        

        if vet_id == "":
            saved, errors = Vet.save_vet(request.POST)
        else:
            vet = get_object_or_404(Vet, pk=vet_id)
            vet.update_vet(request.POST)

        if saved:
            return redirect(reverse("vets_repo"))

        return render(
            request, "vets/form.html", {"errors": errors, "vet": request.POST, "specialties": specialties}
        )

    vet = None
    if id is not None:
        vet = get_object_or_404(Vet, pk=id)

    return render(request, "vets/form.html", {"vet": vet, "specialties": specialties})


def vets_delete(request):
    vet_id = request.POST.get("vet_id")
    vet = get_object_or_404(Vet, pk=int(vet_id))
    vet.delete()

    return redirect(reverse("vets_repo"))

#PRODUCTO

def clients_add_product(request, id=None):
    client = get_object_or_404(Client, pk=id)
    products = Product.objects.all() 
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        client.products.add(product)  
        return redirect(reverse("clients_repo"))
    if not products:
        messages.error(request, "No hay productos disponibles")
        return redirect(reverse("clients_repo"))

    return render(request, "clients/add_product.html", {"client": client, "products": products})

def select_products_to_delete(request):
    client_id = request.GET.get('id')
    client = get_object_or_404(Client, pk=client_id)
    products = client.products.all()
    return render(request, 'clients/select_products.html', {'products': products, 'client_id': client_id})

def delete_selected_products(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('products[]')
        client_id = request.POST.get('client_id')
        client = get_object_or_404(Client, pk=client_id)
        client.products.remove(*product_ids)
    return redirect('clients_repo')

def products_repository(request):
    products = Product.objects.all()
    return render(request, "products/repository.html", {"products": products})

def product_form(request, id=None):
    providers = Provider.objects.all()
    if request.method == "POST":
        product_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if product_id == "":
            saved, errors = Product.save_product(request.POST)
        else:
            product = get_object_or_404(Product, pk=product_id)
            product.update_product(request.POST)

        if saved:
            return redirect(reverse("products_repo"))

        return render(
            request, "products/form.html", {"errors": errors, "product": request.POST, "providers": providers}
        )

    product = None
    if id is not None:
        product = get_object_or_404(Product, pk=id)

    return render(request, "products/form.html", {"product": product, "providers": providers})

def products_delete(request):
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, pk=int(product_id))
    product.delete()
    return redirect(reverse("products_repo"))

#MEDICINA

def medicine_repository(request):
    medicine = Medicine.objects.all()
    print(medicine)
    return render(request, "medicine/repository.html", {"medicines": medicine})

#def medicine_form(request):
#    return render(request,"medicine/form.html",)

def medicine_form(request, id=None):
    if request.method == "POST":
        medicine_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if medicine_id == "":
            saved, errors = Medicine.save_medicine(request.POST)
        else:
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            medicine.update_medicine(request.POST)

        if saved:
            return redirect(reverse("medicine_repo"))

        return render(
            request, "medicine/form.html", {"errors": errors, "medicine": request.POST}
        )

    medicine = None
    if id is not None:
        medicine = get_object_or_404(Medicine, pk=id)

    return render(request, "medicine/form.html", {"medicine": medicine})

def medicine_delete(request):
    medicine_id = request.POST.get("medicine_id")
    medicine = get_object_or_404(Medicine, pk=int(medicine_id))
    medicine.delete()

    return redirect(reverse("medicine_repo"))

def pets_add_medicine(request, id=None):
    pet = get_object_or_404(Pet, pk=id)
    medicines = Medicine.objects.all()
    if request.method == "POST":
        medicine_id = request.POST.get("medicine_id")
        medicine = get_object_or_404(Medicine, pk=medicine_id)
        pet.medicines.add(medicine)
        return redirect(reverse("pets_repo"))
    if not medicines:
        messages.error(request, "No hay medicinas disponibles")
        return redirect(reverse("pets_repo"))

    return render(request, "pets/add_medicine.html", {"pet": pet, "medicines": medicines},)

def pets_add_vets(request, id=None):
    pet = get_object_or_404(Pet, pk=id)
    medicines = Medicine.objects.all()
    if request.method == "POST":
        medicine_id = request.POST.get("medicine_id")
        medicine = get_object_or_404(Medicine, pk=medicine_id)
        pet.medicines.add(medicine)
        return redirect(reverse("pets_repo"))
    if not medicines:
        messages.error(request, "No hay medicinas disponibles")
        return redirect(reverse("pets_repo"))

    return render(request, "pets/add_medicine.html", {"pet": pet, "medicines": medicines},)


def pets_repository(request):
    pets=Pet.objects.all()
    vacioC=bool(Client.objects.all())
    vacioM = bool(Medicine.objects.all())
    vacioV = bool(Vet.objects.all())
    #vacioV 
    return render(request,"pets/repository.html", {"pets":pets, "vacioC":vacioC,"vacioM":vacioM, "vacioV":vacioV  })

def pets_form(request, id=None):
    clients = Client.objects.all()
    fecha_actual = date.today().isoformat()

    if request.method == "POST":
        pet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if pet_id == "":
            saved, errors = Pet.save_pet(request.POST)
        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            pet.update_pet(request.POST)

        if saved:
            return redirect(reverse("pets_repo"))

        return render(
            request, "pets/form.html", {"errors": errors, "pet": request.POST, "clients":clients, "fecha_actual":fecha_actual},
        )
    pet = None
    if id is not None:
        pet = get_object_or_404(Pet, pk=id)

    return render(request, "pets/form.html", {"pet": pet, "clients":clients, "fecha_actual":fecha_actual})

def pets_delete(request):
    pet_id = request.POST.get("pet_id")
    pet = get_object_or_404(Pet, pk=int(pet_id))
    pet.delete()

    return redirect(reverse("pets_repo"))

def select_medicines_to_delete(request):
    pet_id = request.GET.get('id')
    pet = get_object_or_404(Pet, pk=pet_id)
    medicines = pet.medicines.all()
    return render(request, 'pets/select_medicines.html', {'medicines': medicines, 'pet_id': pet_id})

def delete_selected_medicines(request):
    if request.method == 'POST':
        medicine_ids = request.POST.getlist('medicines[]')
        pet_id = request.POST.get('pet_id')
        pet = get_object_or_404(Pet, pk=pet_id)
        pet.medicines.remove(*medicine_ids)
    return redirect('pets_repo')

def select_vets_for_deletion(request):
    pet_id = request.GET.get('id')
    pet = get_object_or_404(Pet, pk=pet_id)
    vets = pet.vets.all()
    return render(request, 'pets/select_vets.html', {'vets': vets, 'pet_id': pet_id})


def delete_vets_selected(request):
    if request.method == 'POST':
        medicine_ids = request.POST.getlist('medicines[]')
        pet_id = request.POST.get('pet_id')
        pet = get_object_or_404(Pet, pk=pet_id)
        pet.medicines.remove(*medicine_ids)
    return redirect('pets_repo')

def pets_add_vet(request, id=None):
    pet = get_object_or_404(Pet, pk=id)
    vets = Vet.objects.all() 
    if request.method == "POST":
        vet_id = request.POST.get("vet_id")
        vet = get_object_or_404(Vet, pk=vet_id)
        pet.vets.add(vet)  
        return redirect(reverse("pets_repo"))
    if not vets:
        messages.error(request, "No hay veterinarios disponibles")
        return redirect(reverse("pets_repo"))

    return render(request, "pets/add_vet.html", {"pet": pet, "vets": vets})

def select_vets_to_delete(request):
    pet_id = request.GET.get('id')
    pet = get_object_or_404(Pet, pk=pet_id)
    vets = pet.vets.all()
    return render(request, 'pets/select_vets.html', {'vets': vets, 'pet_id': pet_id})

def delete_selected_vets(request):
    if request.method == 'POST':
        vett_ids = request.POST.getlist('vets[]')
        pet_id = request.POST.get('pet_id')
        pet = get_object_or_404(Pet, pk=pet_id)
        pet.vets.remove(*vett_ids)
    return redirect('pets_repo')