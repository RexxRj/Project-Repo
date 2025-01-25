from django.urls import path

from . import views

urlpatterns = [
    
    path('',views.StartingPageView.as_view(),name='index'),
    path('transactions/',views.AllTransactionsView.as_view(),name='transactions-page-default'),
    path('transactions/<int:pageno>',views.AllTransactionsView.as_view(),name='transactions-page'),
    path('dashboard/',views.DashboardView.as_view(),name='dashboard-page'),
    path('categories/',views.CategoriesView.as_view(),name='categories-page-default'),
    path('categories/<int:pageno>',views.CategoriesView.as_view(),name='categories-page')
]
