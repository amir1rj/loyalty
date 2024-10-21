from django import forms
from django.core.exceptions import ValidationError

from .models import PointRole, PointRoleGroup, Reward

class PointRoleForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = PointRole
        fields = ['id', 'number', 'from_date', 'to_date', 'point_role_type', 'priority', 'is_active', 'reward']

    def __init__(self, *args, **kwargs):
        super(PointRoleForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['id'].initial = self.instance.pk
            self.fields['id'].widget.attrs['readonly'] = True


class CreatePointRoleForm(forms.ModelForm):
    class Meta:
        model = PointRole
        exclude = ('user', 'user_logs')


class CreatePointRoleGroupForm(forms.ModelForm):
    class Meta:
        model = PointRoleGroup
        fields = '__all__'


class CreateRewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = '__all__'
