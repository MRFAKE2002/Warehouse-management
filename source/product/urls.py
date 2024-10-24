from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name ='product'
urlpatterns = [

    path('', login_required(views.HomeListView.as_view()), name='home'),

    # Supply urls
    path('create_supply/', views.SupplyCreateView.as_view(), name='supply_create'), 
    path('list_supply/', views.SupplyListView.as_view(), name='supply_list'), 
    path('update_supply/<int:id>', views.SupplyUpdateView.as_view(), name='supply_update'), 
    path('delete_supply/<int:id>', views.SupplyDeleteView.as_view(), name='supply_delete'),

    # Variant Urls
    path ('variant_list/', views.VariantListView.as_view(), name='variant_list'),
    path ('supply_variant_list/<int:supply_id>', views.supply_variant_list_view, name='supply_variant_list'),
    path ('detail/<int:id>', views.VariantDetailView.as_view(), name='variant_detail'),
    path ('create_variant/', views.VariantCreateView.as_view( ), name='variant_create'),
    path ('update_variant/<int:id>', views.VariantUpdateView.as_view( ), name='variant_update'),
    path ('delete_variant/<int:id>', views.VariantDeleteView.as_view( ), name='variant_delete'),

    # Category Urls  
    path('category/', views.CategoryList.as_view(), name='category_list'),
    path('create_category/', views.CategoryCreateView.as_view(), name='category_create' ), 
    path('update_category/<int:id>', views.CategoryUpdateView.as_view(), name='category_update' ), 
    path('delete_category/<int:id>', views.CategoryDeleteView.as_view(), name='category_delete' ), 

    # Type Urls
    path('create_type/', views.TypeCreateView.as_view(), name='type_create' ),
    path('type_list/', views.TypeListView.as_view(), name='type_list' ),
    path('update_type/<int:id>', views.TypeUpdateView.as_view(), name='type_update' ),
    path('delete_type/<int:id>', views.TypeDeleteView.as_view(), name='type_delete' ),

    # Size Urls
    path('create_size/', views.SizeCreateView.as_view(), name='size_create' ), 
    path('size_list/', views.SizeListView.as_view(), name='size_list' ), 
    path('update_size/<int:id>', views.SizeUpdateView.as_view(), name='size_update' ), 
    path('delete_size/<int:id>', views.SizeDeleteView.as_view(), name='size_delete' ), 

    # Search Url
    path ('search/', views.search_view, name='search'),
]
