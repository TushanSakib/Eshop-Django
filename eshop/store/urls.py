from django.urls import path
from . import views
from .views import Login,Index,Cart,Check_out,OrderView
from store.middleware.auth import auth_middleware
urlpatterns = [
   # path('',views.index,name='index'),
    path('',Index.as_view(),name='index'),
    path('signup',views.signup,name='signup'),
    # path('login',views.login_customer,name="login"),
    path('login',Login.as_view(),name='login'),
    path('logout',views.logout,name='logout'),
    path('cart',Cart.as_view(),name='cart'),
    path('check-out',auth_middleware(Check_out.as_view()),name="checkout"),
    path('order',auth_middleware(OrderView.as_view()),name='order'),
]