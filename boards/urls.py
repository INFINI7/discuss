from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.board_list, name='home'),

    path('boards/<int:board_pk>/', include([
        path('', views.board_topics, name='board_topics'),
        path('new/', views.new_topic, name='new_topic'),
        path('topics/<int:topic_pk>/', views.topic_posts, name='topic_posts'),
        path('topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    ])),
]
