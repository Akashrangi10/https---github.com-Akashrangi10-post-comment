from unicodedata import name
from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.contrib.auth import authenticate, login as login_ , logout 
from .forms import UserForm,CommentForm, MyProfileForm
from .models import AllUsers,Post,Comments,Like, MyProfileDetails
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# Main Index
def index_view(request):
    posts = Post.objects.values('id','name__username','post_desc','created',"post_img").order_by('-created')
    for post in posts:
        if "post_img" in post:
            post["post_img"] = "media/"+ post["post_img"] 
    comments = Comments.objects.values('id')
    likes=Like.objects.values('post_id','like')
    liked_number = {}
    disliked_number = {}
    for like in likes:
        if like["like"] is False:
            if like['post_id'] in disliked_number:
                disliked_number[like['post_id']] +=1
            else:
                disliked_number[like['post_id']] = 1
        else:
            
            if like["post_id"] in liked_number:
                liked_number[like["post_id"]] += 1  
                
            else:
                liked_number[like["post_id"]] = 1
   
    comment_count = (Comments.objects.values('post_id').annotate(comments=Count('body')))
    
    context = {
        'posts':posts,
        'comments':comments,
        'dislikes':disliked_number,
        'likes':liked_number,
        'comment_numbers':comment_count,
    }
    return render(request,'posts/Akash.html',context=context)




# registration 
def register_view(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('posts:login')
    return render (request,'posts/register.html',{'form':form})


# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username = username,password = password)

        if user:
            login_(request,user)
            return redirect('posts:index')
        else:
            return redirect('posts:login')
    return render (request,'posts/login.html')

def create_profile_view(request):
    form = MyProfileForm()
    if request.method == 'POST':
        form = MyProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    return render(request, 'posts/createprofile.html',{'form':form})

# Logout
def logout_view(request):
    logout(request)
    return redirect ('posts:index')

def post_add_view(request):
    if request.method == 'POST' and request.FILES["post_img"]:
        user = request.user
        post = request.POST['post_body']
        image = request.FILES["post_img"]
        Post.objects.create(name=user,post_desc = post, post_img= image)
        return redirect('posts:index')


# Comment on Post
@login_required(login_url='posts:login')
def comment_view(request,id):
    comments = Comments.objects.filter(post=id).values('name__username','id','body','droped_on')
    form = CommentForm()
    user = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.name = request.user
            user.post_id = id
            user.save()
            return redirect('posts:index')
    return render(request,'posts/comments.html',{
        'form':form,
        'comments':comments,

        })


def like_view(request,post_ids):
    if Like.objects.filter(user = request.user,post_id=post_ids).exists():
        return redirect('posts:index')
    else:
        Like.objects.create(user=request.user,post_id=post_ids,like=True)
        return redirect('posts:index')

@login_required(login_url='posts:login')
def dislike_view(request,posts_id):
    if Like.objects.filter(user=request.user,post_id = posts_id).exists():
        return redirect('posts:index')
    else:
        Like.objects.create(user = request.user,post_id=posts_id,like=False)
        return redirect('posts:index')

    
        