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
    
    def is_stored_post(self,request,post):
        stored_posts = request.session.get('stored_posts')
            
        if stored_posts is not None:
            is_saved_for_later = post.id in stored_posts
        else:
            is_saved_for_later = False
        
        return is_saved_for_later
    
    def get(self,request,slug):
            post = Post.objects.get(slug=slug)
            
            
            
            context = {
                "post_detail": post,
                "post_tags": post.tags.all(),
                "comment_form": CommentForm(),
                "comments": post.comments.all().order_by("-id"),
                "saved_for_later": self.is_stored_post(request,post)
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
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request,post)
        }
        
        return render(request,"blog/post-details.html",context)

# def post_details(request, slug):
    
#     post_detail = Post.objects.get(slug=slug)
    
#     return render(request, 'blog/post-details.html', {'post_detail': post_detail,
#                                                       'post_tags': post_detail.tags.all()})


class ReadLaterView(View):
    
    def get(self,request):
        
        stored_posts = request.session.get('stored_posts')
        
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context['posts'] = posts
            context['has_posts'] = True
        
        return render(request,'blog/stored-posts.html',context)
    
    
    def post(self,request):
        
        stored_posts = request.session.get('stored_posts')
        
        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST['post_id'])
        
        if post_id not in stored_posts:
            stored_posts.append(post_id)
            
        else:
            stored_posts.remove(post_id)
        
        request.session['stored_posts'] = stored_posts
        
        return HttpResponseRedirect("/")