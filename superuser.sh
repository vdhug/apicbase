echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@apicbase.com', 'pass')" | python manage.py shell
echo "Superuser created"
