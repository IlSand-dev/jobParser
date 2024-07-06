from django.urls import path
from vacancy.views import *

urlpatterns =[
    path('vacancySearch/', SearchVacanciesView.as_view()),
    path('vacancy/<int:pk>', VacancyView.as_view())
]