from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # When there is no current value
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs  = qs.filter(**query)
                
                # Get the order for the last item
                last_item = qs.latest(self.attname)
                value = last_item.order +1

            except ObjectDoesNotExist:
                value = 0

            setattr(model_instance, self.attname, value)
            return value

        else:
            return super().pre_save(model_instance, add)

        ## NB: qs is QuerySet
        '''
        When you create custom model fields, make them generic. Avoid
        hardcoding data that depends on a specific model or field. Your
        field should work in any model.
        '''
