from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm


def board_list(request):
    boards = Board.objects.all()
    return render(request, 'boards/boards.html', {'boards': boards})


def board_topics(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 12)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
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
    topic = get_object_or_404(Topic, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', board_pk=board_pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': form})


@ login_required
def edit_post(request, board_pk, topic_pk, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.message = form.cleaned_data.get('message')
            post.updated_by = request.user
            post.updated_at = timezone.now()
            post.save()
            return redirect('topic_posts', board_pk=board_pk, topic_pk=topic_pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'boards/edit_post.html', {'post': post, 'form': form})
