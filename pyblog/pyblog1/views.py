from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.shortcuts import redirect
from django.views.generic.dates import DateDetailView
from el_pagination.views import AjaxListView

from .forms import CommentForm, UserCommentForm
from .models import Comment, Post



import os
def index(request):

	return render(request, "index.html")
def SignUp(request):
	u=User()
	u.email=request.GET.get("email")
	u.pwd=request.GET.get("pwd")
	u.name=request.GET.get("name")
	u.gender=request.GET.get("gender")
	u.save()

	return HttpResponse("sign Up successfull")

def Login(request):
	User=User.objects.filtr(email=request.GET.get("email"),pwd=request.GET.get("pwd"))
	if user.exists()==True:
		request.session["email"]=request.GET.get("email")
		res=redirect("LatestEntriesFeed")
		return res
	else:
		return HttpResponse("Invalid id or password")


class LatestEntriesFeed(Feed):
    title = "%s blog entries" % (Site.objects.get_current())
    description = "The latest blog entries"
    link = "/siteposts/"

    def items(self):
        return Post.objects.order_by('-post_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.bodytext


class BlogListView(AjaxListView):
    context_object_name = "posts"
    queryset = Post.objects.all().select_related()


class BlogDetailView(DateDetailView):
    model = Post
    date_field = 'post_date'
    month_format = '%m'
    page_template = "simpleblog/post_detail_page.html"

    def get_queryset(self):
        queryset = super(BlogDetailView, self).get_queryset()
        return queryset.select_related()

    def post(self, request, *args, **kwargs):
        self.object = post = self.get_object()
        if request.user.is_authenticated():
            form = UserCommentForm(request.POST)
        else:
            form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated():
                comment.user = request.user
                comment.user_name = request.user
                comment.user_email = request.user.email
            comment.ip = '0.0.0.0'
            comment.save()
            return redirect(post.get_absolute_url())
        context = self.get_context_data(object=post)
        context['comment_form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated():
            form = UserCommentForm()
        else:
            form = CommentForm()
        context = {
            'page_template': self.page_template,
            'comment_form': form,
            'comments': Comment.objects.filter(post=self.object.id).select_related()
        }
        return super(BlogDetailView, self).get_context_data(**context)

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template depending if the request is ajax
        or not and it renders with the given context.
        """
        if self.request.is_ajax():
            template = self.page_template
        else:
            template = self.get_template_names()
        return self.response_class(
            request=self.request,
            template=template,
            context=context,
            **response_kwargs
        )
