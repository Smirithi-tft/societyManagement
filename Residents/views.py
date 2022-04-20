from django.shortcuts import render
from .forms import RentForm, BuyForm
from django.contrib import messages


def home(request):
    if request.method == 'POST':
        messages.add_message(request, messages.SUCCESS,
                             message="Thank you! Someone will contact you soon.")

    rent_form = RentForm()
    buy_form = BuyForm()
    return render(request, 'residents/home.html', {'title': 'Home Page',
                                                   'r_form': rent_form,
                                                   'b_form': buy_form})
