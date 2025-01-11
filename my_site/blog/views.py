from django.shortcuts import render
from datetime import date
from django.views.generic import ListView,DetailView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post

from .forms import CommentForm

class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = "posts"
    
    def get_queryset(self):
        querySet = super().get_queryset()
        querySet = querySet[:3]
        return querySet

# def index(request):
    
#     latest_posts = Post.objects.all().order_by('-date')[:3]
    
#     return render(request, 'blog/index.html',{
#         "posts": latest_posts
#     })

class AllPostsView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    ordering = ['-date']
    context_object_name = "posts"

# def posts(request):
    
#     sorted_posts = Post.objects.all().order_by('-date')
    
#     return render(request, 'blog/all-posts.html',{
#         "posts": sorted_posts
#     })

class PostDetailsView(View):
    
    def get(self,request,slug):
            post = Post.objects.get(slug=slug)
            context = {
                "post_detail": post,
                "post_tags": post.tags.all(),
                "comment_form": CommentForm(),
                "comments": post.comments.all().order_by("-id")
            }
            
            return render(request,"blog/post-details.html",context)
        
    
    def post(self,request,slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-details-page",args=[slug]))
        
        
        context = {
            "post_detail": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id")
        }
        
        return render(request,"blog/post-details.html",context)

# def post_details(request, slug):
    
#     post_detail = Post.objects.get(slug=slug)
    
#     return render(request, 'blog/post-details.html', {'post_detail': post_detail,
#                                                       'post_tags': post_detail.tags.all()})