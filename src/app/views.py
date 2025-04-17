import datetime

from django.shortcuts import render
from django.db import Error, connection
from app.models import Customer, Order, OrdersItem

# Phone keyboard translation layer
letters_to_numbers = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "22233344455566677778889999"
)


# Create your views here.
def day01(request):
    customers = Customer.objects.all()
    for customer in customers:
        last_name = customer.name.split(" ")[1]
        digits = last_name.upper().translate(letters_to_numbers)
        phone = customer.phone.replace("-", "")
        if phone == digits:
            return render(request, "output.html", {"customer": customer})


def day02(request):
    customers = Customer.objects.all()

    def extract_first_letter(string):
        return string[0]

    for customer in customers:
        initials = list(map(extract_first_letter, customer.name.split(" ")))
        first_name_init, last_name_init = initials[0], initials[-1]
        # We find the name, but we also need to restrict to the order in 2017
        if initials == ["J", "P"]:
            orders = Order.objects.filter(
                ordered__gte=datetime.date(2017, 1, 1),
                ordered__lte=datetime.date(2017, 12, 31),
                customerid=customer.customerid,
            )
            if len(orders) > 0 and orders.first():
                items = OrdersItem.objects.filter(orderid=orders.first().orderid)
                for item in items:
                    if item.sku.startswith("HOM"):
                        return render(request, "output.html", {"customer": customer})
            else:
                pass
            return render(request, "output.html", {"customer": None})
