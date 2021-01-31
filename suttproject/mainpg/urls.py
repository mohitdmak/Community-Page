from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as mainpgviews

urlpatterns = [
    path('', mainpgviews.home, name = 'home'),
    path('ask/', mainpgviews.ask.as_view(), name = 'askQ'),
    path('like/question/<int:q_id>/',mainpgviews.like, name = 'like'),
    path('dislike/question/<int:pk>/',mainpgviews.dislike, name = 'dislike'),
    path('accounts/', include('allauth.urls')),
 #   path('login/',mainpgviews.login, name = 'login'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)