from rest_framework import serializers

from .models import Cart, CartItem, Category, Product, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug', 'image')


class CategoryWithSubcategoriesSerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'subcategories')


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        source='subcategory.category.name', read_only=True
    )
    subcategory = serializers.CharField(
        source='subcategory.name', read_only=True
    )
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'category', 'subcategory', 'price', 'images'
        )

    def get_images(self, obj):
        request = self.context.get('request')
        if not obj.original_image or not obj.original_image.name:
            return None
        try:
            return {
                'small': (
                    request.build_absolute_uri(obj.image_small.url)
                    if request else obj.image_small.url
                ),
                'medium': (
                    request.build_absolute_uri(obj.image_medium.url)
                    if request else obj.image_medium.url
                ),
                'large': (
                    request.build_absolute_uri(obj.image_large.url)
                    if request else obj.image_large.url
                ),
            }
        except (FileNotFoundError, ValueError, OSError):
            return {
                'smail': None,
                'medium': None,
                'large': None,
            }


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2, read_only=True
    )
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = (
            'id', 'product', 'product_name',
            'product_price', 'quantity', 'total_price'
        )
        read_only_fields = ('id',)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_items', 'total_price')


class CartItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('product', 'quantity')

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Количество должно быть не менее 1"
            )
        return value
