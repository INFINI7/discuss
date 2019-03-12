from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.board_list, name='home'),

    path('boards/', include([
        path('<int:pk>/', views.board_topics, name='board_topics'),
        path('<int:pk>/new/', views.new_topic, name='new_topic'),
    ])),
]
