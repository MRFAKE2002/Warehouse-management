from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.db.models.base import Model as Model
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Variant, Supply, Category, Type, Size
from order.models import OrderItem
from . import forms

from cart.models import CartItem

class HomeListView(ListView):

    model = Supply
    template_name = 'product/home.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(children=None)
        context["recent"] = Supply.objects.all()[:3]
        return context
    

class SupplyListView(ListView):

    model = Supply
    template_name = 'product/list/supply_list.html'

class SupplyCreateView(CreateView):

    model = Supply
    fields = ['title', 'category', 'image', 'status', 'size', 'type', 'description']
    template_name = 'product/add/add_supply_form.html'
    success_url = reverse_lazy('product:supply_list')
    success_message = "محصول با موفقیت ساخته شد!"  # Assuming 'name' field exists

class SupplyUpdateView(UpdateView):

    model = Supply
    fields = ['title', 'category', 'image', 'status', 'description']
    template_name = 'product/update/update_supply_form.html'
    
    def form_valid(self, form):
        self.object = form.save()
        # Your custom update logic here (if any)

        # Display success message using Django's messaging framework
        messages.success(self.request, " محصول با موفقیت به‌روزرسانی شد!")

        # Redirect to the updated variant page (or any other appropriate URL)
        return HttpResponseRedirect(reverse('product:supply_detail', kwargs={'id': self.object.id}))

    def get_object(self):
        global id
        id = self.kwargs.get('id')
        return get_object_or_404(Supply.objects.Available(), pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = id 
        return context

class SupplyDeleteView(DeleteView):

    model = Supply
    success_url = reverse_lazy('product:supply_list')
    template_name = 'product/delete/delete_confirm_supply.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        order_items = OrderItem.objects.filter(variant__supply__id=self.object.id)
        if order_items.exists():
            # If the variant exists in orders, display an error message
            messages.error(self.request, f'این محصول در سفارش موجود است. ابتدا باید سفارشات را حذف کنید.')
            return HttpResponseRedirect(reverse('product:supply_list'))

        self.object.delete()
        messages.success(self.request, 'محصول با ویژگی مورد نظر با موفقیت حذف شد!')
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        global id 
        id = self.kwargs.get('id')
        return get_object_or_404(Supply.objects.Available(), pk=id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = id 
        return context


#---------------------------------------------------------------------------------
# Variant view -> CreateView, UpdateView, DeleteVeiw, ListView
class VariantListView(ListView):
    model = Variant
    template_name = 'product/list/variant_list.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart_items = CartItem.objects.filter(cart__user=self.request.user.id)
        cart_items_quantity = {item.variant.id : item.quantity for item in cart_items}
        context['cart_items_quantity'] = cart_items_quantity
        return context


def supply_variant_list_view(request, supply_id):
    variants = Variant.objects.filter(supply_id=supply_id)
    
    context = {'object_list': variants}
    
    return render(request, 'product/list/variant_list.html', context)

class VariantDetailView(DetailView):

    model = Variant
    template_name = 'product/variant_detail.html'

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Variant.objects.all(), pk=id)


    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        variant = self.get_object()
        
        # Retrieve associated order items using the related field 'order_variants'
        order_items = variant.order_variants.all()

        # Pass the variant and order items to the template context
        context = {
            'object': variant,
            'order_items': order_items,
        }
        return context


class VariantCreateView(CreateView):
    model = Variant
    # fields = ['supply', 'Type', 'size', 'inventory']
    template_name = 'product/add/add_variant_form.html'
    form_class = forms.VariantAddForm
    success_url = reverse_lazy('product:variant_list')
    success_message = "محصول '%(name)s' با موفقیت ساخته شد!"  # Assuming 'name' field exists

class VariantDeleteView(DeleteView):

    model = Variant
    success_url = reverse_lazy('product:variant_list')
    template_name = 'product/delete/delete_confirm_variant.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        order_items = OrderItem.objects.filter(variant=self.object)
        if order_items.exists():
            # If the variant exists in orders, display an error message
            messages.error(self.request, 'این محصول در سفارشات موجود است. ابتدا باید سفارشات را حذف کنید.')
            return HttpResponseRedirect(reverse('product:variant_detail', kwargs={'id': self.object.id}))

        self.object.delete()
        messages.success(self.request, 'محصول با ویژگی مورد نظر با موفقیت حذف شد!')
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Variant.objects.all(), pk=id)

class VariantUpdateView(UpdateView):
    model = Variant
    fields = ['supply', 'type', 'size', 'price', 'inventory']
    template_name = 'product/update/update_variant_form.html'

    def form_valid(self, form):
        self.object = form.save()
        # Your custom update logic here (if any)

        # Display success message using Django's messaging framework
        messages.success(self.request, " محصول با موفقیت به‌روزرسانی شد!")

        # Redirect to the updated variant page (or any other appropriate URL)
        return HttpResponseRedirect(reverse('product:variant_detail', kwargs={'id': self.object.id}))

    def get_object(self):
        global id 
        id = self.kwargs.get('id')
        return get_object_or_404(Variant.objects.all(), pk=id)
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['id'] = id 
        return context 
