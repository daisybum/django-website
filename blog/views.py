from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


class Main(ListView):
    model = Post
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hello'] = 'hello'
        return context


class PostList(ListView):
    model = Post
    ordering = '-id'


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Post, id=id_)


class PostCreate(CreateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload']


class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload']

    template_name = 'blog/post_update_form.html'

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Post, id=id_)

    def dispatch(self, request, *args, **kwargs):
        return super(PostUpdate, self).dispatch(request, *args, **kwargs)


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


main = Main.as_view()
post_list = PostList.as_view()
post_detail = PostDetail.as_view()
post_create = PostCreate.as_view()
post_update = PostUpdate.as_view()
post_delete = PostDelete.as_view()
