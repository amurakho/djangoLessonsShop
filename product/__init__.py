from djnagoShop.celery import app

__all__ = ('app',)


default_app_config = 'product.apps.ProductConfig'