from django.contrib import admin
from .models import Coupon

# Register your models here.


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "vaild_from", "vaild_to", "discount", "active")
    list_filter = ("active", "vaild_from", "vaild_to")
    search_fields = ("code",)
