# Importa las bibliotecas necesarias
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from . models import Cart, Customer, Product
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Función para la página de inicio
def home(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, "app/home.html",locals())

# Función para la página "Acerca de"
def about(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, "app/about.html",locals())

# Función para la página de contacto, requiere inicio de sesión
@login_required
def contact(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, "app/contact.html", locals())

# Clase para ver productos por categoría
class CategoryView(View):
    def get(self, request, val):
        totalitem=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())

# Clase para ver productos por título de categoría
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
        return render(request, "app/category.html", locals())

# Clase para ver detalles de un producto
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        totalitem=0
        if request.user.is_authenticated:
             totalitem= len(Cart.objects.filter(user=request.user))
        return render(request, "app/productdetail.html", locals())

# Clase para el registro de clientes
class CustomerRegistrationView(View):
    def get(self, request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! Successfully registered user')
        else:
            messages.warning(request, "Invalid input data")
        return render(request, "app/customerregistration.html", locals())

# Clase para ver el perfil de un cliente, requiere inicio de sesión
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
        return render(request, "app/profile.html", locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile successfully saved")
        else:
            messages.warning(request, "Invalid input data")
        return render(request, "app/profile.html", locals())

# Función para ver las direcciones de un cliente, requiere inicio de sesión
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem=0
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, "app/address.html", locals())

# Clase para actualizar una dirección de cliente, requiere inicio de sesión
@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self, request, pk):
        totalitem=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, "app/updateAddress.html", locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.mobile = form.cleaned_data['mobile']
            add.city = form.cleaned_data['city']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile successfully saved")
        else:
            messages.warning(request, "Invalid input data")
        return redirect('address')

# Función para agregar productos al carrito, requiere inicio de sesión
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    existing_cart_item = Cart.objects.filter(user=user, product=product).first()

    if existing_cart_item:
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    else:
        Cart(user=user, product=product).save()
    return redirect("/cart")

# Función para mostrar el carrito de compras, requiere inicio de sesión
@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0

    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem=0
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    return render(request, "app/addtocart.html", locals())

# Clase para la página de pago, requiere inicio de sesión
@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0

        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40

        return render(request, 'app/checkout.html', locals())

# Función para ver un resumen de la orden, requiere inicio de sesión
@login_required
def order_summary(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    totalamount = 0

    for item in cart_items:
        totalamount += item.quantity * item.product.discounted_price
    totalamount += 40
    return render(request, 'app/order_summary.html', {'cart_items': cart_items, 'totalamount': totalamount})

# Función para aumentar la cantidad de un producto en el carrito
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0

        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

# Función para reducir la cantidad de un producto en el carrito
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0

        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

# Función para eliminar un producto del carrito
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        cart_item = Cart.objects.filter(user=user, product_id=prod_id).first()

        if cart_item:
            cart_item.delete()

        cart = Cart.objects.filter(user=user)
        amount = 0

        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 40

        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

# Función para buscar productos
@login_required
def search(request):
    query = request.GET['search']
    totalitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html", locals())
