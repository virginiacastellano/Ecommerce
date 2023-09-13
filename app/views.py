from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from . models import Cart, Customer, Product
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

def home(request):
    return render(request,"app/home.html")


def about(request):
    return render(request,"app/about.html")

@login_required
def contact(request):
    return render(request,"app/contact.html")
  
# renderisamos las categorias

class CategoryView(View):
    def get(self,request, val):
        product= Product.objects.filter(category=val)
        title= Product.objects.filter(category=val).values('title')       
        return render(request,"app/category.html", locals())


class CategoryTitle(View):
    def get(self,request, val):
        product= Product.objects.filter(title=val)
        title= Product.objects.filter(category=product[0].category).values('title')       
        return render(request,"app/category.html", locals())

  
class ProductDetail(View):
    def get(self,request,pk):
        product= Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html", locals()) 
    
   

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,"app/customerregistration.html", locals()) 
    def post(self,request):
        form= CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations! User Register Successfully')
        else:
            messages.warning(request,"Invalid Inpit Data")
        return render(request,"app/customerregistration.html", locals())


@method_decorator(login_required, name='dispatch')    
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,"app/profile.html", locals())

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile save successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,"app/profile.html", locals())


@login_required
def address(request):
    add= Customer.objects.filter(user=request.user)
    return render(request,"app/address.html", locals())

@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add= Customer.objects.get(pk=pk)
        form= CustomerProfileForm(instance=add) #gracias a django la recupercion de datos es muy facil 
        return render(request,"app/updateAddress.html", locals())
    def post(self,request,pk):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            # Obtener la instancia del cliente existente
            add = Customer.objects.get(pk=pk)
            # Actualizar los campos con los datos del formulario
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.mobile = form.cleaned_data['mobile']
            add.city = form.cleaned_data['city']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            # Guardar los cambios en la base de datos
            add.save()
            messages.success(request,"Congratulations! Profile save successfully")
        else:
            messages.warning(request,"Invalid Input Data")
            
        return redirect('address')

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)

    # Verificar si el producto ya está en el carrito del usuario
    existing_cart_item = Cart.objects.filter(user=user, product=product).first()

    if existing_cart_item:
        # Si el producto ya está en el carrito, simplemente actualiza la cantidad
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    else:
        # Si no está en el carrito, crea un nuevo registro
        Cart(user=user, product=product).save()

    return redirect("/cart")


@login_required
def show_cart(request):
    user=request.user
    cart= Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value= p.quantity*p.product.discounted_price
        amount= amount + value
    totalamount = amount+ 40
    return render(request, "app/addtocart.html", locals())

@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount= 0
        for p in cart_items:
            value= p.quantity*p.product.discounted_price
            famount= famount + value
        totalamount= famount + 40
    
        return render(request,'app/checkout.html',locals())
    

@login_required   
def order_summary(request):
    # Obtén los elementos del carrito del usuario actual
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    # Calcula el monto total
    totalamount = 0
    for item in cart_items:
        totalamount += item.quantity * item.product.discounted_price
       # Suma $40 al monto total por envío
    totalamount += 40

    return render(request, 'app/order_summary.html', {'cart_items': cart_items, 'totalamount': totalamount})

# incremento y decremento del carrito

def plus_cart(request):
    if request.method == 'GET' :
        prod_id= request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user= request.user
        cart= Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value= p.quantity*p.product.discounted_price
            amount= amount + value
        totalamount = amount+ 40   
        data={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }    
        return JsonResponse(data)



def minus_cart(request):
    if request.method == 'GET' :
        prod_id= request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user= request.user
        cart= Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value= p.quantity * p.product.discounted_price
            amount= amount + value
        totalamount = amount+ 40   
        data={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }    
        return JsonResponse(data)
    


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')  # Obtén el ID del producto
        user = request.user

        # Busca el registro en el carrito para el producto y usuario específicos
        cart_item = Cart.objects.filter(user=user, product_id=prod_id).first()

        if cart_item:
            cart_item.delete()  # Elimina el registro si existe

        # Recalcula el monto total y otros datos
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
 
 
@login_required   
def search(request):
    query= request.GET['search']
    totalitem=0
    #wishitem=0
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
        # wishitem= len(Wishlist.objects.filter(user=request.user))
    product= Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html", locals())