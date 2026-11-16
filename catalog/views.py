from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Product, Contact, Category
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .services import get_products_by_category, get_cached_products_list


class HomeListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.order_by('-created_at')[:5]


class ProductUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.has_perm('catalog.can_unpublish_product'):
            raise PermissionDenied

        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()

        return redirect('catalog:product_detail', pk=product.pk)


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'

    def get(self, request, *args, **kwargs):
        products_list = get_cached_products_list()

        paginator = Paginator(products_list, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'products': page_obj,
            'page_obj': page_obj,
        })

@method_decorator(cache_page(60*15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        if product.owner != self.request.user:
            raise PermissionDenied

        return product


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_object(self, queryset=None):
        product = super().get_object(queryset)

        is_owner = product.owner == self.request.user
        is_moderator = self.request.user.has_perm('catalog.delete_product')

        if not (is_owner or is_moderator):
            raise PermissionDenied

        return product


class ProductByCategoryView(ListView):
    template_name = 'category_products.html'  # Можем использовать тот же шаблон, что и для каталога
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')

        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context['category'] = get_object_or_404(Category, id=category_id)
        return context


class ContactsView(View):
    def get(self, request):
        contacts_list = Contact.objects.all()
        return render(request, 'contacts.html', {'contacts': contacts_list})

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        return self.get(request)
