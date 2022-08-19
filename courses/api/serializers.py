from rest_framework import serializers

from ..models import Module, Subject, Course, Content


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']


class ModuleSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerialaizer(many=True, read_only = True)
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview',
                        'created', 'owner', 'modules']


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()


class ContentSerialazer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']

class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerialazer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title',  'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'subject', 'slug', 'overview', 'created', 'owener', 'modules']