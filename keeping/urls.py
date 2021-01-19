# -*- coding: utf-8 -*-
# Time: 2020/12/26 19:44
# Author: 201816040311_刘晨辉
# FileName: urls.py
from django.urls import path,include,re_path
from . import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', include('keeping.urls')),
    path('index/',views.index,name='index'),
    path('login/', views.login,name='login'),
    path('register/', views.register,name='regerster'),
    path('logout/',views.logout,name='logout'),
    path('captcha/', include('captcha.urls')),
    path('confirm/', views.user_confirm),
    path('incomes/', views.incomes,name='incomes'),
    path('outcomes/', views.outcomes,name='outcomes'),
    path('statistics/', views.statistics,name='statistics'),
    path('show_edu/', views.show_edu,name='show_edu'),
    path('show_lif/', views.show_lif,name='show_lif'),
    path('show_med/', views.show_med,name='show_med'),
    path('show_sal/', views.show_sal,name='show_sal'),
    path('show_income/', views.show_income,name='show_income'),
    path('show_outcome/', views.show_outcome,name='show_outcome'),
]