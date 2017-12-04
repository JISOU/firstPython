from django.shortcuts import render , get_object_or_404 ,redirect
from django.utils import timezone
#from . import models
from .models import Post
from .forms import PostForm

# Create your views here.

def post_list(request):
	## . 현재 디렉토리 표시 (동일한 디렉토리)
	## from . import models 하였을때 전제 경로를 써줘야함 models.Post.objects .....
	#posts = models.Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	## from .models import Post 명시적으로 지정할때는  Post.objects....
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html' ,{'posts' : posts} )

def post_detail(request,pk):
	post = get_object_or_404(Post , pk=pk)
	return render(request,'blog/post_detail.html' ,{'post' : post })

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk = post.pk)
	else:
		form = PostForm()
		return render(request, 'blog/post_edit.html' ,{'form' : form} )

def post_edit(request,pk):
	post = get_object_or_404(Post,pk = pk)
	if request.method =="POST":
		form = PostForm(request.POST, instance = post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk = post.pk)
	else:
		form = PostForm( instance = post)
		return render(request, 'blog/post_edit.html' ,{'form' : form} )