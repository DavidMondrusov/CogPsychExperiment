from django.urls import path
from . import views
from .views import submit_score, get_scores

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('submit-score/', submit_score, name='submit_score'), 
    path('scores/', get_scores, name='get_scores'),
]   