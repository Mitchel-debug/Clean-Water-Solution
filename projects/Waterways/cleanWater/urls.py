from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("charge/", views.charge, name="charge"),
    path("success/<str:args>/", views.successMsg, name="successMsg"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("takeaction", views.takeaction, name="takeaction"),
    path("report", views.report, name="report"),
    path("articles", views.articles, name="articles"),
    path("about", views.about, name="about"),
    path("articles/<str:articles_id>", views.showArticles, name="articles"),
]

urlpatterns += staticfiles_urlpatterns()