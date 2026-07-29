from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator

from .models import Product, Category, ContactInquiry, Testimonial
from .serializers import (
    ProductSerializer, CategorySerializer,
    ContactInquirySerializer, TestimonialSerializer,
)


@method_decorator(cache_control(max_age=300, public=True), name='dispatch')
class ProductListView(generics.ListAPIView):
    """
    GET /api/products/
    GET /api/products/?category=saree
    GET /api/products/?featured=true
    GET /api/products/?category=saree&featured=true

    Returns paginated product list (20 per page by default).
    Browser/CDN caches response for 5 minutes.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related('category').order_by('-created_at')

        category_slug = self.request.query_params.get('category')
        featured = self.request.query_params.get('featured')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """
    GET /api/products/<slug>/
    Returns a single product by its slug.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()
    lookup_field = 'slug'


@method_decorator(cache_control(max_age=600, public=True), name='dispatch')
class CategoryListView(generics.ListAPIView):
    """
    GET /api/categories/
    Returns all product categories. Cached for 10 minutes.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ContactInquiryCreateView(generics.CreateAPIView):
    """
    POST /api/inquiries/
    Accepts a contact form submission and saves to the database.
    """
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'message': 'Thank you! Your inquiry has been received. We will contact you soon.'},
            status=status.HTTP_201_CREATED
        )


@method_decorator(cache_control(max_age=600, public=True), name='dispatch')
class TestimonialListView(generics.ListAPIView):
    """
    GET /api/testimonials/
    Returns all active testimonials. Cached for 10 minutes.
    """
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer


class HealthCheckView(APIView):
    """
    GET /api/health/
    Simple health check endpoint for Render uptime monitoring.
    Returns 200 OK if the app is running.
    """
    def get(self, request):
        return Response({'status': 'ok', 'service': 'Sundari Silk Palace API'})