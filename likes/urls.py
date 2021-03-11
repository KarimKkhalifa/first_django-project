from django.urls import path, include
from likes.views import AddLikeView, RemoveLike

app_name = 'likes'


urlpatterns = [
    path('likes/', include([
        path('add/', AddLikeView.as_view(), name='add'),
        path('remove/', RemoveLike.as_view(), name='remove'),

    ])),
]
