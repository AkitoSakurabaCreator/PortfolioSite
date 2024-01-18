from django import forms
from allauth.account.forms import SignupForm
from bootstrap_datepicker_plus.widgets import DatePickerInput

from accounts.models import CustomUser
from django.core.exceptions import ValidationError


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='姓', required=True)
    last_name = forms.CharField(max_length=30, label='名', required=True)
    nick_name = forms.CharField(max_length=30, label='ニックネーム', required=False)
    user_screen_id = forms.CharField(max_length=30, label='ユーザーID', required=True)
    zipcode = forms.RegexField(label='郵便番号(ハイフンなし)',
        regex=r'^[0-9]+$',
        max_length=7,
        widget=forms.TextInput(), required=False
        )
    address = forms.CharField(max_length=30, label='住所', required=False)
    buildingname = forms.CharField(max_length=30, label='建物名(任意)', required=False)
    tel = forms.CharField(max_length=30, label='電話番号', required=False)
    job = forms.CharField(max_length=30, label='職業(任意)', required=False)
    year = forms.CharField(
            label='生年月日',
            widget = DatePickerInput(
            format='%Y/%m/%d',
            attrs={'readonly': 'true','id': 'year'},
            options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                    'ignoreReadonly': True,
                    'allowInputToggle': True
                    }))
    
    avatar = forms.ImageField(label="プロフィール画像", required=False)


class SignupUserForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    read_terms = forms.BooleanField(
        label="利用規約同意",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'check'}),
    )

    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.read_terms = self.cleaned_data['read_terms']
        user.save()
        return user

class Inquiry(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    first_name = forms.CharField(max_length=30, label="姓")
    last_name = forms.CharField(max_length=30, label="名")
    title = forms.CharField(max_length=100, label="件名")
    summary = forms.CharField(label="お問い合わせ内容", widget=forms.Textarea)
    read_field = forms.BooleanField(
        label="お問い合わせ送信確認",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'check'}),
    )