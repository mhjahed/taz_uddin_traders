# shop/forms.py
from django import forms
from .models import Product, ProductImage, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 
                  'stock_quantity', 'minimum_order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_primary']

ProductImageFormSet = forms.inlineformset_factory(
    Product, ProductImage,
    form=ProductImageForm,
    extra=3,
    can_delete=True
)