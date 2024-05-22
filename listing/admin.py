from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Listing, Category,Transaction

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
    
class ListingAdmin(admin.ModelAdmin):
    list_display = ["title", 'category', "condition", "price", 'created_at']
    prepopulated_fields = {"slug": ("title",)}

class TransactionADmin(admin.ModelAdmin):
    list_display = ["buyer","listing_price","date","status"]

    def buyer(self,obj):
        return obj.buyer.username
    
    def listing_price(self,obj):
        return obj.listing.price
    
admin.site.register(Transaction,TransactionADmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
