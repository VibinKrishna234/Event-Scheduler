from django.db import models
from django.urls import reverse
from mapbox_location_field.models import LocationField
from ckeditor_uploader.fields import RichTextUploadingField


class EventCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=6, unique=True)
    image = models.ImageField(upload_to='event_category/')
    priority = models.IntegerField(unique=True)
    created_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_user')
    updated_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='updated_user')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)
    status_choice = (
        ('disabled', 'Disabled'),
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        ('blocked', 'Blocked'),
        ('completed', 'Completed'),
    )
    status = models.CharField(choices=status_choice, max_length=10)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event-category-list')


class Event(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = RichTextUploadingField()
    select_scheduled_status = (
        ('yet to scheduled', 'Yet to Scheduled'),
        ('scheduled', 'Scheduled')
    )
    scheduled_status = models.CharField(max_length=25, choices=select_scheduled_status)
    start_date = models.DateField()
    end_date = models.DateField()
    created_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True,
                                     related_name='event_created_user')
    updated_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True,
                                     related_name='event_updated_user')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)
    status_choice = (
        ('disabled', 'Disabled'),
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        ('time out', 'Time Out'),
        ('completed', 'Completed'),
        ('cancel', 'Cancel'),
    )
    status = models.CharField(choices=status_choice, max_length=10)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event-list')

    def created_updated(model, request):
        obj = model.objects.latest('pk')
        if obj.created_by is None:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


class EventImage(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_image/')


class EventAgenda(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
