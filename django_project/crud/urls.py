from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "crud"
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/update/", views.update, name="update"),
    path("user_page/", views.user_page, name="user_page"),
    path("<int:pk>/like/", views.like, name="like"),
    path("user_profile/", views.user_profile, name="user_profile"),
    path("<int:pk>/like_delete/", views.like_delete, name="like_delete"),
    path("new_feature_one/", views.new_feature_one, name="new_feature_one"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
