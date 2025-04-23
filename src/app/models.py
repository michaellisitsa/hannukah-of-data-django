# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Customer(models.Model):
    customerid = models.IntegerField(primary_key=True, db_index=True, unique=True)
    name = models.CharField()
    address = models.CharField()
    citystatezip = models.CharField()
    birthdate = models.DateField()
    phone = models.CharField()
    timezone = models.CharField()
    lat = models.DecimalField(
        max_digits=10, decimal_places=5
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    long = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True, null=True
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    def count_orders_by_sku_type(self):

        return self.orders_fk.filter(orders_items_fk__sku__startswith="BKY").count()

    class Meta:
        db_table = "customers"


class Order(models.Model):
    orderid = models.CharField(primary_key=True, db_index=True, unique=True)

    customerid = models.CharField()
    # Identical copy of the above but with a foreign key constraint.
    # Approach used in https://marcolcl.medium.com/converting-text-field-to-foreign-key-in-django-34e191845bbe
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name="orders_fk", null=True
    )
    ordered = models.DateTimeField()  # This field type is a guess.
    shipped = models.DateTimeField()  # This field type is a guess.
    total = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True, null=True
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    items = models.CharField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = "orders"


class Product(models.Model):
    sku = models.CharField(primary_key=True, db_index=True, unique=True)
    desc = models.CharField(blank=True, null=True)
    wholesale_cost = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True, null=True
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    dims_cm = models.CharField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = "products"


class OrdersItem(models.Model):
    orderid = models.IntegerField()
    # Identical copy of the above but with a foreign key constraint.
    order = models.ForeignKey(
        Order, on_delete=models.DO_NOTHING, related_name="orders_items_fk", null=True
    )
    sku = models.CharField()
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="products_fk", null=True
    )
    qty = models.IntegerField()
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True, null=True
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        db_table = "orders_items"
