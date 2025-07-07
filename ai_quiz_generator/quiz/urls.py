app_name = 'quiz'
from django.urls import path
from . import views

urlpatterns = [
   path("", views.home, name="home"), 
   path('create-quiz', views.create_quiz, name="create-quiz"),
   path('view/<int:pdf_id>/', views.view_quiz, name= 'view_quiz'),
]

