from django.dispatch import Signal

register_success = Signal(providing_args=['user', 'p'])
