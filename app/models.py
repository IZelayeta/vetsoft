from enum import Enum

from django.db import models


class Specialty(Enum):
    """
    Enumeración para las especialidades veterinarias.

    Atributos:
    ----------
    GENERAL : str
        Especialidad de medicina general.
    SURGERY : str
        Especialidad en cirugía.
    DERMATOLOGY : str
        Especialidad en dermatología.
    ORTHOPEDICS : str
        Especialidad en ortopedia.
    CARDIOLOGY : str
        Especialidad en cardiología.
    OPHTHALMOLOGY : str
        Especialidad en oftalmología.
    NEUROLOGY : str
        Especialidad en neurología.

    Métodos:
    --------
    choices():
        Devuelve una lista de tuplas con las especialidades disponibles.
    """
    GENERAL = "General"
    SURGERY = "Cirugía"
    DERMATOLOGY = "Dermatología"
    ORTHOPEDICS = "Ortopedia"
    CARDIOLOGY = "Cardiología"
    OPHTHALMOLOGY = "Oftalmología"
    NEUROLOGY = "Neurología"

    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]

def validate_client(data):
    """
    Valida los datos de un cliente.

    Args:
        data (dict): Diccionario con los datos del cliente.

    Returns:
        dict: Diccionario con los errores de validación.
    """
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    elif str(phone).startswith("54") == False:
        errors["phone"] = "Por favor el telefono debe iniciar con 54"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors

def validate_provider(data):
    """
    Valida los datos de un proveedor.

    Args:
        data (dict): Diccionario con los datos del proveedor.

    Returns:
        dict: Diccionario con los errores de validación.
    """
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors

