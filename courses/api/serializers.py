from rest_framework import serializers

from ..models import Module, Subject, Course


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'title', 'slug')


class ModuleSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerilaizer(many=True, read_only = True)
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview',
                        'created', 'owner', 'modules']