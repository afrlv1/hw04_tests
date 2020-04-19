from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User, Post, Group
from .forms import PostForm

def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10) # показывать по 10 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number) # получить записи с нужным смещением
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:12]

    paginator = Paginator(posts, 10) # показывать по 10 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number) # получить записи с нужным смещением
    return render(request, 'group.html', {'group': group, 'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            author = request.user
            Post.objects.create(text=text, group=group, author=author)
            return redirect('index')
    form = PostForm()
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    # тут тело функции
    profile = get_object_or_404(User, username=username)
    posts_profile = Post.objects.filter(author=profile).order_by("-pub_date").all()
    posts_count = Post.objects.filter(author=profile).count()
    paginator = Paginator(posts_profile, 10) # показывать по 10 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number) # получить записи с нужным смещением
    return render(request, "profile.html", {'profile':profile,'posts_count': posts_count, 'paginator': paginator, 'page_num': page_number, 'page':page})

@login_required
def post_view(request, username, post_id):
    # тут тело функции
    profile = get_object_or_404(User, username=username)
    post_count = Post.objects.filter(author=profile).count()
    post = Post.objects.get(pk=post_id)
    return render(request, "post.html", {'profile':profile, 'posts_count': post_count, 'post':post,})

def post_edit(request, username, post_id):
    # тут тело функции. Не забудьте проверить,
    # что текущий пользователь — это автор записи.
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author = profile.pk)
    if request.method == "GET":
        if request.user.username != username:
            return redirect('post', username=post.author, post_id=post.pk)
        form = PostForm(instance=post)
        return render(request, 'new_post.html', {'form': form, 'post': post})
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if request.user.username == username:
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post', username=post.author, post_id=post.pk)
            return render(request, 'new_post.html', {'form': form, 'post': post})
        return redirect('post', username=post.author, post_id=post.pk)

