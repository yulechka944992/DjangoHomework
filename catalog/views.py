from gc import get_objects

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, Contact
from .forms import ProductForm


def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    for p in latest_products:
        print(p.name, p.price)

    return render(request, 'home.html', {'products': latest_products})


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")

    contacts_list = Contact.objects.all()
    return render(request, 'contacts.html', {'contacts': contacts_list})


def product_list(request):
    products = Product.objects.all()

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product_list.html', {'page_obj': page_obj})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_list')
    else:
        form = ProductForm()

    return render(request, 'product_create.html', {'form': form})