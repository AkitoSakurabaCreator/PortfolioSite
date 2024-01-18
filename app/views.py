from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Post, CreateItem, Category, Tag
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser, Certification, Skill, Reward
from django.db.models import Q
from django.core.paginator import Paginator
import datetime

class PortfolioView(View):
    def get(self, request, *args, **kwargs):
        item_data = CreateItem.objects.all().order_by("orderby")
        category_data = Category.objects.all()
        tag_data = Tag.objects.all()

        paginator = Paginator(item_data, 16)
        p = request.GET.get('p')
        item_data = paginator.get_page(p)

        context = {
            "item_data": item_data,
            "category_data": category_data,
            "tag_data": tag_data,
        }
        
        return render(request, 'app/portfolio/index.html', context)

    def post(self, request, *args, **kwargs):
        search = request.POST["search"]
        category = request.POST.getlist("categories")
        checkBox = request.POST.getlist("tags")

        if not search:
            search = ''
        if not category:
            category = ''
        if not checkBox:
            checkBox = ''
            
        if not "All" in category or not "All" in checkBox:
            if len(search) == 0:
                print ("None1")
                item_data = CreateItem.objects.all().filter(
                    Q(categories__category__in=category) | Q(tags__tag__in=checkBox)
                ).order_by("orderby").distinct()
            else:
                print ("else1")
                item_data = CreateItem.objects.all().filter(
                    Q(title__icontains=search) | Q(description__icontains=search) |
                    Q(categories__category__in=category) | Q(tags__tag__in=checkBox)
                ).order_by("orderby").distinct()
        else:
            if len(search) == 0:
                print ("None2")
                item_data = CreateItem.objects.all().order_by("orderby")
            else:
                print ("else2")
                item_data = CreateItem.objects.all().filter(
                    Q(title__icontains=search) | Q(description__icontains=search)
                ).order_by("orderby").distinct()

        category_data = Category.objects.all()
        tag_data = Tag.objects.all()

        paginator = Paginator(item_data, 15)
        p = request.GET.get('p')
        item_data = paginator.get_page(p)

        context = {
            "item_data": item_data,
            "category_data": category_data,
            "tag_data": tag_data,
        }
        return render(request, 'app/portfolio/index.html', context)


class PortfolioDetailView(View):
    def get(self, request, *args, **kwargs):
        slug=self.kwargs['slug']
        item_data = CreateItem.objects.get(slug=slug)
        category_data = Category.objects.all()
        tag_data = Tag.objects.all()
        
        return render(request, "app/portfolio/product.html",
            {
                "item_data": item_data,
                "category_data": category_data,
                "tag_data": tag_data
            })

class PortfolioSearch(View):
    def get(self, request, *args, **kwargs):
        search = self.kwargs["slug"]
        p = request.GET.get('p')
        
        item_data = CreateItem.objects.all().filter(
            Q(categories__category=search) | Q(tags__tag=search)
        ).distinct()
        print (search)
        paginator = Paginator(item_data, 15)
        item_data = paginator.get_page(p)

        category_data = Category.objects.all()
        tag_data = Tag.objects.all()

        context = {
            "item_data": item_data,
            "category_data": category_data,
            "tag_data": tag_data,
        }
        return render(request, 'app/portfolio/index.html', context)


class Profile(View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=1)
        cert_data = Certification.objects.all().order_by('orderby')
        skill_data = Skill.objects.all().order_by('orderby')
        reward_data = Reward.objects.all().order_by('orderby')
        
        birthday = CustomUser.objects.get(id=1).year
        today = datetime.date.today()
        date = ((int(today.strftime("%Y%m%d")) - int(birthday.strftime("%Y%m%d"))) // 10000)
        context = {
            'user_data': user_data,
            'cert_data': cert_data,
            'skill_data': skill_data,
            'reward_data': reward_data,
            "birthday": date,
            }
        return render(request, "app/portfolio/profile.html", context)


class BlogView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        return render(request, 'app/blog/blog.html', {
            'post_data': post_data
        })

class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/blog/post_detail.html', {
            'post_data': post_data
        })

class CreatePostView(View):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        return render(request, 'app/blog/post_form.html', {
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('post_detail', post_data.id)

        return render(request, 'app/blog/post_form.html', {
            'form': form
        })

class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            initial = {
                'title': post_data.title,
                'content': post_data.content
            }
        )

        return render(request, 'app/blog/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])

        return render(request, 'app/blog/post_form.html', {
            'form' : form
        })

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/blog/post_delete.html', {
            'post_data' : post_data
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('Index')