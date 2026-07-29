from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ContactInquiry, Testimonial


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_featured', 'created_at', 'image_preview')
    list_filter = ('category', 'is_featured')
    list_editable = ('is_featured',)
    search_fields = ('name', 'description')
    readonly_fields = ('slug', 'created_at', 'image_preview')
    prepopulated_fields = {}  # Slug is auto-generated in model.save()

    fieldsets = (
        ('Product Info', {
            'fields': ('name', 'slug', 'category', 'price', 'description', 'is_featured')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            try:
                return format_html(
                    '<img src="{}" style="width:80px;height:auto;border-radius:6px;border:1px solid #ddd;" />',
                    obj.image.url
                )
            except Exception:
                return "Image URL unavailable"
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('name', 'phone', 'email', 'message', 'created_at')
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        # Inquiries should only come from the frontend form, not be manually added
        return False


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'rating', 'is_active', 'short_quote')
    list_editable = ('is_active', 'rating')
    list_filter = ('is_active', 'rating')
    search_fields = ('author', 'quote')

    def short_quote(self, obj):
        return obj.quote[:80] + '...' if len(obj.quote) > 80 else obj.quote
    short_quote.short_description = 'Quote'