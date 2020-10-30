from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from posts.models import Post,Like
from profiles.models import Profile
from posts.forms import PostModelForm,CommentModelForm
from django.views.generic import UpdateView,DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
@login_required
def list_post(request):
	qs=Post.objects.all()
	profile=Profile.objects.get(user=request.user)
	post_form=PostModelForm()
	comment_form=CommentModelForm()
	profile=Profile.objects.get(user=request.user)
	post_added=False
	if "submit_p_form" in request.POST:
		post_form=PostModelForm(request.POST,request.FILES)

		if post_form.is_valid():
			instance=post_form.save(commit=False)
			instance.author=profile
			instance.save()
			post_form=PostModelForm()
			post_added=True
	if "submit_c_form" in request.POST:
		comment_form=CommentModelForm(request.POST)

		if comment_form.is_valid():
			instance=comment_form.save(commit=False)
			instance.user=profile
			instance.post=Post.objects.get(id=request.POST.get('post_id'))
			instance.save()
			comment_form=CommentModelForm()
			post_added=True

	context={
		'qs':qs,
		'profile':profile,
		'post_form':post_form,
		'comment_form':comment_form,
		'post_added':post_added,
	}
	return render(request,'posts/main.html',context)




@login_required
def like_unlike(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value=='Like':
                like.delete()
            else:
            	like.delete()
                
        else:
            like.value='Like'

            post_obj.save()
            like.save()
    return redirect('posts:my-post-view')

class PostDeleteView(LoginRequiredMixin,DeleteView):
	model=Post
	template_name='posts/confirm_del.html'
	success_url=reverse_lazy('posts:my-post-view')


class PostUpdateView(LoginRequiredMixin,UpdateView):
	form_class=PostModelForm
	model=Post
	template_name='posts/update.html'
	success_url=reverse_lazy('posts:my-post-view')

	def form_valid(self, form):
		profile = Profile.objects.get(user=self.request.user)
		if form.instance.author == profile:
			return super().form_valid(form)
		else:
			form.add_error(None, "You need to be the author of the post in order to update it")
			return super().form_invalid(form)
