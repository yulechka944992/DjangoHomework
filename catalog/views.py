from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact


def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    for p in latest_products:
        print(p.name, p.price)

    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")

    contacts_list = Contact.objects.all()
    return render(request, 'contacts.html', {'contacts': contacts_list})
