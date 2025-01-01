from django.shortcuts import render
from datetime import date
from .models import Post

# all_posts = [
#     {
#         "slug": "hike-in-the-mountains",
#         "image": "mountains.jpg",
#         "author": "Rexx",
#         "date": date(2021, 7, 21),
#         "title": "Mountain Hiking",
#         "excerpt": "There's nothing like the views you get when hiking in the mountains!",
#         "content": """
#         Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quibusdam debitis adipisci quae fugit earum doloribus ipsum corporis est, distinctio asperiores, blanditiis eius illum eos tenetur vel corrupti nihil quaerat aperiam.
#         Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quibusdam debitis adipisci quae fugit earum doloribus ipsum corporis est, distinctio asperiores, blanditiis eius illum eos tenetur vel corrupti nihil quaerat aperiam.
#         Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quibusdam debitis adipisci quae fugit earum doloribus ipsum corporis est, distinctio asperiores, blanditiis eius illum eos tenetur vel corrupti nihil quaerat aperiam.
#         """
#     },
#     {
#         "slug": "into-the-woods",
#         "image": "woods.jpg",
#         "author": "Barsha",
#         "date": date(2022, 7, 22),
#         "title": "Into the Woods",
#         "excerpt": "Get lost in the woods with me and enjoy the sounds of nature.",
#         "content": """
#         Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quibusdam debitis adipisci quae fugit earum doloribus ipsum corporis est, distinctio asperiores, blanditiis eius illum eos tenetur vel corrupti nihil quaerat aperiam.
#         Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quibusdam debitis adipisci quae fugit earum doloribus ipsum corporis est, distinctio asperiores, blanditiis eius illum eos tenetur vel corrupti nihil quaerat aperiam.
#         Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quibusdam debitis adipisci quae fugit earum doloribus ipsum corporis est, distinctio asperiores, blanditiis eius illum eos tenetur vel corrupti nihil quaerat aperiam.
#         """
#     },
#     {
#         "slug": "coding-is-fun",
#         "image": "coding.jpg",
#         "author": "Rexx",
#         "date": date(2024, 8, 16),
#         "title": "Programming is fun",
#         "excerpt": "Programming is fun and challenging. It's a great way to exercise your brain.",
#         "content": """
#         Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quibusdam debitis adipisci quae fugit earum doloribus ipsum corporis est, distinctio asperiores, blanditiis eius illum eos tenetur vel corrupti nihil quaerat aperiam.
#         Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quibusdam debitis adipisci quae fugit earum doloribus ipsum corporis est, distinctio asperiores, blanditiis eius illum eos tenetur vel corrupti nihil quaerat aperiam.
#         Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quibusdam debitis adipisci quae fugit earum doloribus ipsum corporis est, distinctio asperiores, blanditiis eius illum eos tenetur vel corrupti nihil quaerat aperiam.
#         """
#     }
# ]

# sorted_posts = sorted(all_posts, key=lambda post: post['date'], reverse=True)
# latest_posts = sorted_posts[:3]

def index(request):
    
    latest_posts = Post.objects.all().order_by('-date')[:3]
    
    return render(request, 'blog/index.html',{
        "posts": latest_posts
    })

def posts(request):
    
    sorted_posts = Post.objects.all().order_by('-date')
    
    return render(request, 'blog/all-posts.html',{
        "posts": sorted_posts
    })

def post_details(request, slug):
    
    post_detail = Post.objects.get(slug=slug)
    
    return render(request, 'blog/post-details.html', {'post_detail': post_detail,
                                                      'post_tags': post_detail.tags.all()})