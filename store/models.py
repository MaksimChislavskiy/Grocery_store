from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Slug')
    image = ProcessedImageField(
        upload_to='categories/',
        processors=[ResizeToFit(800, 800)],
        format='JPEG',
        options={'quality': 90},
        verbose_name='Изображение'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Родительская категория'
    )
    name = models.CharField(max_length=100, verbose_name='Наименование')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Slug')
    image = ProcessedImageField(
        upload_to='subcategories/',
        processors=[ResizeToFit(800, 800)],
        format='JPEG',
        options={'quality': 90},
        verbose_name='Изображение'
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} -> {self.name}"


class Product(models.Model):
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Подкатегория'
    )
    name = models.CharField(max_length=200, verbose_name='Наименование')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Slug')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    original_image = ProcessedImageField(
        upload_to='products/',
        processors=[ResizeToFit(1200, 1200)],
        format='JPEG',
        options={'quality': 95},
        verbose_name='Исходное изображение'
    )
    image_small = ImageSpecField(
        source='original_image',
        processors=[ResizeToFill(150, 150)],
        format='JPEG',
        options={'quality': 85}
    )
    image_medium = ImageSpecField(
        source='original_image',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 90}
    )
    image_large = ImageSpecField(
        source='original_image',
        processors=[ResizeToFill(600, 600)],
        format='JPEG',
        options={'quality': 90}
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def category(self):
        return self.subcategory.category


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина {self.user.username}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
