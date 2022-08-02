from django import forms
from django.forms.models import inlineformset_factory

from .models import Course, Module


ModuleFormSet = inlineformset_factory(Course,
                                        Module,
                                        fields=['title', 
                                                'description'],
                                        extra=2,
                                        can_delete=True)

'''
You build it using the inlineformset_
factory() function provided by Django. Inline formsets are a small abstraction
on top of formsets that simplify working with related objects. This function allows
you to build a model formset dynamically for the Module objects related to a
Course object.
'''