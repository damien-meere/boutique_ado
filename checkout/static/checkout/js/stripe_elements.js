/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// slice off the first and last character on each since they'll have 
// quotation marks which we don't want.
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

//handle realtime validation errors on cards
card.addEventListener('change', function(event){
    var errorDiv  =document.getElementById('card-errors')
    if(event.error){
        var html = `
            <span class="icon" role ="alert">
                <i class = "fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html)
    }else {
        errorDiv.textContent = '';
    }
});

// Handle Form Submission
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    // Prevent defualt POST action
    ev.preventDefault();
    // Instesd execute the following code
    // Disable both the card element and the submit button to prevent multiple submissions.
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    // Provide the card to stripe
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    // then execute this function on the result.
    }).then(function(result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            // After providing error notification, reenable card and submit button
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        // If status of the payment intent comes back as successful, Submit Form
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});