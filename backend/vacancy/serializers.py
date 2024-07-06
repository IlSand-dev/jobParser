from rest_framework import serializers
from .models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer

from rest_framework import serializers
from .models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer


class SalarySerializer(serializers.ModelSerializer):

    def to_representation(self, data):
        currency = data.currency.abbr
        data = super(SalarySerializer, self).to_representation(data)
        data['currency'] = currency
        return data

    class Meta:
        model = Salary
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):

    def save(self):
        if Company.objects.filter(name=self.validated_data['name'], city=self.validated_data['city'],
                                  address=self.validated_data['address']).exists():
            return Company.objects.get(name=self.validated_data['name'], city=self.validated_data['city'],
                                       address=self.validated_data['address'])
        return super().save()

    class Meta:
        model = Company
        fields = "__all__"


class VacancySerializer(WritableNestedModelSerializer):
    salary = SalarySerializer(allow_null=True)
    experience = ExperienceSerializer(allow_null=True)
    company = CompanySerializer()

    class Meta:
        model = Vacancy
        fields = ("id", "name", "salary", "experience", "employment", "schedule", "company", "description", "href")
