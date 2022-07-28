from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	FormView,
	)
from .forms import PostForm #, PostCommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse





# trying out multiple objects inside one class-based listView template
class BlogHomeView(ListView):
    context_object_name = 'posts'    
    template_name = 'blog/home.html'
    queryset = Post.objects.all()
    ordering = ['-date_posted']			# filter for newest post first
    paginate_by = 10					# number of posts to show per page

    def get_context_data(self, **kwargs):
        context = super(BlogHomeView, self).get_context_data(**kwargs)
        return context


class PostDetailView(DetailView): # LoginRequiredMixin for authed users
	model = Post
	template_name = 'blog/postdetail.html'
	posts = Post.objects.all()
	context = {
		'posts': posts,
	}


class PostCreateView(LoginRequiredMixin, CreateView):		
	model = Post
	form_class = PostForm
	template_name = 'blog/postcreateform.html'
	success_message = "Successfully posted!"
	success_url = '/blogs'		# using this takes the user to a specific page after posting

	def form_valid(self, form):			# to automatically get the id of the current logged-in user as the author
		form.instance.author = self.request.user 	# set the author to the current logged-in user
		return super().form_valid(form)
		

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post 
	form_class = PostForm	# blogPostForm was the one used in the tutorials
	template_name = 'blog/postupdateform.html'
	success_message = "Post updated"
	# success_url = '/blog'

	def form_valid(self, form):			
		form.instance.author = self.request.user 	#to automatically get the id of the current logged-in user as the author
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()

		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):		
	model = Post
	template_name = 'blog/postconfirmdelete.html'
	success_url = '/blog'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()

		if self.request.user == post.author:
			return True
		return False		

class CategoryCreateView(LoginRequiredMixin, CreateView):
	'''
		Take note that this view may only be intended for admins. If the site has many users all of users of the site are able to access
		this page, category list for posts may become chaotic. Please handle appropriately and have it removed if needed.
	'''	
	model = Category
	fields = '__all__'
	template_name = 'blog/categorycreateform.html'
	success_url = '/blogs'		

	def form_valid(self, form):			# to automatically get the id of the current logged-in user as the author
		form.instance.author = self.request.user 	# set the author to the current logged-in user
		return super().form_valid(form)

def CategoryView(request, cats):
	category_posts = Post.objects.filter(category=cats)
	context = {
		'cats': cats,
		'category_posts': category_posts,
	}
	return render(request, 'blog/categories.html', context)








