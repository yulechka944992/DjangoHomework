from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost
from django import forms


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:blog_list')

    widgets = {
        'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        'preview': forms.FileInput(attrs={'class': 'form-control'}),
    }


class BlogUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    widgets = {
        'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        'preview': forms.FileInput(attrs={'class': 'form-control'}),
    }


    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})

class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')
