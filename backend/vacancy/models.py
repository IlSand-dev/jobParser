from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    abbr = models.CharField(max_length=5)

class Salary(models.Model):
    minimal = models.IntegerField(null=True)
    maximum = models.IntegerField(null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)


class Experience(models.Model):
    minimal = models.IntegerField(null=True)
    maximum = models.IntegerField(null=True)

class Company(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True)

class Vacancy(models.Model):
    name = models.CharField(max_length=100)
    salary = models.OneToOneField(Salary, on_delete=models.SET_NULL, null=True)
    experience   = models.OneToOneField(Experience, on_delete=models.SET_NULL, null=True)
    employment = models.CharField(max_length=50)

    schedule = models.CharField(max_length=20)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    description = models.TextField()

    href = models.CharField(max_length=255)