from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from urllib import request
from django.views import View
from .models import Product,Customer,Cart,Payment,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import login
import time
from django.db.models import Q 
import razorpay
from django.conf import settings

# Create your views here.
def home(request):
    product = Product.objects.all()
    s = len(product)//3
    Final = []
    temp= []
    for j in range(s):
        temp = [product[j*3], product[j*3+1] , product[j*3+2]]
        Final.append(temp)
        temp = []
    for i in range((len(product)//3)*3,len(product)):
        temp.append(product[i])
    if temp:
        Final.append(temp)
    len_cart = 0
    if request.user.is_authenticated:
        len_cart = len(Cart.objects.filter(user = request.user))
    return render(request, 'app/home.html',locals())


def about(request):
    len_cart = 0
    if request.user.is_authenticated:
        len_cart = len(Cart.objects.filter(user = request.user))
    return render(request, 'app/about.html',locals())


def contact(request):
    len_cart = 0
    if request.user.is_authenticated:
        len_cart = len(Cart.objects.filter(user = request.user))
    return render(request, 'app/contact.html',locals())


class Categoryview(View):
    def get(self,request,val):
        len_cart = 0
        if request.user.is_authenticated:
            len_cart = len(Cart.objects.filter(user = request.user))
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title')
        return render(request , 'app/category.html',locals())
    

class CategoryTitle(View):
    def get(self,request,val):
        len_cart = 0
        if request.user.is_authenticated:
            len_cart = len(Cart.objects.filter(user = request.user))
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category = product[0].category).values('title')
        return render(request , 'app/category.html',locals())
    

class ProductDetail(View):
    def get(self,request,pk):
        len_cart = 0
        if request.user.is_authenticated:
            len_cart = len(Cart.objects.filter(user = request.user))
        product = Product.objects.get(pk = pk)
        return render(request, 'app/productdetail.html',locals())
    

class CustomerRegistrationView(View):
    def get(self,request):
        len_cart = 0
        if request.user.is_authenticated:
            len_cart = len(Cart.objects.filter(user = request.user))
        form = CustomerRegistrationForm()
        return render(request, 'app/registration.html',locals())
    def post(self,request):
        len_cart = 0
        if request.user.is_authenticated:
            len_cart = len(Cart.objects.filter(user = request.user))
        form = CustomerRegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,"Congratulations! User Register Successfully")
            return redirect('home')
        else:
            messages.warning(request,'Invalid Input Data')
            return render(request, 'app/registration.html',locals())
        

class ProfileView(View):
    def get(self,request):
        len_cart = 0
        if request.user.is_authenticated:
            len_cart = len(Cart.objects.filter(user = request.user))
        form = CustomerProfileForm()
        return render(request,'app/profile.html',locals())
    def post(self,request):
        len_cart = 0
        if request.user.is_authenticated:
            len_cart = len(Cart.objects.filter(user = request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user = user , name = name , locality = locality , mobile = mobile , city = city , state = state , zipcode = zipcode)
            reg.save()
            messages.success(request, "Congratulations ! Profile Save Successfully")
            return redirect('address')
        else:
            messages.warning(request,"Invalid Input Data")
            return render(request,'app/profile.html',locals())
    
def Address(request):
    len_cart = 0
    if request.user.is_authenticated:
        len_cart = len(Cart.objects.filter(user = request.user))
    add = Customer.objects.filter(user = request.user)
    return render(request,'app/address.html' , locals())

class updateAddressView(View):
    def get(self,request,pk):
        len_cart = 0
        if request.user.is_authenticated:
            len_cart = len(Cart.objects.filter(user = request.user))
        add = Customer.objects.get(pk = pk)
        form = CustomerProfileForm(instance=add)
        return render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        len_cart = 0
        if request.user.is_authenticated:
            len_cart = len(Cart.objects.filter(user = request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Successfully Updated")
            time.sleep(2)
            return redirect('address')
        else:
            messages.warning(request,"Invalid Input Data")
            return render(request,'app/updateAddress.html',locals())
        

def cart(request):
    len_cart = 0
    if request.user.is_authenticated:
        len_cart = len(Cart.objects.filter(user = request.user))
    user = request.user
    cart = Cart.objects.filter(user = user)
    ammount = 0
    shipping = 40
    for p in cart:
        value = p.quantity * p.product.discounted_price
        ammount = ammount + value
    totalammount = ammount + shipping
    return render(request, 'app/cart.html', locals())


def add_cart(request):
    len_cart = 0
    if request.user.is_authenticated:
        len_cart = len(Cart.objects.filter(user = request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    product =  Product.objects.get(id = product_id)
    try:
        c = Cart.objects.get(Q(product = product_id) & Q(user = request.user))
    except:
        Cart(user = user , product = product).save()  
    else:
        messages.success(request,'This Item is already in cart')
   
    return redirect('cart')


def plus_cart(request):
    len_cart = 0
    if request.user.is_authenticated:
        len_cart = len(Cart.objects.filter(user = request.user))
    if request.method == "GET":
        shipping = 40
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user = user)
        ammount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            ammount = ammount + value
        totalammount = ammount + 40
        data = { 
            'quantity' : c.quantity,
            'amount':ammount,
            'totalamount' : totalammount,
            'shipping' : shipping
        }
        return JsonResponse(data)


def minus_cart(request):
    len_cart = 0
    if request.user.is_authenticated:
        len_cart = len(Cart.objects.filter(user = request.user))
    shipping = 40
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        if c.quantity > 1:
            c.quantity -= 1
            c.save()
        user = request.user
        cart = Cart.objects.filter(user = user)
        ammount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            ammount = ammount + value
        totalammount = ammount + 40
        if not cart:
            totalammount = 0
        data = {
            'quantity' : c.quantity,
            'amount':ammount,
            'totalamount' : totalammount,
            'shipping' : shipping
        }
        return JsonResponse(data)
    
def remove_cart(request):
    len_cart = 0
    if request.user.is_authenticated:
        len_cart = len(Cart.objects.filter(user = request.user))
    if request.method == "GET":
        shipping = 40
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user = user)
        ammount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            ammount = ammount + value
        totalammount = ammount + shipping
        if len(cart) == 0:
            totalammount = 0
            shipping = 0
        data = {
            'amount':float(ammount),
            'totalamount' : float(totalammount),
            'shipping' : float(shipping)

        }
        return JsonResponse(data)
    

class check_out(View):
    def get(self,request):
        len_cart = 0
        if request.user.is_authenticated:
            len_cart = len(Cart.objects.filter(user = request.user))
        user = request.user
        add = Customer.objects.filter(user = user)
        cart_items = Cart.objects.filter(user = user)
        ammount = 0
        shipping = 40
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            ammount = ammount + value
        totalamount = ammount + shipping
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment_response = client.order.create(data=data)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status,

            )
            payment.save()
        return render(request, 'app/checkout.html', locals())

def payment_done(request):
    len_cart = 0
    if request.user.is_authenticated:
        len_cart = len(Cart.objects.filter(user = request.user))
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id = cust_id)
    add = customer.locality + " " + customer.city + " " + customer.state + "-" + str(customer.zipcode)
    payment = Payment.objects.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_order_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user = user)
    for c in cart:
        OrderPlaced(user = user ,customer = customer,product = c.product,quantity = c.quantity,payment = payment,address = add).save()
        c.delete()
    return redirect('orders')

def orders(request):
    len_cart = 0
    if request.user.is_authenticated:
        len_cart = len(Cart.objects.filter(user = request.user))
    order_placed = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'app/order.html' , locals())