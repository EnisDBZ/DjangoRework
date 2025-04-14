from django.urls import path 

from . import views
from . import custom_admin

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
    path('satin-al/',views.checkout,name="checkout"),
    path("satin-al/satin-alim-onaylandi/",views.shipping_checked,name="shipping_checked"),
    path('search/',views.search_view,name="search"),
    path('categories/',views.categories_list,name="categories"),
    path('categories/<slug:slug>/', views.categories, name='category_products'),

    # Custom Admin panelinin URL'leri
    path("yonetici-paneli/",custom_admin.admin_links,name="yonetici-paneli"),
    path("yonetici-paneli/<str:app_label>/<str:model_name>/",custom_admin.admin_links_pages,name = "yonetici_paneli_sayfa"),
    path("yonetici-paneli/<str:model_name>/sil/<int:model_id>",custom_admin.model_silme,name="obje_sil"),
    path("yonetici-paneli/<str:app_label>/ekle/<str:model_name>" ,custom_admin.dynamic_model_item_add, name="add_model"),
    path('yonetici-paneli/<str:app_label>/update/<str:model_name>/<int:object_id>/', custom_admin.dynamic_model_item_update, name='update_model'),

]
