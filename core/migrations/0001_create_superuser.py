from django.db import migrations
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    User = get_user_model()
    
    username = "admin"
    password = "admin"
    email = ""

    if not User.objects.filter(username=username).exists():
        print(f"Criando superusuário: {username}")
        User.objects.create_superuser(
            username=username,
            password=password,
            email=email
        )
    else:
        print(f"Superusuário '{username}' já existe.")

class Migration(migrations.Migration):

    dependencies = [
        # A dependência anterior foi removida.
        # Podemos deixar vazio ou depender da última migração de autenticação do Django.
        # Para simplificar, vamos depender da migração que cria os grupos de usuários.
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]