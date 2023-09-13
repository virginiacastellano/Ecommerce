from django.contrib import admin
from .models import Cart, Customer, Product, Payment, OrderPlaced
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.

# Registra el modelo Product en el panel de administración
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','discounted_price','category','product_image']

# Registra el modelo Customer en el panel de administración
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','locality','city','state','zipcode']

# Registra el modelo Cart en el panel de administración
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','products','quantity']
    
    # Define una función para mostrar enlaces a las páginas de edición de productos en el panel de administración
    def products(self, obj):
        # Genera un enlace a la página de edición del producto usando el ID del producto
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

# Registra el modelo Payment en el panel de administración
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

# Registra el modelo OrderPlaced en el panel de administración
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity','order_date','status','payment']