from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quickshop.accounts.urls')),
    path('products/', include('quickshop.products.urls')),
    path('cart/', include('quickshop.cart.urls')),
    path('orders/', include('quickshop.orders.urls')),
    path('seller/', include('quickshop.seller.urls')),
    path('admin-panel/', include('admin_app.urls')),
    path('payment/', include('payment.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)