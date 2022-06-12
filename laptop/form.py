from django import forms
from laptop.models import Laptop

class UploadForm(forms.ModelForm):
    discount = forms.IntegerField(required=False)
    class Meta:
        model = Laptop
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 15}),
        }
        fields = ["title", "description", "image", "price", "discount"]
