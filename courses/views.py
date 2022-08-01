from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Course


# Create your views here.
'''
OwnerMixin implements the get_queryset() method,
which is used by the views to get the base QuerySet. Your mixin will override this
method to filter objects by the owner attribute to retrieve objects that belong to the
current user (request.user).

OwnerEditMixin implements the form_valid() method, which is used by views
that use Django's ModelFormMixin mixin, that is, views with forms or model
forms such as CreateView and UpdateView. form_valid() is executed when
the submitted form is valid.

Your OwnerMixin class can be used for views that interact with any model that
contains an owner attribute.
'''

class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# OwnerCourseMixin class that inherits OwnerMixin
class OwnerCourseMixin(OwnerMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


# Will use for the CreateView and UpdateView views
class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'

'''
Subclasses of OwnerCourseMixin
'''
# Lists the courses created by the user
class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'

# Uses a model form to create a new Course object.
class CourseCreateView(OwnerCourseEditMixin, CreateView):
    pass

# Allows the editing of an existing Course object
class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    pass

# Inherits from OwnerCourseMixin and the generic DeleteView.
class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'

    