from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),
    path("clientes/agregar-producto/<int:id>/", view=views.clients_add_product, name="clients_add_product"),
    path("clientes/seleccionar-productos/", views.select_products_to_delete, name='select_products_to_delete'),
    path("clientes/eliminar-productos/", views.delete_selected_products, name='delete_selected_products'),

    path("proveedores/", view=views.providers_repository, name="providers_repo"),
    path("proveedores/nuevo/", view=views.providers_form, name="providers_form"),
    path("proveedores/editar/<int:id>/", view=views.providers_form, name="providers_edit"),
    path("proveedores/eliminar/", view=views.providers_delete, name="providers_delete"),

    path("productos/", view=views.products_repository, name="products_repo"),
    path("productos/nuevo/", view=views.product_form, name="products_form"),
    path("productos/editar/<int:id>/", view=views.product_form, name="products_edit"),
    path("productos/eliminar/", view=views.products_delete, name="products_delete"),
    
    path("vets/", view=views.vets_repository, name="vets_repo"),
    path("vets/nuevo/", view=views.vets_form, name="vets_form"),
    path("vets/editar/<int:id>/", view=views.vets_form, name="vets_edit"),
    path("vets/eliminar/", view=views.vets_delete, name="vets_delete"),
    
    path("medicine/", view=views.medicine_repository, name="medicine_repo"),
    path("medicine/nuevo/", view=views.medicine_form, name="medicine_form"),
    path("medicine/editar/<int:id>/", view=views.medicine_form, name="medicine_edit"),
    path("medicine/eliminar/", view=views.medicine_delete, name="medicine_delete"),

    path("mascotas/", view=views.pets_repository, name="pets_repo"),
    path("mascotas/nuevo/", view=views.pets_form, name="pets_form"),
    path("mascotas/editar/<int:id>/", view=views.pets_form, name="pets_edit"),
    path("mascotas/eliminar", view=views.pets_delete, name="pets_delete"),

    path("mascotas/agregar-medicina/<int:id>/", view=views.pets_add_medicine, name="pets_add_medicine"),
    path("mascotas/seleccionar-medicinas/", view=views.select_medicines_to_delete, name="select_medicines_to_delete"),
    path("mascotas/eliminar-medicinas/", view=views.delete_selected_medicines, name="delete_selected_medicines"),

    path("mascotas/agregar-veterinario/<int:id>/", view=views.pets_add_vet, name="pets_add_vet"),
    path("mascotas/seleccionar-veterinarios/", view=views.select_vets_to_delete, name="select_vets_to_delete"),
    path("mascotas/eliminar-veterinarios/", view=views.delete_selected_vets, name="delete_selected_vets"),

]
