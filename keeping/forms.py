# -*- coding: utf-8 -*-
# Time: 2020/12/27 10:18
# Author: 201816040311_刘晨辉
# FileName: forms.py

from .models import *
from django import forms
from captcha.fields import CaptchaField

THINGS_STYLE = (('e',"教育"),('l',"生活"),('m',"医疗"),('f',"理财"),('s',"工资"))

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)
    captcha = CaptchaField(label='验证码')


class IncomeForm(forms.ModelForm):
    # detail = forms.CharField(max_length=255)
    # inmoney = forms.IntegerField()
    # things = forms.MultipleChoiceField(label=u'活动类型', choices=THINGS_STYLE, widget=forms.CheckboxSelectMultiple())
    class Meta:
        model=income
        exclude = ['userID']

# class StatForm(forms.Form):
#     stat_year = forms.IntegerField(label="按年份查询")
#     stat_day  = forms.IntegerField(label="按日查询")
#     stat_month = forms.IntegerField(label="按月份查询")

class OutcomeForm(forms.ModelForm):
    class Meta:
        model=outcome
        exclude = ['userID']

class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)
    password2 = forms.CharField(label="确认密码", max_length=256,widget=forms.PasswordInput)
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput)
    captcha = CaptchaField(label='验证码')
