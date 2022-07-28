from django.db import models
from django.utils import timezone	# for "default" argument in DateTimeField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Quote(models.Model):
	title = models.CharField(max_length=255, blank=True, null=True)
	by = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.title

class Announcement(models.Model):
	title = models.CharField(max_length=100)
	content = RichTextUploadingField(blank=True, null=True)
	date_posted = models.DateTimeField(auto_now_add=True) #you can use "(default=timezone.now)" instead but the timezone import is needed
	date_modified = models.DateTimeField(auto_now=True) # shows the actual time the post was modified // everytime it is modified
	author = models.ForeignKey(User, on_delete=models.CASCADE) # ForeignKey is for relationship with another model

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('announcement-detail', kwargs={'pk': self.pk})