from rest_framework import serializers
from .models import Category, Product, ContactInquiry, Testimonial


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    # Return category name (readable) and slug for frontend filtering
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    # Accept category_id when creating/updating from admin
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    # Return the full Cloudinary URL (or empty string — never None to avoid frontend errors)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug',
            'category_name', 'category_slug', 'category_id',
            'image_url', 'description', 'price', 'is_featured',
            'created_at',
        ]
        read_only_fields = ['slug', 'created_at']

    def get_image_url(self, obj):
        """
        Returns the absolute Cloudinary URL.
        Cloudinary storage returns a full https:// URL via obj.image.url.
        Falls back to '' so the frontend can always safely render.
        """
        if obj.image:
            try:
                return obj.image.url
            except Exception:
                return ''
        return ''


class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = ['id', 'name', 'phone', 'email', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_phone(self, value):
        """Ensure phone number is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Phone number is required.")
        return value.strip()

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value.strip()


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'author', 'quote', 'rating']