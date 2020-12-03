import os
from mimetypes import MimeTypes
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.db.models.functions import Length
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from wsgiref.util import FileWrapper
from django import forms
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	RedirectView
	)
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from blog.models import Post, Comment, Post2, Photo


class PostList(ListView):
 	model = Post

class PostCreate(CreateView):
	model = Post
	fields = ['image', 'description', 'author']
	success_url = '/'


class CommentForm(forms.Form):
	comment = forms.CharField()

class PostDetail(DetailView):
	model = Post

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['comment_form'] = CommentForm()
		return context

	def post(self, request, *args, **kwargs):
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			comment = Comment(
				author=request.user,
				post=self.get_object(),
				text=comment_form.cleaned_data['comment']
			)
			comment.save()
		else:
			raise Exception
		return redirect(reverse('detail', args=[self.get_object().id]))

# Create your views here.
def home(request):
	context = {
	'posts':Post2.objects.all(),
	'title': 'Home Page'
	}
	return render(request, 'blog/home.html', context)

class PhotoListView(ListView):
	model = Photo
	template_name = 'blog/gallery.html'
	context_object_name = 'photos'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		
		photos = Photo.objects.all()
		if 'order' in self.kwargs:
			param_order = self.kwargs['order']
			if param_order == 'old-to-new':
				context['photos'] = Photo.objects.order_by('created')
			elif param_order == 'new-to-old':
				context['photos'] = Photo.objects.order_by('-created')
			else:
				context['photos'] = Photo.objects.annotate(num_votes = Count('total_votes')).order_by('-num_votes')
		
		lower_third = len(Photo.objects.all())/3
		context['lower_third'] = lower_third
		context['upper_third'] = 2 * lower_third
		return context

class PersonalListView(ListView):
	model = Photo
	template_name = 'blog/personal_list.html'
	context_object_name = 'photos'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)	
		user = self.request.user

		for p in (Photo.objects.all()):
			print(p.saved_by)
		context['photos'] = Photo.objects.filter(saved_by = user)

		lower_third = len(context['photos'])/3
		context['lower_third'] = lower_third
		context['upper_third'] = 2 * lower_third

		return context


class PhotoDetailView(DetailView):
	model = Photo

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['comment_form'] = CommentForm()
		detail_photo = self.get_object()
		if self.request.user in detail_photo.saved_by.all():
			context['saved_by_this_user'] = True
		else:
			context['saved_by_this_user'] = False

		return context

	def post(self, request, *args, **kwargs):
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			comment = Comment(
				author=request.user,
				post=self.get_object(),
				text=comment_form.cleaned_data['comment']
			)
			comment.save()
		else:
			raise Exception
		return redirect(reverse('photo-detail', args=[self.get_object().id]))



class PhotoCreateView(LoginRequiredMixin, CreateView):
	model = Photo
	fields = ['image', 'description']
	redirect = 'gallery/'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Photo
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PhotoVoteToggle(LoginRequiredMixin, RedirectView):

	def get_redirect_url(self, *args, **kwargs):
		obj = get_object_or_404(Photo, pk = self.kwargs['pk'])
		url = self.request.META.get('HTTP_REFERER')
		user = self.request.user
		if user.is_authenticated:
			if user in obj.total_votes.all():
				obj.total_votes.remove(user)
			else:
				obj.total_votes.add(user)

		return url

class PhotoSaveView(LoginRequiredMixin, RedirectView):

	def get_redirect_url(self, *args, **kwargs):
		obj = get_object_or_404(Photo, pk = self.kwargs['pk'])
		pk = self.kwargs['pk']
		url = f'/photos/{pk}'
		print(url)
		user = self.request.user
		if user.is_authenticated:
			if user in obj.saved_by.all():
				print('un do the save')
				obj.saved_by.remove(user)
			else:
				print('save')
				obj.saved_by.add(user)

		return url

@login_required
def download_image(request, pk):
    img = Photo.objects.get(id=pk)
    inputfile = os.getcwd()+img.image.url
    print(inputfile)
    print('-----------------')
    mime = MimeTypes()
    wrapper      = FileWrapper(open(inputfile,'rb')) # img.file returns full path to the image
    content_type = mime.guess_type(inputfile)[0]  # Use mimetypes to get file type
    print(content_type)
    response     = HttpResponse(wrapper,content_type=content_type)  
    response['Content-Length']      = os.path.getsize(inputfile)    
    response['Content-Disposition'] = "attachment; filename=%s" %  img.image.name
    return response

class PostListView(ListView):
	model = Post2
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']

class PostDetailView(DetailView):
	model = Post2

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post2
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post2
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post2
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

def about(request):
	return render(request, 'blog/about.html', {'title':'About the boys'})


