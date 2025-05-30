from django.core.management.base import BaseCommand
from accounts.models import Users
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Hashes password for user kadirzeybekoglu"

    def handle(self, *args, **kwargs):
        try:
            # "kadirzeybekoglu" kullanıcısını bul
            user = Users.objects.get(username="salihkutukte")
            
            # Mevcut şifreyi al ve hash'le
            plain_password = user.password_hash  # Mevcut şifre düz metin
            user.password_hash = make_password(plain_password)
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f"Successfully hashed password for kadirzeybekoglu"))
            
        except Users.DoesNotExist:
            self.stdout.write(self.style.ERROR("User kadirzeybekoglu not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))