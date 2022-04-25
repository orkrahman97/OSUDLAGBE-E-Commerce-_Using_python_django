from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class home(ListView):
    model = Product
    template_name = 'store_templates\home.html'

class Product_detail(LoginRequiredMixin,DetailView):
    model = Product
    template_name  = 'store_templates\product_detail.html'
    
