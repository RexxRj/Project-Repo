from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

class Tag(models.Model):
    caption = models.CharField(max_length=20)
    
    def __str__(self):
        return self.caption
    
class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.full_name()
    
class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=200)
    image_name = models.CharField(max_length=100)
    date = models.DateField()
    slug = models.SlugField(blank=False, null=False, unique=True, db_index=True)
    content = models.TextField(validators=[MinValueValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField(Tag)
    
    def get_absolute_url(self):
        return reverse("post-details-page", args=[self.slug])
    
    def __str__(self):
        return f"{self.title} - {self.date}"




        
    
    
