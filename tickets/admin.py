from django.contrib import admin
from .models import Movie,Guest,Reserveration,Post
# Register your models here.

admin.site.register(Guest)
admin.site.register(Movie)
admin.site.register(Reserveration)
admin.site.register(Post)