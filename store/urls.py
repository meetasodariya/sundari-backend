from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    CategoryListView,
    ContactInquiryCreateView,
    TestimonialListView,
    HealthCheckView,
)

urlpatterns = [
    # Products
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),

    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),

    # Contact / Inquiries
    path('inquiries/', ContactInquiryCreateView.as_view(), name='create-inquiry'),

    # Testimonials
    path('testimonials/', TestimonialListView.as_view(), name='testimonial-list'),

    # Health Check (for Render uptime monitoring)
    path('health/', HealthCheckView.as_view(), name='health-check'),
]