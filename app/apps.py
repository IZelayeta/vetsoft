from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    Configuración de la aplicación.

    La clase `AppConfig` se utiliza para configurar algunos de los atributos de la aplicación.

    Atributos:
    ----------
    default_auto_field : str
        Especifica el tipo de campo automático predeterminado para los modelos en esta aplicación.
    name : str
        Nombre de la aplicación.

    Métodos:
    --------
    ready():
        Método opcional que se puede sobrescribir para ejecutar el código de inicialización cuando la aplicación está lista.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
