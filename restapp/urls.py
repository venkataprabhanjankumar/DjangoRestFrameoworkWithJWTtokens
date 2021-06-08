from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('signup', views.signup),
    path('signin', views.signin),
    path('getproducts', views.getProducts),
    path('getproduct/<int:product_id>', views.getProduct),
    path('getusers', views.getUsers),
    path('getuser/<int:user_id>', views.getUser),
    path('deleteproduct/<int:product_id>', views.deleteProduct),
    path('deleteuser/<int:user_id>', views.deleteUser),
    path('createproduct', views.createProduct),
    path('updateproduct/<int:product_id>', views.updateProduct),
    path('createuser',views.createUser),
]
