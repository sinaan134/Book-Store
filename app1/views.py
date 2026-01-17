from django.shortcuts import render,redirect,get_object_or_404
from . models import Book,Cart
from . forms import BookForm
from . forms import UpdateForm ,RegForm , LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY




# Create your views here.

# def home(request):
#     a={
#         "name":"nihal",
#         "age":21,
#         "place":"malappuram"
#     }
#     return render(request,"home.html",a)

def home(request):
    a = ["nihal",21,"malappuram"]
    return render(request,"home.html",{"a":a})#home view

def about(request):
    return render(request,"about.html")

@login_required
def view_book(request):
    a = Book.objects.all()
    return render(request,"view_book.html",{"data":a})

@login_required
def create_book(request):
    b = BookForm(request.POST or None,request.FILES or None)
    if b.is_valid():
        b.save()
        return redirect('book')
    return render(request,"create_book.html",{"form":b})

@login_required
def update_book(request,id):
    a = Book.objects.get(id=id)
    d = UpdateForm(request.POST or None,request.FILES or None, instance = a)
    if d.is_valid():
        d.save()
        return redirect('book')
    return render(request,"update_book.html",{"form":d})

@login_required
def delete_book(request,id):
    a = Book.objects.get(id=id)
    if request.method == 'POST':
        a.delete()
        return redirect('book')
    return render(request,'delete_book.html',{"data":a})

def regview(request):
    r = RegForm(request.POST or None)
    if request.method == 'POST' and r.is_valid():
        r.save()
        return redirect('book')
    return render(request,'registration.html',{'form':r})

def loginview(request):
    l = LoginForm(request,data=request.POST or None)
    if request.method == 'POST' and l.is_valid():
        user = l.get_user()
        login(request,user)
        return redirect('book')
    return render(request,'login.html',{"form":l})

def logoutview(request):
    logout(request)
    return redirect('home')

@login_required
def cartview(request):
    a = Cart.objects.filter(user=request.user)
    return render(request,'cart.html',{"data":a})

def addcart(request,id):
    a=Book.objects.get(id=id)
    cart_item,created=Cart.objects.get_or_create(book=a ,user=request.user)
    if not created:
        cart_item.quantity+=1
        cart_item.save()
    return redirect('cart')
from django.shortcuts import get_object_or_404, redirect

def removecartitem(request, id):
   
    cart_item = Cart.objects.get( id=id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
      
        cart_item.delete()
        
    return redirect('cart')
@login_required
def buy_now(request, book_id):
    cart_items = get_object_or_404(Cart, user=request.user, book_id=book_id)
    book=cart_items.book

    session=stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'inr',
                    'product_data':{    
                        'name':book.name,
                    },
                    'unit_amount': int(float(book.price) * 100),

                },
                'quantity':cart_items.quantity, 
            }
        ],

        mode="payment", 
        success_url=request.build_absolute_uri(reverse('payment_success')),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
        
    )
    return redirect(session.url)


def payment_success(request):
    return render(request,"sucess.html")
        
    

def payment_cancel(request):
    return render(request,"cart.html")


@login_required
def buy_all_cart(request):
   
    cart_items = Cart.objects.filter(user=request.user)
 
    if not cart_items.exists():
        return redirect('cart') 

    
    line_items_list = []
    for item in cart_items:
        line_items_list.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item.book.name,  
                },
                'unit_amount': int(float(item.book.price) * 100),
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items_list,  
        mode="payment",
        success_url=request.build_absolute_uri(reverse('payment_success')),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
    )
    
    return redirect(session.url)

def remove_all_item(request):
    cart_items = Cart.objects.filter(user=request.user)
 
    if  cart_items.exists():
        cart_items.delete()
        return render(request,"cart.html") 