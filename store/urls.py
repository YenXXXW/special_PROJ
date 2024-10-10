from django.urls import path
from . import views
from . import shopAdminPanelOrderViews
from . import shopAdminProductsViews
# app_name="store"

urlpatterns=[
    path('', views.store, name="store"),
    path('product/<int:product_id>', views.product_details, name="product_details"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('shop_admin_panel', shopAdminProductsViews.shop_admin_panel, name="shop_admin_panel"),
    path('get-products', shopAdminProductsViews.getAllProducts, name="get-products"),
    path('get-product-by_Id<int:product_id>', shopAdminProductsViews.get_product_by_Id, name="get-product-by-Id"),
    path('edit-product/<int:product_id>', shopAdminProductsViews.edit_product, name="edit-product"),
    path('add-product', shopAdminProductsViews.addProduct, name="add-product"),
    path('log_in/', views.log_in, name="log_in"),
    path('logout/', views.log_out, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('get-orders', shopAdminPanelOrderViews.getOrders, name="getOrders"),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('delete-product', shopAdminProductsViews.deleteProduct, name='delete-product'),
    path('get-orders/', shopAdminPanelOrderViews.getOrders, name="get-orders"),
    path('order-details/<int:order_id>', shopAdminPanelOrderViews.oderDetails, name="order-details")
]