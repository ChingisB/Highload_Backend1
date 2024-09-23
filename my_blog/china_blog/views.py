from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm

# Create your views here.

def basic_view(request):
    return HttpResponse("Hello, blog!")


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

@login_required
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'china_blog/post_detail.html', {"post": post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'china_blog/post_form.html', {'form': form})

@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'china_blog/post_form.html', {'form': form, 'post': post})

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'china_blog/post_confirm_delete.html', {'post': post})