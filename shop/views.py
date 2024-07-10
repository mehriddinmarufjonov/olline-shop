from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Category, Product, Rating
from django.contrib.auth import logout


# Create your views here.

class ProductList(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    extra_context = {
        'categories': Category.objects.filter(parent=None),
        'title': "Fruitables online shop",
        'page_name': "Shop"
    }


class AllProductsList(ProductList):
    template_name = 'shop/all_products.html'


class SortingProductList(AllProductsList):

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(filter_choice=self.kwargs['key_name'])
        context['products'] = products
        return context


class SortingBySubcategories(AllProductsList):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory = Category.objects.get(slug=self.kwargs['slug'])
        context['products'] = subcategory.product_set.all()
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    extra_context = {
        'page_name': "Shop Detail",
        'categories': Category.objects.filter(parent=None)
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            product = Product.objects.get(slug=self.kwargs['slug'])
            rating = Rating.objects.filter(product=product, user=self.request.user).first()
            context['user_rating'] = rating.rating if rating else 0
        return context


def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
    product = Product.objects.get(pk=product_id)
    if request.user.is_authenticated:
        Rating.objects.filter(product=product, user=request.user).delete()
        product.rating_set.create(user=request.user, rating=rating)
    return redirect('detail', slug=product.slug)



def logout_view(request):
    logout(request)
    return redirect('login')



# def index(request: HttpRequest) -> HttpResponse:
#     posts = Product.objects.all()
#     for post in posts:
#         rating = Rating.objects.filter(post=post, user=request.user).first()
#         post.user_rating = rating.rating if rating else 0
#     return render(request, "index.html", {"posts": posts})





# def detail(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     context = {
#         'product': product,
#         'page_name': "Shop Detail"
#     }
#     return render(request, 'shop/product_detail.html', context)








# def sorting(request: HttpRequest, key_name) -> HttpResponse:
#     context = {
#         'products': Product.objects.filter(filter_choice=key_name),
#         'categories': Category.objects.filter(parent=None)
#     }
#     return render(request, 'shop/all_products.html', context)


# def sorting_by_subcategories(request, slug):
#     subcategory = Category.objects.get(slug=slug)
#     context = {
#         'categories': Category.objects.filter(parent=None),
#         'products': subcategory.product_set.all()
#     }
#     return render(request, 'shop/all_products.html', context)
#


# def index(request: HttpRequest):
#     context = {
#         'products': Product.objects.all(),
#         'categories': Category.objects.all()
#     }
#     return render(request, 'shop/index.html', context)



