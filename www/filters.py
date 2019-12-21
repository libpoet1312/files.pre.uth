import django_filters
from .models import File, Course
from django import forms

class FileFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = File
        fields = ['title', 'summary']