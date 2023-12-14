from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import *
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
from store.middleware.auth import auth_middleware
from django.utils.decorators import method_decorator
# Create your views here.

class Index(View):
    def post(self,request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        
        request.session['cart'] = cart

        return redirect('index')

    def get(self,request):
        cart = request.session.get('cart')

        if not cart:
            request.session['cart'] = {}
        products = None
        category  = Category.get_all_categories()
        categoryId = request.GET.get('category')
        
        if categoryId:
            products = Product.get_all_products_by_categoryId(categoryId)
        else:
            products = Product.get_all_products()

        return render(request,'home.html',{'products':products,'category':category})




def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html',{})
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        customer = Customer(first_name=first_name,last_name=last_name,phone=phone,email=email,password=password)

        vlaue = {
            'first_name':first_name,
            'last_name':last_name,
            'phone':phone,
            'email':email
        }

         # Validation
        error_message = None
        if (not first_name):
            error_message = "First Name Required"
        elif len(first_name) < 4:
            error_message = "First Name must be 4 character long or more"
        elif (not last_name):
            error_message = "Last Name Required"
        elif len(last_name) <4:
            error_message = "Last Name must be 4 character long or more"
        elif (not phone):
            error_message = "Phone Number Required"
        elif len(phone) <10 :
            error_message = "Phone number must be more than 10 numbers"

        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
        else:
            return render(request,'signup.html',{'error':error_message,'values':vlaue})

        return redirect('index')



        
class Login(View):
    return_url = None
    def get(self,request):
        Login.return_url = request.GET.get('return_url')
        return render(request,'login.html')
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password,customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('index')
            else:
                error_message = "Email or Password Invalid"

        else:
            error_message = "Email or Password Invalid"
        
        print(email,password)
            
        return render(request,'login.html',{'error':error_message})

def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self,request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request,'cart.html',{'products':products})

class Check_out(View):
    def post(self,request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address,phone,customer,products)

        for product in products:
            order = Order(customer = Customer(id=customer),
            product=product,
            price = product.price,
            quantity = cart.get(str(product.id)),
            address=address,
            phone=phone)
            order.save()
        
        request.session['cart'] = {}
        return redirect('cart')


class OrderView(View):
    def get(self,request):
        customer = request.session.get('customer_id')
        orders = Order.get_order_by_customer(customer)
        print(orders)
        orders = orders.reverse()
        return render(request,'order.html',{'orders':orders})














