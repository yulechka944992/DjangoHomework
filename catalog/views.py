from gc import get_objects

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Product, Contact
from .forms import ProductForm


class HomeListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.order_by('-created_at')[:5]


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'page_obj'

    paginate_by = 6


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    success_url = reverse_lazy('catalog:product_list')


class ContactsView(View):
    def get(self, request):
        contacts_list = Contact.objects.all()
        return render(request, 'contacts.html', {'contacts': contacts_list})

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        return self.get(request)
# def home(request):
#     latest_products = Product.objects.order_by('-created_at')[:5]
#     return render(request, 'home.html', {'products': latest_products})
#
#
# def contacts(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#
#         return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
#
#     contacts_list = Contact.objects.all()
#     return render(request, 'contacts.html', {'contacts': contacts_list})
#
#
# def product_list(request):
#     products = Product.objects.all()
#
#     paginator = Paginator(products, 6)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'product_list.html', {'page_obj': page_obj})
#
#
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'product_detail.html', {'product': product})
#
#
# def product_create(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('catalog:product_list')
#     else:
#         form = ProductForm()
#
#     return render(request, 'product_create.html', {'form': form})