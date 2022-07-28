from django.db import models
from django.utils import timezone	# for "default" argument in DateTimeField
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name.title()

	def get_absolute_url(self):
		return reverse('home')

class Tags(models.Model):
	name = models.CharField(max_length=50)	# always restart server whenever adding a new Tag for Posts. 
	def __str__(self):
		return self.name.title()


class Post(models.Model):
	title = models.CharField(max_length=100)
	slug = models.SlugField(default='', blank=True)
	# header image
	def post_header_directory(instance, filename):
		return 'users/{}/post_images/{}/header/{}'.format(instance.author.username, instance.title, filename)
	header_image = models.ImageField(null=True, blank=True, upload_to=post_header_directory)

	content = RichTextUploadingField(blank=True, null=True)#models.TextField(blank=True, null=True)
	date_posted = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE) # ForeignKey is for relationship with another model
	likes = models.ManyToManyField(User, related_name = "posts", blank=True) # "posts" was used in views.py's context_object_name
	def total_likes(self):
		return self.likes.count()

	tag = models.CharField(max_length=50, default="#no-tag", help_text="Please limit to 1 hashtag - 50 chars max.")

	category = models.CharField(max_length=50, default="general", help_text="Choose which best suits your article's content.")

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'slug': self.slug})

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)
		# downsizing header_image, if there's any
		if self.header_image:
			header_img = Image.open(self.header_image.path)			# open the image of the current instance
			if header_img.height > 700 or header_img.width > 700:	# for sizing-down the images to conserve memory in the server
				output_size = (700, 700)
				header_img.thumbnail(output_size)
				header_img.save(self.header_image.path)

