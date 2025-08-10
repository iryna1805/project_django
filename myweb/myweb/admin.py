from django.contrib import admin
from .models import UserProfile, Product

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age')
    search_fields = ('name', 'email')


admin.site.register(Product)



