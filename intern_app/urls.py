from django.urls import path 

from . import views

app_name = "intern_app"

urlpatterns = [
    path('',views.product_view,name = "index"),
    path('',views.redirect_url_ , name ="redirect_url"),
    path('settings/',views.setting,name="settings"),
    path('login/',views.login_view,name="login"),
    path('signup/',views.signup_view, name ="signup"),
    path('logout/',views.logout_view, name="logout"),
    path('settings/update_password/' , views.update_password , name = "update_password"),
    path('settings/update_email/',views.update_email,name="update_email"),
    path('settings/update_names/',views.update_names,name="update_names"),
    path("", views.cart_view, name="cart"),
    path("add/<int:product_id>/",views.add_to_cart, name="add_to_cart"),
    path("update/<int:item_id>/", views.update_cart, name="update_cart"),
    path('remove/<int:item_id>/',views.remove_from_cart,name ="remove_from_cart"),
    path('search/',views.search_view,name="search"),
    path('categories/',views.categories_list,name="categories"),
    path('categories/<slug:slug>/', views.categories, name='category_products'),

]
