# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Relationship(models.ForeignObject):
    """
    Create a django link between models on a field where a foreign key isn't used.
    This class allows that link to be realised through a proper relationship,
    allowing prefetches and select_related.
    Attribution to blog
    https://devblog.kogan.com/blog/custom-relationships-in-django
    """

    def __init__(self, model, from_fields, to_fields, **kwargs):
        super().__init__(
            model,
            on_delete=models.DO_NOTHING,
            from_fields=from_fields,
            to_fields=to_fields,
            null=True,
            blank=True,
            **kwargs,
        )

    def contribute_to_class(self, cls, name, private_only=False, **kwargs):
        # override the default to always make it private
        # this ensures that no additional columns are created
        super().contribute_to_class(cls, name, private_only=True, **kwargs)
        # setattr(cls, self.name, self.forward_related_accessor_class(self))


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


class OrdersItem(models.Model):
    pk = models.CompositePrimaryKey("orderid", "sku")
    orderid = models.IntegerField()
    order_reference = Relationship(
        "Order",
        from_fields=["orderid"],
        to_fields=["orderid"],
        related_name="orders_items",
    )
    sku = models.CharField()
    sku_reference = Relationship(
        "Product", from_fields=["sku"], to_fields=["sku"], related_name="orders_items"
    )
    qty = models.IntegerField()
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True, null=True
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        db_table = "orders_items"


class Product(models.Model):
    sku = models.CharField(primary_key=True, db_index=True, unique=True)
    desc = models.CharField(blank=True, null=True)
    wholesale_cost = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True, null=True
    )  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    dims_cm = models.CharField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = "products"
