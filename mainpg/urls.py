from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as mainpgviews

urlpatterns = [
    path('', mainpgviews.home, name = 'home'),
    path('ask/', mainpgviews.ask.as_view(), name = 'askQ'),
    path('like/question/<int:q_id>/',mainpgviews.like, name = 'like'),
    path('dislike/question/<int:q_id>/',mainpgviews.dislike, name = 'dislike'),
    path('accounts/', include('allauth.urls')),
    path('view/Question/<int:pk>/', mainpgviews.viewans, name='viewans'),
    path('answer/Question/<int:pk>/', mainpgviews.answer, name = 'answer'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)