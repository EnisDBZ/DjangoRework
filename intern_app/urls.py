from django.urls import path 

from . import views
from . import custom_admin

app_name = "intern_app"

urlpatterns = [
    path('',views.product_view,name = "index"),
    path('<str:item_name>-<int:item_id>/',views.item_details,name="item_details"),
    path('',views.redirect_url_ , name ="redirect_url"),
    path('settings/',views.setting,name="settings"),
    path("settings/kart-ekle/",views.card_ekle,name="card_ekle"),
    path("settings/kart-guncelle/<int:item_id>",views.card_guncelle,name="card_guncelle"),
    path('settings/kart-sil/<int:item_id>/',views.card_sil,name="card_sil"),
    path('settings/adres-ekle/',views.adres_ekle,name="adres_ekle"),
    path('settings/adres-guncelle/<int:adres_id_guncelleme>/',views.adres_guncelleme,name="adres_guncelleme"),
    path('set-default-ajax/', views.only_default_update_address, name='only_default_update_address'),
    path('set-default-ajax-cc/', views.only_default_update_cc, name='only_default_update_cc'),
    path('settings/adres-sil/<int:adres_id>/',views.adres_sil,name="adres_sil"),
    path('login/',views.login_view,name="login"),
    path('signup/',views.signup_view, name ="signup"),
    path('logout/',views.logout_view, name="logout"),
    path('settings/update_password/' , views.update_password , name = "update_password"),
    path('settings/update_email/',views.update_email,name="update_email"),
    path('settings/update_names/',views.update_names,name="update_names"),
    path("", views.cart_view, name="cart"),
    path("add/<int:product_id>/",views.add_to_cart, name="add_to_cart"),
    path("clear-quick-buy/",views.clear_quick_buy,name="clear_quick_buy"),
    path("update/<int:item_id>/", views.update_cart, name="update_cart"),
    path('remove/<int:item_id>/',views.remove_from_cart,name ="remove_from_cart"),
    path('satin-al/',views.checkout,name="checkout"),
    path('buy_now/<int:product_id>/', views.checkout_quick_buy, name='checkout_quick_buy'),
    path("satin-al/satin-alim-onaylandi/",views.shipping_checked,name="shipping_checked"),
    path('search/',views.search_view,name="search"),
    path('categories/',views.categories_list,name="categories"),
    path('categories/<slug:slug>/', views.categories, name='category_products'),
    path('categories/<slug:slug>/urunler/',views.category_products,name="subcategory_products"),

    # Custom Admin panelinin URL'leri
    path("yonetici-paneli/",custom_admin.admin_links,name="yonetici-paneli"),
    path("yonetici-paneli/<str:app_label>/<str:model_name>/",custom_admin.admin_links_pages,name = "yonetici_paneli_sayfa"),
    path("yonetici-paneli/<str:model_name>/sil/<int:model_id>",custom_admin.model_silme,name="obje_sil"),
    path("yonetici-paneli/<str:app_label>/ekle/<str:model_name>" ,custom_admin.dynamic_model_item_add, name="add_model"),
    path('yonetici-paneli/<str:app_label>/update/<str:model_name>/<int:object_id>/', custom_admin.dynamic_model_item_update, name='update_model'),

]
