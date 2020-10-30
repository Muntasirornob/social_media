from django.shortcuts import render,HttpResponseRedirect,redirect,get_object_or_404
from profiles.models import Profile
from profiles.models import Relationship
from django.db.models import Q
from profiles.forms import ProfileModelForm
from django.views.generic import ListView,DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@login_required
def my_profile_view(request):
	profile=Profile.objects.get(user=request.user)
	form=ProfileModelForm(request.POST or None,request.FILES or None, instance=profile)
	confirm=False
	if request.method=='POST':
		if form.is_valid():
			form.save()
			confirm=True

	context={
		'profile':profile,
		'form':form,
		'confirm':confirm,

	}
	return render(request,'profiles/mprofile.html',context)
@login_required
def invites_received_view(request):	
	profile=Profile.objects.get(user=request.user)
	qs=Relationship.objects.invatations_received(profile)
	result=list(map(lambda x:x.sender,qs ))
	context={'qs':result,}
	is_empty=False
	if len(result)==0:
		is_empty= True
	context={'qs':result, 'is_empty':is_empty,}
	return render(request,'profiles/my_invites.html',context)
@login_required
def invite_accept(request):
	if request.method=='POST':
		pk=request.POST.get('profile_pk')
		user=request.user
		sender=Profile.objects.get(pk=pk)
		receiver=Profile.objects.get(user=user)
		rl=get_object_or_404(Relationship,sender=sender,receiver=receiver)
		if rl.status=="send":
			rl.status="accept"
			rl.save()
		return redirect('profiles:my-invites-view')
@login_required
def invite_reject(request):
	if request.method=='POST':
		pk=request.POST.get('profile_pk')
		user=request.user
		sender=Profile.objects.get(pk=pk)
		receiver=Profile.objects.get(user=user)
		rl=get_object_or_404(Relationship,sender=sender,receiver=receiver)
		rl.delete()
		return redirect('profiles:my-invites-view')

	

@login_required
def inv_profile_list_view(request):
	user=request.user
	qs=Profile.objects.get_all_profiles_to_invite(user)
	context={'qs':qs}

	return render(request,'profiles/invite_availabe_list.html',context)
#	def profile_list_view(request):
#		user=request.user
#		qs=Profile.objects.get_all_profiles(user)
#		context={'qs':qs}

#		return render(request,'profiles/profile_list.html',context)

class ProfileDetailView(LoginRequiredMixin,DetailView):
	model=Profile
	template_name='profiles/profile_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user=User.objects.get(username__iexact=self.request.user)
		profile=Profile.objects.get(user=user)
		rel_r=Relationship.objects.filter(sender=profile)
		rel_s=Relationship.objects.filter(receiver=profile)
		rel_receiver=[]
		rel_sender=[]
		for item in rel_r:
			rel_receiver.append(item.receiver.user)
			#print(rel_receiver)
		for item in rel_s:
			rel_sender.append(item.sender.user)
			#print(rel_sender)
		context['rel_receiver']=rel_receiver
		context['rel_sender']=rel_sender
		context['posts']=self.get_object().get_all_author_posts()
		context['len_posts'] = True if len(self.get_object().get_all_author_posts()) > 0 else False
		return context
class ProfileListView(LoginRequiredMixin,ListView):
	model=Profile
	template_name='profiles/profile_list.html'
	context_object_name='qs'
	def get_queryset(self):
		qs=Profile.objects.get_all_profiles(self.request.user)
		return qs
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user=User.objects.get(username__iexact=self.request.user)
		profile=Profile.objects.get(user=user)
		rel_r=Relationship.objects.filter(sender=profile)
		rel_s=Relationship.objects.filter(receiver=profile)
		rel_receiver=[]
		rel_sender=[]
		for item in rel_r:
			rel_receiver.append(item.receiver.user)
			#print(rel_receiver)
		for item in rel_s:
			rel_sender.append(item.sender.user)
			#print(rel_sender)

		context['rel_receiver']=rel_receiver
		context['rel_sender']=rel_sender
		context['is_empty']=False
		if len(self.get_queryset())==0:
			context['is_empty']=True
		return context
        
@login_required
def send_invatation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')
    
@login_required
def remove_from_friends(request):
	if request.method=='POST':
		pk = request.POST.get('profile_pk')
		user = request.user
		sender = Profile.objects.get(user=user)
		receiver = Profile.objects.get(pk=pk)

		rel = Relationship.objects.get(
			(Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
		)
		print(rel)
		rel.delete()
		return redirect(request.META.get('HTTP_REFERER'))
	return redirect('profiles:my-profile-view')
