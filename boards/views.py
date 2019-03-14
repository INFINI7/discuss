from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Board, Topic, Post
from .forms import NewTopicForm, ReplyTopicForm


def board_list(request):
    boards = Board.objects.all()
    return render(request, 'boards/boards.html', {'boards': boards})


def board_topics(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
    return render(request, 'boards/topics.html', {'board': board, 'topics': topics})


@ login_required
def new_topic(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    user = request.user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            Post.objects.create(message=form.cleaned_data.get('message'), topic=topic, created_by=user)
            return redirect('board_topics', board_pk=board_pk)
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})


def topic_posts(request, board_pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'boards/posts.html', {'topic': topic})


@ login_required
def reply_topic(request, board_pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)
    if request.method == 'POST':
        form = ReplyTopicForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', board_pk=board_pk, topic_pk=topic_pk)
    else:
        form = ReplyTopicForm()
    return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': form})
