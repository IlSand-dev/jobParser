from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from .parser import HHParser
from .hhAPI import get_vacancies
from rest_framework import generics


class SearchVacanciesView(APIView):
    def get(self, request):
        vacancies, pages = get_vacancies(**request.query_params)
        data = []
        for vacancy in vacancies:
            if Vacancy.objects.filter(href=vacancy['href']).exists():
                serializer = VacancySerializer(Vacancy.objects.get(href=vacancy['href']), data=vacancy)
            else:
                serializer = VacancySerializer(data=vacancy)
            if serializer.is_valid():
                serializer.save()
                data.append({
                    "id": serializer.data['id'],
                    "name": serializer.data['name']
                })
            else:
                print(serializer.data)
                print(serializer.errors)
                break

        return Response({"items": data, "pages": pages})


class VacancyView(generics.RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer