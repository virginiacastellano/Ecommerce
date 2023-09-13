from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from . forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    # Rutas para las vistas definidas en views.py
    path("", views.home),  # Página de inicio
    path("about/", views.about, name="about"),  # Página Acerca de
    path("contact/", views.contact, name="contact"),  # Página de contacto
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),  # Vista de categoría
    path("category-title/<val>", views.CategoryTitle.as_view(), name="category-title"),  # Vista de título de categoría
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),  # Detalle de producto
    path("profile/", views.ProfileView.as_view(), name="profile"),  # Vista de perfil de usuario
    path("address/", views.address, name="address"),  # Vista de dirección
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),  # Actualizar dirección

    # Carrito de compras
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),  # Agregar al carrito
    path('cart/', views.show_cart, name='showcart'),  # Mostrar carrito
    path('checkout/', views.checkout.as_view(), name='checkout'),  # Finalizar compra
    path('order_summary/', views.order_summary, name='order_summary'),  # Resumen de la orden

    path('search/', views.search, name="search"),  # Búsqueda de productos

    path('pluscart/', views.plus_cart),  # Aumentar cantidad en el carrito
    path('minuscart/', views.minus_cart),  # Disminuir cantidad en el carrito
    path('removecart/', views.remove_cart),  # Quitar producto del carrito

    # Autenticación y usuarios
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),  # Registro de usuarios
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),  # Inicio de sesión
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),  # Cambio de contraseña
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),  # Contraseña cambiada con éxito
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),  # Cerrar sesión

    # Restablecimiento de contraseña
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),  # Solicitar restablecimiento de contraseña
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),  # Restablecimiento de contraseña solicitado
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),  # Confirmar restablecimiento de contraseña
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),  # Restablecimiento de contraseña completo

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

# Configuración del panel de administración
admin.site.site_header = "Virginia Castellano"
admin.site.site_title = "Virginia Castellano"
admin.site.site_index_title = "Welcome to Virginia Castellano Shop"
