# -*- coding: UTF-8 -*-
from django.db import models


class GeneralModelFields(models.Model):
    # logical deletion
    deleted = models.BooleanField(verbose_name='marked for removal', default=False)

    # last modified time
    mtime = models.DateTimeField(verbose_name='update time', auto_now=True)

    # creation time
    ctime = models.DateTimeField(verbose_name='created time', auto_now_add=True)

    class Meta:
        # Don't create the table
        abstract = True


class GeneralModelMethods:
    @staticmethod
    def format_datetime(datetime_object):
        return datetime_object.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def update_queryset(queryset: any, **kwargs):
        """
        About the update() instance method of the Django orm queryset object.
        Example of use: queryset.update(key=value)

        In this way, the return value obtained is the number of updated rows in the database
        table, and the queryset object will not be updated accordingly.

        Therefore, if you want to get the latest data from the database later, you can only
        get the queryset object again, Like this:

        queryset = models.ModelClassName.objects.filter(...)

        And if you need to reload a model's values from the database, you can use the
        refresh_from_db() method.

        In order to solve the above problems, the update() method of Django models is rewritten.

        You can update to the latest queryset by save() instance method.

        # models.Model.objects.update()
        # models.Model.save()
        """
        # We all know that after the design model adds 'auto_now=True' to the field,
        # modifying the data will automatically update the modification time.
        # If you use the update of django filter (usually when updating data in batches),
        # it is because the sql statement is called directly without going through the
        # model layer.
        # We need to assign the time 'datetime.datetime.now()' at the same time when using
        # the update update of the filter.
        # [fixed] https://blog.csdn.net/qq_41854273/article/details/88634837
        import datetime
        kwargs.update({
            'mtime': datetime.datetime.now()
        })

        # Get the updated field list
        fields_lists = list(kwargs.keys())

        # Get model object
        for q in queryset:
            # Code Example:
            # queryset.id = 999
            # setattr(queryset, 'id', '999')
            # _exec = lambda obj, variable, data: setattr(obj, variable, data)
            def _exec(obj: any, variable: str, data: str):
                setattr(obj, variable, data)

            # Use partial functions
            from functools import partial
            set_props = partial(_exec, obj=q)

            # Reflection set fields value
            for name, value in kwargs.items():
                set_props(variable=name, data=value)

            # Save into database
            q.save(update_fields=fields_lists)

        # Return QuerySet object
        return queryset
