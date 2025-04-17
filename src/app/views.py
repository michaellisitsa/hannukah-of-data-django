from django.shortcuts import render
from django.db import Error, connection

from app.models import Customer

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
