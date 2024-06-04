from django.urls import reverse

links = [
    {"label": "Home", "href": reverse("home"), "icon": "bi bi-house-door"},
    {"label": "Clientes", "href": reverse("clients_repo"), "icon": "bi bi-people"},
    {"label": "Productos", "href": reverse("products_repo"), "icon": "bi bi-basket3"},
]


def navbar(request):
    """
        Genera un diccionario de contexto que contiene una lista de enlaces de navegación,
        marcando el enlace activo actual basado en la ruta de la solicitud.

        Args:
            request: El objeto HttpRequest.

        Returns:
            dict: Un diccionario con los enlaces de navegación y su estado activo.
    """
    def add_active(link):
        copy = link.copy()

        if copy["href"] == "/":
            copy["active"] = request.path == "/"
        else:
            copy["active"] = request.path.startswith(copy.get("href", ""))

        return copy

    return {"links": map(add_active, links)}
