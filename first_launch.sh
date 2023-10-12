./manage.py migrate
./manage.py loaddata scp_app/fixtures/producto.json
./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"