def validate_vet(data):
    """
    Valida los datos de un veterinario.

    Args:
        data (dict): Diccionario con los datos del veterinario.

    Returns:
        dict: Diccionario con los errores de validación.
    """
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")
    specialty = data.get("specialty", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"
    
    if specialty == "":
        errors["specialty"] = "Por favor ingrese una especialidad"
    elif specialty not in [key.value for key in Specialty]:
        errors["specialty"] = "Por favor ingrese una especialidad valida"

    return errors


class Vet(models.Model):
    """
    Modelo para representar un veterinario.

    Atributos:
    ----------
    name : str
        Nombre del veterinario.
    phone : str
        Teléfono del veterinario.
    email : str
        Correo electrónico del veterinario.
    specialty : str
        Especialidad del veterinario, seleccionada de la enumeración Specialty.

    Métodos:
    --------
    __str__():
        Devuelve una representación en cadena del nombre del veterinario.
    save_vet(vet_data):
        Guarda un nuevo veterinario en la base de datos si los datos son válidos.
    update_vet(vet_data):
        Actualiza los datos de un veterinario existente.
    """
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    specialty = models.CharField(max_length=50, choices=Specialty.choices(), default=Specialty.GENERAL.value)

    def __str__(self):
        return self.name

    @classmethod
    def save_vet(vet, vet_data):
        errors = validate_vet(vet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Vet.objects.create(
            name=vet_data.get("name"),
            phone=vet_data.get("phone"),
            email=vet_data.get("email"),
            specialty=vet_data.get("specialty"),
        )

        return True, None

    def update_vet(self, vet_data):
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone
        self.specialty = vet_data.get("specialty", "") or self.specialty

        self.save()

def validate_product(data):
    """
    Valida los datos de un producto.

    Args:
        data (dict): Diccionario con los datos del producto.

    Returns:
        dict: Diccionario con los errores de validación.
    """
    errors = {}

    name = data.get("name", "")
    type = data.get("type", "")
    price = data.get("price", "")
    provider = data.get("provider", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if type == "":
        errors["type"] = "Por favor ingrese un tipo"

    if price == "":
        errors["price"] = "Por favor ingrese un precio"
    try:
        float_price = float(price)
        if float_price <= 0:
            errors["price"] = "Por favor ingrese un precio mayor que 0"
        integer_part, decimal_part = str(float_price).split(".")
        if len(decimal_part) > 2:
            errors["price"] = "Por favor ingrese un precio con maximo 2 decimales"
    except ValueError:
        errors["price"] = "Por favor ingrese un precio valido"

    if not provider:
        errors["provider"] = "Por favor seleccione un proveedor"

    return errors

def validate_pet(data):
    """
    Valida los datos de una mascota.

    Args:
        data (dict): Diccionario con los datos de la mascota.

    Returns:
        dict: Diccionario con los errores de validación.
    """
    errors = {}

    name = data.get("name", "")
    cliente = data.get("client", "")
    breed = data.get("breed", "")
    birthday = data.get("birthday","")
    weight = data.get("weight","")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if cliente == "":
        errors["cliente"] = "Por favor seleccione un cliente"

    if breed == "":
        errors["breed"] = "Por favor ingrese una raza"
    if birthday == "":
        errors["birthday"] = "Por favor ingrese la fecha de cumpleaños"
    if weight == "":
        errors["weight"] = "Por favor ingrese un peso"
    try:
        float_weight = float(weight)
        if float_weight<=0:
            errors["weight"] = "Por favor ingrese un peso mayor que 0"
        decimal_part = str(float_weight).split(".")
        if len(decimal_part)>2:
            errors["weight"] = "Por favor ingrese un peso con maximo 2 decimales"
    except ValueError:
        errors["weight"] = "Por favor ingrese un peso valido"
    return errors
                
class Provider(models.Model):
    """
    Modelo para representar un proveedor.

    Atributos:
    ----------
    name : str
        Nombre del proveedor.
    email : str
        Correo electrónico del proveedor.
    address : str, opcional
        Dirección del proveedor.

    Métodos:
    --------
    __str__():
        Devuelve una representación en cadena del nombre del proveedor.
    save_provider(provider_data):
        Guarda un nuevo proveedor en la base de datos si los datos son válidos.
    update_provider(provider_data):
        Actualiza los datos de un proveedor existente.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
    
    @classmethod
    def save_provider(cls, provider_data):
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            email=provider_data.get("email"),
            address=provider_data.get("address"),
        )
        return True, None
    
    def update_provider(self, provider_data):
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        self.address = provider_data.get("address", "") or self.address

        self.save()
    
class Product(models.Model):
    """
    Modelo para representar un producto.

    Atributos:
    ----------
    name : str
        Nombre del producto.
    type : str
        Tipo del producto.
    price : float
        Precio del producto.
    provider : ForeignKey
        Proveedor del producto.

    Métodos:
    --------
    __str__():
        Devuelve una representación en cadena del nombre del producto.
    save_product(product_data):
        Guarda un nuevo producto en la base de datos si los datos son válidos.
    update_product(product_data):
        Actualiza los datos de un producto existente.
    """
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    price = models.FloatField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_product(cls, product_data):
        errors = validate_product(product_data)

        if len(errors.keys()) > 0:
            return False, errors
        provider_id = product_data.get("provider")
        provider_instance = Provider.objects.get(id=provider_id)

        Product.objects.create(
            name=product_data.get("name"),
            type=product_data.get("type"),
            price=product_data.get("price"),
            provider = provider_instance,
        )
        return True, None
    
    def update_product(self, product_data):
        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        try:
            self.price = float(product_data.get("price", "")) or self.price
        except ValueError:
            pass

        self.save()

class Client(models.Model):
    """
    Modelo para representar un cliente.

    Atributos:
    ----------
    name : str
        Nombre del cliente.
    phone : int
        Número de teléfono del cliente.
    email : str
        Correo electrónico del cliente.
    address : str, opcional
        Dirección del cliente.
    products : ManyToManyField
        Productos asociados al cliente.

    Métodos:
    --------
    __str__():
        Devuelve una representación en cadena del nombre del cliente.
    save_client(client_data):
        Guarda un nuevo cliente en la base de datos si los datos son válidos.
    update_client(client_data):
        Actualiza los datos de un cliente existente.
    """
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)
    products = models.ManyToManyField(Product)

    def str(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address

        self.save()

def validate_medicine(data):
    """
    Valida los datos de una medicina.

    Args:
        data (dict): Diccionario con los datos de la medicina.

    Returns:
        dict: Diccionario con los errores de validación.
    """
    errors = {}

    name = data.get("name", "")
    description = data.get("description", "")
    dose = data.get("dose", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if description == "":
        errors["description"] = "Por favor ingrese una descripcion"

    if dose == "":
        errors["dose"] = "Por favor ingrese una dosis"
    else:
        try:
            float_dose = float(dose)
            if float_dose <= 0:
                errors["dose"] = "Por favor ingrese una dosis mayor que 0"
            elif float_dose < 1 or float_dose > 10:
                errors["dose"] = "Por favor ingrese una dosis entre 1 y 10"
            else:
                integer_part, decimal_part = str(float_dose).split(".")
                if len(decimal_part) > 2:
                    errors["dose"] = "Por favor ingrese una dosis con maximo 2 decimales"
        except ValueError:
            errors["dose"] = "Por favor ingrese una dosis valida"

    return errors


class Medicine(models.Model):
    """
    Modelo para representar una medicina.

    Atributos:
    ----------
    name : str
        Nombre de la medicina.
    description : str
        Descripción de la medicina.
    dose : float
        Dosis de la medicina.

    Métodos:
    --------
    __str__():
        Devuelve una representación en cadena del nombre de la medicina.
    save_medicine(medicine_data):
        Guarda una nueva medicina en la base de datos si los datos son válidos.
    update_medicine(medicine_data):
        Actualiza los datos de una medicina existente.
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    dose = models.FloatField()
#    pets = models.ManyToManyField('Pet', related_name='medicines')

    def __str__(self):
        return self.name

    @classmethod
    def save_medicine(cls, medicine_data):
        errors = validate_medicine(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        Medicine.objects.create(
            name=medicine_data.get("name"),
            description=medicine_data.get("description"),
            dose=medicine_data.get("dose"),
        )
    
        return True, None
    
    def update_medicine(self, medicine_data):
        self.name =medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", "") or self.dose

        self.save()

class Pet(models.Model):
    """
    Modelo para representar una mascota.

    Atributos:
    ----------
    name : str
        Nombre de la mascota.
    breed : str
        Raza de la mascota.
    birthday : DateField
        Fecha de cumpleaños de la mascota.
    weight : float
        Peso de la mascota.
    client : ForeignKey
        Cliente al que pertenece la mascota.
    medicines : ManyToManyField
        Medicinas asociadas a la mascota.
    vets : ManyToManyField
        Veterinarios asociados a la mascota.

    Métodos:
    --------
    __str__():
        Devuelve una representación en cadena del nombre de la mascota.
    save_pet(pet_data):
        Guarda una nueva mascota en la base de datos si los datos son válidos.
    update_pet(pet_data):
        Actualiza los datos de una mascota existente.
    """
    name=models.CharField(max_length=100)
    breed=models.CharField(max_length=100)
    birthday=models.DateField(verbose_name="Fecha de Cumpleaños")
    weight=models.FloatField()
    client = models.ForeignKey(Client,on_delete=models.CASCADE, null=True)
    medicines = models.ManyToManyField(Medicine)
    vets = models.ManyToManyField(Vet)

    def __str__(self):
        return self.name
    
    @classmethod
    def save_pet(cls,pet_data):
        errors = validate_pet(pet_data)

        if len(errors.keys()) > 0:
            return False, errors
        client2=Client.objects.get(id=pet_data.get("client"))
        Pet.objects.create(
            name = pet_data.get("name"),
            breed= pet_data.get("breed"),
            birthday = pet_data.get("birthday"),
            weight = pet_data.get("weight"),
            client = client2
        )

        return True, None
    
    def update_pet(self, pet_data):
        self.name = pet_data.get("name","") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday
        self.weight = pet_data.get("weight", "") or self.weight

        self.save()    



