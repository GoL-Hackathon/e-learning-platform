from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.apps import apps
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Count
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from students.forms import CourseEnrollForm

from .forms import ModuleFormSet
from .models import Content, Course, Module, Subject

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
class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, 
                                PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


# Will use for the CreateView and UpdateView views
class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'

'''
Subclasses of OwnerCourseMixin

PermissionRequiredMixin checks that the user accessing the view has the
permission specified in the permission_required attribute. Your views are
now only accessible to users with proper permissions.
'''
# Lists the courses created by the user
class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'

# Uses a model form to create a new Course object.
class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

# Allows the editing of an existing Course object
class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'
    

# Inherits from OwnerCourseMixin and the generic DeleteView.
class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


'''
The CourseModuleUpdateView view handles the formset to add, update, and
delete modules for a specific course.
'''
class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    # To avoid repeating the code to build the formset.
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    '''
    # This method is provided by the View class. It takes an HTTP
     request and its parameters and attempts to delegate to a lowercase method
     that matches the HTTP method used.
    '''
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request,pk)

    def get(self, requset, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})
        
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


# allows you to create and update different models' contents
class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'


    '''
    Check that the given model name is one of the four
    content models: Text, Video, Image, or File. Then use Django's apps
    module to obtain the actual class for the given model name. If the given
    model name is not one of the valid ones, return None.
    '''
    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                    model_name=model_name)
        return None

    '''
    You build a dynamic form using the modelform_factory() function of the form's framework.
    use the exclude parameter to specify the common fields to exclude from the form and let all other
    attributes be included automatically
    '''
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude={'owner',
                                                'order',
                                                'created',
                                                'updated'})
        return Form( *args, **kwargs)

    '''
    It receives the following URL parameters and stores the
    corresponding module, model, and content object as class attributes
    '''
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)

        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, 
                                        id=id,
                                        owner=request.user)  
        return super().dispatch(request, module_id, model_name, id)  


    '''
    Executed when a GET request is received. You build the model
    form for the Text, Video, Image, or File instance that is being updated.
    Otherwise, you pass no instance to create a new object, since self.obj
    is None if no ID is provided.
    '''
    def get(self, request, module_id, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    '''
    Executed when a POST request is received. You build the model
    form, passing any submitted data and files to it. Then, you validate it. If the
    form is valid, you create a new object and assign request.user as its owner
    before saving it to the database. You check for the id parameter. If no ID is
    provided, you know the user is creating a new object instead of updating an
    existing one. If this is a new object, you create a Content object for the given
    module and associate the new content with it.
    '''
    def post(self, request, module_id, model_name, id=None):   
        form = self.get_form(self.model,
                                instance=self.obj,
                                data=request.POST,
                                files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            if not id:
                # new content
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)

        return self.render_to_response({'form': form,
                                        'object': self.obj})


# Retrieves the Content object with the given ID. It deletes the related Text, Video, Image, or File object
class ContentDeleteView(View):

    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)                 


# Display all modules for a course and list the contents of a specific module.
class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, 
                                    id=module_id,
                                    course__owner=request.user)
        return self.render_to_response({'module': module})


#  A view that receives the new order of module IDs encoded in JSON.'
class ModuleOrderView(CsrfExemptMixin, 
                        JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, 
                        JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                                    module__course__owner=request.user) \
                                        .update(order=order)
            return self.render_json_response({'saved': 'OK'})

            

# Displaying courses views
class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(total_courses=Count('courses'))
        courses = Course.objects.annotate(total_modules=Count('modules'))

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({ 'subjects': subjects, 
                                        'subject': subject,
                                        'courses': courses})
        

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    # Enroll button form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})

        return context