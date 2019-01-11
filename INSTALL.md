Proyecto creado en Django

para instalar librerias pip install requirements.txt

para ejecutar el proyecto python manage.py runserver

Para enviar un Post es necerario tener un Token lo pueden generar aqui, creando un usuario

http://localhost:8000/rest-auth/registration/

y luego hacer login para obtener el token

http://localhost:8000/rest-auth/login/

para poder enviar un post dejo un ejemplo dentro de la carpeta Api el archivo llamado request.py

este es el url para el servicio http://127.0.0.1:8000/api/v1/shorturl/
