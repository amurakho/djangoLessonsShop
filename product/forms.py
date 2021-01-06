from django import forms

from product import models


class SearchForm(forms.Form):

    search_field = forms.CharField(max_length=100)


def star_valid(value):
    if value > 5:
        raise forms.ValidationError(message='Invalid rating')
    else:
        return value


class ReviewForm(forms.ModelForm):

    stars = forms.IntegerField(validators=(star_valid, ))

    class Meta:
        model = models.Review
        fields = ('text', 'stars', )


class ProductBuyForm(forms.Form):

    count = forms.IntegerField()
    product_slug = forms.CharField(widget=forms.HiddenInput())