
from django.urls import path, include

# from django documentation -- check CoreyMS' django tutorial Part 8 / 22:30
from .views import (
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    BlogHomeView,
    CategoryView,   # this is a function-based view
    CategoryCreateView,
    )
# alternatively, you can just use "from . import views".
# however, importing views one-by-one seems to be a better option so you can remember which views you have already worked on.


urlpatterns = [
    path('', BlogHomeView.as_view(), name="blogs"),             # homepage for blog app
    path('new/', PostCreateView.as_view(), name='post-new'),
    path('<str:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<str:slug>delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<str:slug>/', PostDetailView.as_view(), name='post-detail'),
    # path('<str:username>/', UserPostFilter.as_view(), name='user-posts'),     # filters applied to posts
    path('add-category/', CategoryCreateView.as_view(), name='add-category'),
    path('category/<str:cats>/', CategoryView, name='category'),
    ] 

    # replaced <int:pk> with <str:slug>


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)