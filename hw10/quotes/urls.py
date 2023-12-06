from django.urls import path

from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('<int:page>', views.index, name='index_paginate'),
    path('quotes/<int:author_id>/', views.author_detail, name='author_detail'),
    path('quotes/<str:tag>/', views.tag_search, name='tag_search')
]
