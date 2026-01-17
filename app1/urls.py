from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('view_book/',views.view_book,name="book"),
    path('create_book/',views.create_book,name="createbook"),
    path('update_book/<int:id>',views.update_book,name="update_book"),
    path('delete_book/<int:id>',views.delete_book,name="delete_book"),
    path('registration/',views.regview,name="reg"),
    path('login/',views.loginview,name="login"),
    path('logout/',views.logoutview,name="logout"),
    path('cart/',views.cartview,name="cart"),
    path('addcart/<int:id>',views.addcart,name="addcart"),
    path('removecartitem/<int:id>',views.removecartitem,name="remove_cart_item"),
    path('buy_now/<int:book_id>',views.buy_now,name="buy"),
    path('payment_success/',views.payment_success,name="payment_success"),
    path('payment_cancel/',views.payment_cancel,name="payment_cancel"),
    path('buy_all/', views.buy_all_cart, name="buy_all"),
    path('remove_all/', views.remove_all_item, name="remove_all"),

]