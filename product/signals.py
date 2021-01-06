from django.core.signals import request_started, request_finished, got_request_exception
from django.db.models.signals import pre_save, post_save, pre_init, post_init, pre_delete, post_delete, pre_migrate, post_migrate, m2m_changed
from django.dispatch import receiver

from product.models import Product


@receiver(pre_save, sender=Product)
def my_signal(sender, **kwargs):
    print('HELLO FROM MODEL')

# request_finished.connect(my_signal, sender=Product)