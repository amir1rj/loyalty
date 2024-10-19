from django import forms
from django.core.exceptions import ValidationError

from .models import PointRole


class PointRoleForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)  # Hidden field to store the id

    class Meta:
        model = PointRole
        fields = ['id', 'number', 'from_date', 'to_date', 'point_role_type', 'priority', 'is_active']

    def __init__(self, *args, **kwargs):
        super(PointRoleForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['id'].initial = self.instance.pk
            self.fields['id'].widget.attrs['readonly'] = True
