# SCP | Desafío
# Levantar El Proyecto
## Levantar Docker
- docker-compose up -d --build
## Poblar la base de datos
- Ejecutar el script first_launch.sh que carga de productos la bd
  - bash first_launch.sh
- Se creará un superuser al correr el script
  - user: admin
  - password: adminpass
## Test Coverage
If you want to do a test coverage, use this command: coverage run manage.py test -v 2 && coverage report -m 
