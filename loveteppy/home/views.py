from django.shortcuts import render
from .models import Announcement, Quote
from blog.models import Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# for needing user to be logged-in first before accessing the page requested
from django.contrib.auth.decorators import login_required


# @login_required
def home(request):
	'''
		note how I used two ways to display info to the view:
		one was thru a variable passing it as the "value" for the dictionary key,
		the other is thru directly using the imported model as the "value".

		A bit messy but I was experimenting and didn't want to change it for future reference.
	'''
	context = {
		'posts': Post.objects.all().order_by("-date_posted"),
		'announcements': Announcement.objects.all().order_by("-date_posted"),
		'quotes': Quote.objects.all(),
		'quotescount': Quote.objects.count()+1, #+1 because there's a hard-coded quote on html page: fall seven times; stand-up eight
		'postcount': Post.objects.count(),
	}

	# template_folder/html_file
	return render(request, 'home/index.html', context)


def about(request):
	return render(request, 'home/about.html')



