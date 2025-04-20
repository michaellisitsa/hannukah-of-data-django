import datetime

from django.shortcuts import render
from django.db import Error, connection
from app.models import Customer, Order, OrdersItem, Product
from django.db.models import Q, Count

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
    return render(request, "output.html", {"customer": None})


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
    print("fall through should not be hit")
    return render(request, "output.html", {"customer": None})


def day02_alt(request):
    # Use smarter filtering to narrow down the list
    # instead of looping. This reduces the number of queries to
    customers = list(
        Customer.objects.filter(
            name__regex=r"^J[a-z]+ P[a-z]+",
        ).values_list("customerid", flat=True)
    )

    orders = list(
        Order.objects.filter(
            ordered__gte=datetime.date(2017, 1, 1),
            ordered__lte=datetime.date(2017, 12, 31),
            # Use a custom regex matcher instead of finding individuals with initials
            customerid__in=customers,
        ).values_list("orderid", flat=True)
    )

    orders_items = OrdersItem.objects.filter(
        # search for cleaning products (homeware)
        sku__startswith="HOM",
        orderid__in=orders,
    )
    print(connection.queries)

    if len(orders_items) > 0:
        # The problem is without the foreign key, we can't navigate back up.
        # Instead we need to manually climb back up.
        orders = Order.objects.filter(orderid=orders_items.first().orderid)
        customer = Customer.objects.filter(customerid=orders.first().customerid)
        return render(request, "output.html", {"customer": customer.first()})
    print("fall through should not be hit")
    return render(request, "output.html", {"customer": None})


def day02_fk(request):

    orders_items = OrdersItem.objects.filter(
        order_reference__ordered__gte=datetime.date(2017, 1, 1),
        order_reference__ordered__lte=datetime.date(2017, 12, 31),
        # Use a custom regex matcher instead of finding individuals with initials
        order_reference__customer_reference__name__regex=r"^J[a-z]+ P[a-z]+",
    ).filter(
        sku__startswith="HOM",
    )

    return render(
        request,
        "output.html",
        {"customer": orders_items[0].order_reference.customer_reference},
    )


def day03(request):
    years_of_rabbit = [2035, 2023, 2011, 1999, 1987, 1975, 1963, 1951, 1939, 1927]
    customers = Customer.objects.filter(
        # Narrow down cancer in year of the rabbit
        Q(birthdate__year__in=years_of_rabbit)
        & (
            (Q(birthdate__month="06") & Q(birthdate__day__gte=22))
            | (Q(birthdate__month="07") & Q(birthdate__day__lte=22))
        )
        # narow down to the same city as the customer from day 02
    ).filter(citystatezip__exact="Jamaica, NY 11435")
    if len(customers) == 0:
        print("could not find customer with a cancer birthdate in 2011")
        return render(request, "output.html", {"customer": None})
    else:
        return render(request, "output.html", {"customer": customers.first()})


def day04(request):
    early_orders = (
        Order.objects.annotate(n_orders=Count("orders_items"))
        .filter(
            # Before dawn, she was at the house by 5
            ordered__hour__lte=5,
            ordered__hour__gte=3,
            # More than 2 were found
            n_orders__gte=2,
            ordered__year__lte=2019,
        )
        .order_by("ordered__hour", "ordered__minute")
    )

    early_orders_list = list(early_orders.values_list("orderid", flat=True))

    orders_items = OrdersItem.objects.filter(
        orderid__in=early_orders_list, sku__startswith="BKY"
    )
    # Down to <35 entries of bakery goods that were ordered between 3 and 5 am
    print("how many items: ", orders_items.count())
    # TODO: Figure out how to limit this list more.
    # - limit to females
    # - Filter to only the earliest item of any day in that range
    # - Filter to more than 2 bakery items within a single order, rather than just 2 items which may include a bakery item

    return render(request, "output.html", {"customer": None})
