from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.fields import AutoSlugField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    in_stock = models.BooleanField(default=False)
    image = models.ImageField(upload_to='media')
    rating = models.IntegerField(default=0)
    slug = AutoSlugField(populate_from='name')
    tegory = models.ForeignKey(Category, on_delete=models.CASCADE)
    code = models.IntegerField()
    count = models.IntegerField()

    def __str__(self):
        return f'Product: {self.name}, price: {self.price}, in_stock: {self.in_stock}'


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    stars = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductInBucket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    full_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    one_product_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    bucket = models.ForeignKey('Bucket', on_delete=models.SET_NULL, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_price = round(float(self.one_product_price) * float(self.count), 2)
        super().save(force_insert, force_update, using, update_fields)
        self.bucket.update_status()


class Bucket(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    count = models.IntegerField(default=0)

    def update_status(self):
        price = 0
        count = 0
        for product in self.productinbucket_set.all():
            price += product.full_price
            count += product.count
        self.price = price
        self.count = count

        self.save()



