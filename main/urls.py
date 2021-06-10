from django.urls import path

from .views import TestSetListView, TestDetailView, TestSetDetailView


urlpatterns = [
    path('', TestSetListView.as_view(), name='testsets'),
    path('test/<int:pk>', TestDetailView.as_view(), name='test'),
    path('testset/<int:pk>', TestSetDetailView.as_view(), name='testset'),
]
