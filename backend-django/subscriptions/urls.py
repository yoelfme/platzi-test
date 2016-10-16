from django.conf.urls import url
from .views import PaymentView, ProcessPaymentView

urlpatterns = [
    url(r'^$', PaymentView.as_view(), name='index'),
    url(r'^payment/$', ProcessPaymentView.as_view(), name='payment')
]
