from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from .models import Profile
from .models import BlogPost, Comment

class LoginForm(forms.Form):
    username = forms.CharField(label="username", widget= forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    email = forms.CharField(label="email", widget=forms.TextInput(attrs={'placeholder': 'Enter your Email'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

class NewUserForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput(attrs={'placeholder': 'Enter your Username'}))
    email = forms.CharField(label="email", widget=forms.TextInput(attrs={'placeholder': 'Enter your email'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

class ProfileForm(forms.Form):
    first_name = forms.CharField(label="first_name",widget=forms.TextInput(attrs={'placeholder':'Your First name'}))
    last_name = forms.CharField(label="last_name", widget=forms.TextInput(attrs={'placeholder':'Your last name'}))
    bio = forms.CharField(label="bio",widget=forms.Textarea(attrs={'placeholder':'Dont be shy, say something about yourself......','rol':25,'cols':55}))
    location = forms.CharField(label="location", widget=forms.TextInput(attrs={'placeholder':'Your location'}))
    birth_date = forms.DateField(label="birth_date", widget=forms.TextInput(attrs={'placeholder':'Birthdate'}))
    photo = forms.ImageField(label="photo", required=False)
    background_photo = forms.ImageField(label="background_photo",required=False)

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['content', 'image', 'video'] #Fields to display 
        widgets = {
            'content':forms.Textarea(attrs={'placeholder': 'Write your post here .......','rol':35, 'cols':55}),
            
        }

    # Add a validation to ensure either text, image, or video is provided
    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')

        if not content and not image and not video:
            raise forms.ValidationError("Please provide either content,an image, or video")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment'] # Fields to display
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Comment here ..', 'rows': 3}),
        }

        #Adding a validation to ensure the text field of the form is provided
    def clean(self):
        cleaned_data = super().clean()
        comment = cleaned_data.get('comment')

        if not comment:
            raise forms.ValidationError("You must write a comment.")
        return cleaned_data






# Create your views here.
@login_required()
def create_blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)# handling both text and files uploads
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user #set the user who created the post
            blog_post.save()
            return HttpResponseRedirect(reverse("home"))
    else:
        form = BlogPostForm()
    return render(request, 'post/create_blog_post.html',{
        "form": form
    })

@login_required()
def Comment_Section(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user # setting the user who made the comment
            comment.post = post # linking the comment to the blogpost
            comment.save()
            return HttpResponseRedirect(reverse("home"))
    else:
        form = CommentForm()
    return render(request, "post/comment_section.html",{
    
       "post":post,
       "form":form,
       
    })
@login_required()
def update_blog_post(request, post_id):
    post = get_object_or_404(BlogPost,id=post_id, user=request.user)#Ensures the user owns the post
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("home"))# redirecting the user to the homepage where blogpost are displayed
    else:
        form = BlogPostForm(instance=post)#Prepulate the form with the post's data
    return render(request, "post/update_blog_post.html",{
        "form":form,
        "post":post
    })
@login_required()
def delete_post(request, post_id):
    #get the post and ensure the loged in user is the owner of the post
    post = get_object_or_404(BlogPost, id=post_id, user=request.user)
    
    #check if it's a post request which confirms the user's actions
    if request.method == "POST":
        post.delete()
        return HttpResponseRedirect(reverse("home"))

    return render(request, "post/confirm_delete.html",{
        "post":post
    })
@login_required()
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    
    # create user profile
    profile, create = Profile.objects.get_or_create(user=user)

    #Fetch all blog posts by this user
    posts = BlogPost.objects.filter(user=user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)# handling files for images and documents in request.FILES
        if form.is_valid():
            profile.first_name = form.cleaned_data["first_name"]
            profile.last_name = form.cleaned_data["last_name"]
            profile.bio = form.cleaned_data["bio"]
            profile.location = form.cleaned_data["location"]
            profile.birth_date= form.cleaned_data["birth_date"]
            
            if form.cleaned_data["photo"]:
                profile.photo = form.cleaned_data["photo"] 
            if form.cleaned_data["background_photo"]:
                profile.background_photo = form.cleaned_data["background_photo"]
            profile.save()


            # Redirect the user to the profile view page after saving the profile
            return HttpResponseRedirect(reverse ("profile_view", args=(user.username,)))
        else:
            # if the form is not valid, re render the form with the errors
            return render(request, "post/profileform.html",{
                "form":form
            })
    else:
        #user already has the profile data, show the profile details
        if not profile.first_name or not profile.last_name or not profile.bio or not profile.location or  not profile.birth_date:
            #user is new or hasn't filled in data. Re render the form
            form = ProfileForm()
            return render(request, "post/profileform.html",{
                "form":form
            })
        else:
            #user already has profile data, show profile data
            form = ProfileForm(initial={
                'first_name':profile.first_name,
                'last_name': profile.last_name,
                'bio':profile.bio,
                'location':profile.location,
                'birth_date':profile.birth_date,
                'photo':profile.photo,
                'background_photo':profile.background_photo

            })
            return render(request, "post/profile.html",{
                "profile":profile,
                "posts":posts
            })
def home(request):
    post = BlogPost.objects.all()
    comments = Comment.objects.all() #Fetching all the comments
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login_view"))
    return render(request,"post/post_list.html",{
        "post":post,
        "comments":comments
    })

def login_view(request):
    signup=NewUserForm()
    form = LoginForm()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            profile, create = Profile.objects.get_or_create(user=user)
            return render(request, "post/picture.html",{
                "profile":profile
            })
        else:
            return render(request, "post/signup.html",{
                "signup": signup
            })
    return render(request, "post/login.html",{
        "form":form
    })

# Signing in a New User

def signup(request):
    signup = NewUserForm(request.POST)
    if request.method == "POST":
        if signup.is_valid():
            username = signup.cleaned_data["username"]
            email = signup.cleaned_data["email"]
            password = signup.cleaned_data["password"]

            # create and save the user
            user = User.objects.create_user(username = username, email = email, password = password)

            # login the user
            login(request, user)
            return HttpResponseRedirect(reverse("profile_view", args=(user.username,)))

        else:
            return render(request, "post/signup.html",{
                "signup": signup
            })
    return render(request, "post/signup.html",{
        "signup":signup
    })

def logout_view(request):
    form = LoginForm()
    return render(request,"post/login.html",{
        "form":form,
        "message": "You are logedout"
    })








