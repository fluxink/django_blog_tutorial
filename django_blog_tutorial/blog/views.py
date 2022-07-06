from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post, PostRating
import json



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostRateView(LoginRequiredMixin, SingleObjectMixin, View):
    model = PostRating

    def get_object(self, queryset):
        post_rating_obj = super().get_object(queryset)
        return 
        



class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html as default
    context_object_name = 'posts' # <model>_list as default
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context.update({
            'posts_rating_list': PostRating.objects.all()
        })
        return context


@login_required
def post_rate(request):
    if request.method == 'POST':
        user = request.user
        json_data = json.loads(request.body)
        action = json_data['action']
        post = json_data['post_id']
        post = Post.objects.get(pk=post)
        if PostRating.objects.filter(user=user, post=post).exists():
            PostRating.objects.filter(user=user, post=post).update(action=action)
        else:
            PostRating.objects.create(user=user, post=post, action=action)
        print('Yay')
        return HttpResponse(request, {'content': 'Yay'})
    else:
        print('Foo')
        return HttpResponse(request, {'content': 'Foo'})


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html as default
    context_object_name = 'posts' # <model>_list as default
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    success_message = "Post was published"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    success_message = 'Post was updated'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Post

    success_message = 'Post was deleted successfully'

    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
