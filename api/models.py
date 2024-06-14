from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Libro(models.Model):
    titolo = models.CharField(max_length = 255)
    autore = models.CharField(max_length = 255)
    isbn = models.CharField(max_length = 255)
    pubyear = models.CharField(max_length = 255)

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libri"

    def __str__(self):
        return self.titolo
    
class Preferiti(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Preferiti"
        verbose_name_plural = "Preferiti"
    
    def __str__(self):
        return f"{self.utente.username} - {self.libro.titolo}"