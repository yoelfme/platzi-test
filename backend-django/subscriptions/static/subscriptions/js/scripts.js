(function () {
  'use strict'

  // Grab the form:
  var $form = $('#payment-form')

  // Set stripe configuration
  Stripe.setLanguage('es')
  Stripe.setPublishableKey('pk_test_5ZFNuU5gBd8qSwrrAcKIHpUK')

  $form.on('submit', function (event) {
    // Prevent the form from being submitted:
    event.preventDefault()

    // Disable the submit button to prevent repeated clicks:
    $form.find('.submit').prop('disabled', true)

    // Request a token from Stripe:
    Stripe.card.createToken($form, stripeResponseHandler)
  })

  var stripeResponseHandler = function (status, response) {
    if (response.error) { // Problem!
      // Set the errors on the form:
      $form.find('.payment-errors').text(response.error.message)
      // Re-enable submission
      $form.find('.submit').prop('disabled', false)
      // Show error messages
      showErrors(true)
    } else { // Token was created!
      // Get the token ID:
      var token = response.id

      // Insert the token ID into the form so it gets submitted to the server:
      $form.append($('<input type="hidden" name="stripeToken">').val(token))
      // Submit the form:
      $form.get(0).submit()
    }
  }

  var showErrors = function (show) {
    var divErrors = $($form.find('.payment-errors').parents('.row')[0])

    return show ? divErrors.css('display', 'block') : divErrors.css('display', 'none')
  }
}())
