from django.core.management.base import BaseCommand
from accounts.models import Users
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Hashes passwords for all users in the database"

    def handle(self, *args, **kwargs):
        # Tüm kullanıcıları getir
        users = Users.objects.all()
        
        if not users:
            self.stdout.write(self.style.WARNING("No users found in the database"))
            return
        
        success_count = 0
        error_count = 0
        
        for user in users:
            try:
                # Doğrudan şifreyi hash'le (kontrol etmeden)
                plain_password = user.password_hash  # Mevcut şifre düz metin
                user.password_hash = make_password(plain_password)
                user.save()
                success_count += 1
                self.stdout.write(f"Successfully hashed password for: {user.username}")
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f"Error hashing password for {user.username}: {str(e)}"))
        
        # Özet bilgi göster
        self.stdout.write(self.style.SUCCESS(f"Process completed: {success_count} passwords hashed, {error_count} errors"))