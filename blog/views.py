from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment
from .forms import CommentForm
from django.db.models import Q

class Main(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hello'] = 'hello'
        return context


class PostList(ListView):
    model = Post
    ordering = '-created_at'


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("id")
        obj = get_object_or_404(Post, id=id_)
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['comment_form'] = CommentForm()
        return context


class PostCreate(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload']

    def form_valid(self, form):
        currnet_user = self.request.user
        if currnet_user.is_authenticated:
            form.instance.author = currnet_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('login')


class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload']

    template_name = 'blog/post_update_form.html'

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Post, id=id_)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError('You are not allowed to update this post')


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/post_delete.html'

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Post, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Post'
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError('You are not allowed to update this post')


class PostSearch(PostList):
    ordering = '-created_at'
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs.get('q')
        post_list = Post.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        ).distinct().order_by('-created_at')
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs.get('q')
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context


def comment_create(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
            else:
                return redirect(post.get_absolute_url())
        else:
            raise PermissionDenied

main = Main.as_view()
post_list = PostList.as_view()
post_detail = PostDetail.as_view()
post_create = PostCreate.as_view()
post_update = PostUpdate.as_view()
post_delete = PostDelete.as_view()
post_search = PostSearch.as_view()