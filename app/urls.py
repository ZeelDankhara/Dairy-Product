from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('product-detail/<int:pk>',views.ProductDetail.as_view(),name='product-detail'),
    path('category-title/<val>',views.CategoryTitle.as_view(),name='category-title'),
    path('orders/' ,views.orders , name = 'orders'),
   

    path('category/<slug:val>',views.Categoryview.as_view(),name='category'),
    path('profile/',views.ProfileView.as_view(),name='profile'),


    path('cart/' , views.cart,name = 'cart'),
    path('add-cart/' , views.add_cart,name = 'add-cart'),



    path('address/',views.Address,name='address'),
    path('updateAddress/<int:pk>',views.updateAddressView.as_view(),name='updateAddress'),


    path('register/',views.CustomerRegistrationView.as_view(),name='register'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name = 'app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/' , auth_view.LogoutView.as_view(next_page = 'login'),name = "logout"),



    path('password-change/',auth_view.PasswordChangeView.as_view(template_name = 'app/passwordChange.html',form_class=MyPasswordChangeForm,success_url = '/passwordchangedone'),name = 'passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name = 'app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name = 'app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name = 'app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name = 'app/password_reset_confirm.html',form_class= MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete',auth_view.PasswordResetCompleteView.as_view(template_name = 'app/password_reset_complete.html'),name='password_reset_complete'),


    path('pluscart/' , views.plus_cart),
    path('minuscart/' , views.minus_cart),
    path('removecart/' , views.remove_cart),

    path('check-out' , views.check_out.as_view() , name='checkout'),


    path('paymentdone/', views.payment_done,name = 'paymentdone')
   
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
