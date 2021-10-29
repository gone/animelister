from django import forms
from .models import UserRating


class UserRatingForm(forms.ModelForm):
    required_css_class = "is-link"
    error_css_class = "is-danger"
    rating = forms.IntegerField(
        help_text="rating from 1-10",
        widget=forms.NumberInput(
            attrs={"class": "input", "placeholder": "Rating (1-10)"}
        ),
    )

    class Meta:
        model = UserRating
        fields = ["rating", "anime", "user", "id"]

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating > 10:
            raise forms.ValidationError("rating must be less than 10")
        return rating
