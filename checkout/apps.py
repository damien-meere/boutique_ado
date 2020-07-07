from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'

    # verriding the ready method and importing our signals module.
    # With that done, every time a line item is saved or deleted.
    # Our custom update total model method will be called. Updating
    # the order totals automatically.
    def ready(self):
        import checkout.signals
