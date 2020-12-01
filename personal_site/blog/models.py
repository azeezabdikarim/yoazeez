from django.db import models
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class BlogPost(models.Model):

	title = models.CharField(max_length=120, null=True, blank=False)

	subtitle = models.CharField(max_length=180, null=True, blank=False)

	slug = models.CharField(max_length = 240, null=True, blank=False)

	body = models.TextField()

	created_at = models.DateTimeField(auto_now_add=True, null=False)

	updated_at = models.DateTimeField(auto_now=True, null=False)

class Post(models.Model):
	image = models.ImageField()
	description = models.TextField()
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

class PostList(ListView):
 	model = Post

class Post2(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post2-detail', kwargs={'pk':self.pk})

class Photo(models.Model):
	image = models.ImageField(upload_to='gallery_photos')
	description = models.TextField()
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	total_votes = models.ManyToManyField(User, related_name = "votes")
	saved_by = models.ManyToManyField(User, related_name = "saves")

	# upvotes = models.IntegerField(default = 0)

	def __str__(self):
		return f'{self.image.name} Profile'

	def get_absolute_url(self):
		return reverse('photo-detail', kwargs={'pk':self.pk})

class Comment(models.Model):
	post = models.ForeignKey(Photo, on_delete=models.CASCADE)
	text = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def get_absolute_url(self):
		return reverse('photo-detail', kwargs={'pk':self.pk})


