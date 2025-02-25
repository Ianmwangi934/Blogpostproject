from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login_view", views.login_view, name="login_view"),
    path("signup", views.signup, name="signup"),
    path("logout_view", views.logout_view, name="logout_view"),
    path("profile_view/<str:username>/", views.profile_view, name="profile_view"),
    path("create_blog_post", views.create_blog_post, name="create_blog_post"),
    path("update_blog_post/<int:post_id>/", views.update_blog_post, name="update_blog_post"),
    path("delete_post/<int:post_id>/", views.delete_post, name="delete_post"),
    path("post/<int:post_id>/comment/", views.Comment_Section,name="Comment_Section")
    
]