from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from django.utils import timezone
from django.views import View
from .forms import PaymentForm
from .models import Customer

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentView(View):
    template_name = 'subscriptions/payment.html'
    def get(self, request):
        return render(request, self.template_name)

class ProcessPaymentView(View):
    form_class = PaymentForm
    template_name = 'subscriptions/payment.html'
    messages = {
        'success': 'El pago ha sido procesado exitosamente, ahora formas parte de Platzi B)',
        'failed': 'Ocurrio un error al procesar el pago :(',
        'error_validation': 'Creo que tendras que corregir algunos datos :/',
        'late_suscribed': 'Ya eras Platzier, solo faltaba la suscripcion, has sido suscrito :D',
        'already_suscribed': 'Apreciamos tu amor por Platzi, pero ya estas suscrito al plan <3',
    }

    def get(self, request):
        raise Http404

    def post(self, request):
        form = self.form_class(request.POST)
        message_key = 'success'
        if form.is_valid():
            try:
                # Get the credit card details submitted by the form
                token = request.POST.get('stripeToken')
                email = request.POST.get('email')
                name = request.POST.get('name')

                # Verify if customer has not exists in database
                old_customer = Customer.objects.filter(email=email).first()
                if (old_customer):
                    # Customer already exists
                    customer = stripe.Customer.retrieve(old_customer.stripe_id)

                    if not old_customer.stripe_subscription_id:
                        # Create subscription for old customer
                        subscription = stripe.Subscription.create(
                          customer=customer.stripe_id,
                          plan=settings.STRIPE_DEFAULT_PLAN['id']
                        )

                        # Save the new subscription id
                        old_customer.stripe_subscription_id = subscription.id
                        old_customer.save()

                        message_key = 'late_suscribed'
                    else:
                        message_key = 'already_suscribed'
                else:
                    # Process payment and suscribe customer to plan in Stripe
                    customer = stripe.Customer.create(
                      source=token,
                      plan=settings.STRIPE_DEFAULT_PLAN['id'],
                      email=email
                    )

                    # Paid has been processed, create a new customer
                    self.create_new_customer(name, email, customer.id, customer.subscriptions.data[0].id)
            except stripe.error.InvalidRequestError as e:
                print(e)
                message_key = 'failed'
        else:
            message_key = 'error_validation'

        return render(request, 'subscriptions/payment.html', {
            'message': self.messages[message_key]
        })

    def create_new_customer(self, name, email, stripe_id, stripe_subscription_id):
        return Customer.objects.create(
            name=name,
            email=email,
            amount=settings.STRIPE_DEFAULT_PLAN['amount'],
            stripe_id=stripe_id,
            stripe_subscription_id=stripe_subscription_id,
            payment_date=timezone.now()
        )
