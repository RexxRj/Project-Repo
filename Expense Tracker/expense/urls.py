from django.urls import path

from . import views

urlpatterns = [
    
    path('',views.StartingPageView.as_view(),name='index'),
    path('transactions/',views.AllTransactionsView.as_view(),name='transactions-page-default'),
    path('transactions/<int:pageno>',views.AllTransactionsView.as_view(),name='transactions-page')
]
