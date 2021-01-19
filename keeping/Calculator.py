# -*- coding: utf-8 -*-
# 用来计算总和或者总差
# Time: 2020/12/28 10:58
# Author: 201816040311_刘晨辉
# FileName: Calculator.py
from django.db.models.query import QuerySet

def CalI(queryset):
    num = 0
    for que in queryset:
        num += que.inmoney

    return num

def CalO(queryset):
    num = 0
    for que in queryset:
        num += que.outmoney

    return num