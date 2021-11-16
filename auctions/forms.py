from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, Form
from django import forms

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class CreateListing(forms.ModalForm):
    title = forms.CharField(
        min_length=4,
        max_length=100,
        label="Title",
        widget=forms.TextInput(
            attrs={"placeholder": "Title", "class": "form-control" "mb-3"}
        ),
    )
    description = forms.CharField(
        max_length=1000,
        label="Description",
        widget=forms.TextInput(
            attrs={"placeholder": "Description", "class": "form-control" "mb-3"}
        ),
    )
    starting_bid = forms.DecimalField(
        label="Starting Bid",
        widget=forms.NumberInput(
            attrs={"placeholder": "Starting Bid", "class": "form-control" "mb-3"}
        ),
    )
    category = forms.ChoiceField(
        choices=[