#---------------------------------------------------------------------------------
# Category view -> CreateView, UpdateView, DeleteVeiw, ListView
class CategoryList(ListView):

    model = Category
    queryset = Category.objects.filter(status=True)
    template_name = "product/list/category_list.html"

class CategoryCreateView(CreateView):

    model = Category
    fields = ['children', 'title', 'status']
    template_name = "product/add/add_category_form.html"
    success_url = reverse_lazy('product:category_list')

class CategoryDeleteView(DeleteView):

    model = Variant
    success_url = reverse_lazy('product:category_list')
    template_name = 'product/delete/delete_confirm_category.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'دسته بندی مورد نظر با موفقیت حذف شد!')
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Category.objects.all(), pk=id)
    

class CategoryUpdateView(UpdateView):

    model = Category
    fields = ['children', 'title', 'status']
    template_name = "product/update/update_category_form.html"

    def form_valid(self, form):
        self.object = form.save()
        # Your custom update logic here (if any)

        # Display success message using Django's messaging framework
        messages.success(self.request, " دسته بندی با موفقیت به‌روزرسانی شد!")

        # Redirect to the updated variant page (or any other appropriate URL)
        return HttpResponseRedirect(reverse('product:category_list'))

    def get_object(self):
        global id 
        id = self.kwargs.get('id')
        return get_object_or_404(Category.objects.all(), pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = id 
        return context
    

#---------------------------------------------------------------------------------
# Size view -> CreateView, UpdateView, ListView, DeleteView
class SizeCreateView(CreateView):

    model = Size
    fields = ['name']
    template_name = "product/add/add_size_form.html"
    success_url = reverse_lazy('product:size_list')

class SizeUpdateView(UpdateView):

    model = Size
    fields = ['name']
    template_name = "product/update/update_size_form.html"

    def form_valid(self, form):
        self.object = form.save()
        # Your custom update logic here (if any)

        # Display success message using Django's messaging framework
        messages.success(self.request, " سایز با موفقیت به‌روزرسانی شد!")

        # Redirect to the updated variant page (or any other appropriate URL)
        return HttpResponseRedirect(reverse('product:size_list'))

    def get_object(self):
        global id
        id = self.kwargs.get('id')
        return get_object_or_404(Size.objects.all(), pk=id)
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = id 
        return context
    
class SizeListView(ListView):
    
    model = Size
    template_name = 'product/list/size_list.html'
    queryset = Size.objects.all()

class SizeDeleteView(DeleteView):
    model = Size
    success_url = reverse_lazy('product:size_list')
    template_name = 'product/delete/delete_confirm_size.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'سایز مورد نظر با موفقیت حذف شد!')  # Removed SET()
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Size.objects.all(), pk=id)

#---------------------------------------------------------------------------------
# Type view -> CreateView, UpdateView, ListView, DeleteView
class TypeCreateView(CreateView):

    model = Type
    fields = ['name']
    template_name = "product/add/add_type_form.html"
    success_url = reverse_lazy('product:type_list')

class TypeUpdateView(UpdateView):

    model = Type
    fields = ['name']
    template_name = "product/update/update_type_form.html"

    def form_valid(self, form):
        self.object = form.save()
        # Your custom update logic here (if any)

        # Display success message using Django's messaging framework
        messages.success(self.request, " مدل با موفقیت به‌روزرسانی شد!")

        # Redirect to the updated variant page (or any other appropriate URL)
        return HttpResponseRedirect(reverse('product:type_list'))

    def get_object(self):
        global id 
        id = self.kwargs.get('id')
        return get_object_or_404(Type.objects.all(), pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = id 
        return context
    
class TypeListView(ListView):
    
    model = Type
    template_name = 'product/list/type_list.html'
    queryset = Type.objects.all()

class TypeDeleteView(DeleteView):

    model = Variant
    success_url = reverse_lazy('product:type_list')
    template_name = 'product/delete/delete_confirm_type.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'مدل مورد نظر با موفقیت حذف شد!')
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Type.objects.all(), pk=id)

#---------------------------------------------------------------------------------

# SearchView
@require_POST
def search_view(request):
    """
    this view gets search phrase from input in template named query via method POST
    and checks if there is match in Category.title
    """
    variant_query =Variant.objects.all()
    if request.method == "POST":
        search = request.POST.get('query')
        variant = variant_query.filter(supply__title__icontains = search)
        return render(request, 'product/search_result.html', {"variant": variant})

