# Vetsoft

Aplicación web para veterinarias utilizada en la cursada 2024 de Ingeniería y Calidad de Software. UTN-FRLP

## Dependencias

- python 3
- Django
- sqlite
- playwright
- ruff

## Instalar dependencias

`pip install -r requirements.txt`

## Iniciar la Base de Datos

`python manage.py migrate`

## Iniciar app

`python manage.py runserver`

## Crear la imagen de docker

`docker build -t vetsoft-app:Version .`

## Desplegar el contenedor de docker

`$ docker run --name actividad-2 -p 8000:8000 vetsoft-app:Version`


NOMBRE DE LOS INTEGRANTES:

        - Iñaki Jose Zelayeta
        - Bruno Alejo Santillan
        - Katerina Mariescurrena 
        - Lautaro Frias

INFORMACION:

1. Version actual de la imagen Docker utilizada:

        vetsoft-app:1.0

2. Formato de escritura de los commits:

        <tipo> [optional scope]:<descripcion>
        ^----^ ^--------------^ ^-----------^   
        |     |                 |
        |     |                 +-->Descripción del commit
        |     |    
        |     +---------------------->Sirve para especificar el alcance del commit. Por ejemplo: especificar el paquete que estamos modificando.
        |
        +----------------------------->Tipos de commits: feat, fix, docs, style, chore, build, refactor, test.

        - EJEMPLO
                - feat(Component): Se agrego nuevo funcionalidad.

3. Significado de cada tipo de commit:

        - feat: 
                - Se utiliza para indicar la adición de una nueva funcionalidad al software. Por ejemplo, «feat: Añadir funcionalidad de búsqueda».

        - fix: 
                - Este tipo se usa para commits que corrigen errores o problemas existentes en el código. Por ejemplo, «fix: Corregir error de validación de formulario».

        - doc: 
                - Reservado para commits relacionados con la documentación del proyecto, como actualizaciones en documentos o comentarios en el código. Por ejemplo, «docs: Actualizar la guía del usuario».

        - style: 
                - Se utiliza para cambios que afectan solo al estilo del código, como la formateación, el espaciado o la indentación. Por ejemplo, «style: Ajustar formateo del código».

        - chore: 
                - Este tipo de commit está destinado a tareas de mantenimiento general o actividades que no encajan en las categorías anteriores.Por ejemplo, «chore: Limpiar archivos no utilizados».

        - build: 
                - Cambios que afectan el sistema de compilación o dependencias externas.Por ejemplo: «build(Electron): Bump version 7 to 9».

        - ci: 
                - Cambios en nuestros archivos y scripts de configuración de integración continua.

        - perf: 
                - Un cambio de código que mejora el rendimiento.

        - refacto: 
                - Un cambio de código que no corrige un error ni agrega una característica.

        - test: 
                - Agregar pruebas faltantes o corregir pruebas existentes.


4. Formato de escritura: 

        snake_case: palabras separadas por barra baja en vez de espacios y 
        con la primera letra de cada palabra en minúscula. 

        Por ejemplo: mi_blog_de_desarrollo.

        Este tipo de convención seran utilizados para nombres de variables y funciones.
