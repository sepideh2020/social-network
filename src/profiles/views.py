from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import CustomUser, Relationship
from .forms import ProfileModelForm ,LoginForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import  login
from django.db.models import Q
from django.contrib.auth import views as auth_views
from .forms import SignUpForm
from .tokens import account_activation_token, check_otp_expiration, get_random_otp, send_otp


# class RegisterUser(CreateView):
# form_class = SignUpForm
# success_url = '/posts:main-post-view/'
# template_name = 'main/signup.html'
#
# def get(self, request, **kwargs):
#     form = SignUpForm()
#     return render(request, 'main/signup.html', {'form': form})
#
# def post(self, request, **kwargs):
#     form = SignUpForm(request.POST)
#     if form.is_valid():
#         form.save()
#         username = form.cleaned_data.get('username')
#         email = form.cleaned_data.get('email')
#         phone = form.cleaned_data.get('phone')
#         raw_password = form.cleaned_data.get('password1')
#
#         user = authenticate(username=username, email=email, phone=phone, password=raw_password)
#         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#         return redirect('posts:main-post-view')
#     return render(request, 'main/signup.html', {'form': form})
def SignupEmail(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('main/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})


def SignupPhone(request):
    form = SignUpForm()
    if request.method == "POST":
        try:
            if "phone" in request.POST:
                phone = request.POST.get('phone')
                user = CustomUser.objects.get(phone=phone)
                # send otp
                otp = get_random_otp()
                # send_otp(phone, otp)
                # save otp
                print(otp)
                user.otp = otp
                user.save()
                request.session['user_phone'] = user.phone
                return HttpResponseRedirect(reverse('verify'))

        except CustomUser.DoesNotExist:
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # send otp
                otp = get_random_otp()
                # send_otp(phone, otp)
                # send_otp_soap(mobile, otp)
                # save otp
                print(otp)
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_phone'] = user.phone
                return HttpResponseRedirect(reverse('verify'))
    return render(request, 'main/signup.html', {'form': form})

def verify(request):
    try:
        phone = request.session.get('user_phone')
        user = CustomUser.objects.get(phone=phone)

        if request.method == "POST":

            # check otp expiration
            if not check_otp_expiration(user.phone):
                # messages.error(request, "OTP is expired, please try again.")
                return HttpResponseRedirect(reverse('signup-phone'))

            if user.otp != int(request.POST.get('otp')):
                # messages.error(request, "OTP is incorrect.")
                return HttpResponseRedirect(reverse('verify'))

            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home-view'))

        return render(request, 'main/verify.html', {'phone': phone})

    except CustomUser.DoesNotExist:
        # messages.error(request, "Error accorded, try again.")
        return HttpResponseRedirect(reverse('signup-phone'))




def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home-view')
    else:
        return render(request, 'main/acc_active_email.html')


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'main/login.html'


@login_required
def my_profile_view(request):
    profile = CustomUser.objects.get(id__exact=request.user.id)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    posts = profile.get_all_authors_posts()
    len_posts = True if len(profile.get_all_authors_posts()) > 0 else False
    # instance shows us which profile we want to update
    confirm = False

    if request.method == 'POST':
        if form.is_valid:
            form.save()
            confirm = True  # for update

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
        'posts': posts,
        'len_posts': len_posts
    }

    return render(request, 'profiles/myprofile.html', context)


@login_required
def invited_received_view(request):
    """gets all the invitations for a particular profile"""
    profile = CustomUser.objects.get(id__exact=request.user.id)
    qs = Relationship.objects.invitation_received(profile)
    results = list(map(lambda x: x.sender, qs))
    if len(results) == 0:
        is_empty = True
    else:
        is_empty = False
    context = {
        'qs': results,
        'is_empty': is_empty,
    }
    return render(request, 'profiles/my_invites.html', context)


class invite_profiles_list_view(LoginRequiredMixin, ListView):
    """profiles list available to invite"""
    model = CustomUser
    template_name = 'profiles/to_invite_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        user = self.request.user
        qs = CustomUser.objects.get_all_profiles_to_invite(user)
        return qs

    def get_context_data(self, **kwargs):
        """this function allows us to some additional context to the template"""
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(username__iexact=self.request.user.username)  # it gets user the user
        profile = CustomUser.objects.get(id__exact=user.id)
        rel_r = Relationship.objects.filter(sender=profile)
        # relationships where we invited other users
        rel_s = Relationship.objects.filter(receiver=profile)
        # relationships where we are receiver of the invitation
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.username)
        for item in rel_s:
            rel_sender.append(item.sender.username)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            # if we will be the only profile 'is_empty' will be equall to True
            context['is_empty'] = True
        return context


@login_required
def accept_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = CustomUser.objects.get(pk=pk)
        receiver = CustomUser.objects.get(id__exact=request.user.id)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')


@login_required
def reject_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        receiver = CustomUser.objects.get(id__exact=request.user.id)
        sender = CustomUser.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')


@login_required
def profiles_list_view(request):
    """get all profiles by method view"""
    user = request.user
    qs = CustomUser.objects.get_all_profiles(user)
    context = {'qs': qs}
    return render(request, 'profiles/profile_list.html', context)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profiles/detail.html'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = CustomUser.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(username__iexact=self.request.user.username)
        profile = CustomUser.objects.get(id__exact=user.id)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.username)
        for item in rel_s:
            rel_sender.append(item.sender.username)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context


class ProfileListView(LoginRequiredMixin, ListView):
    """get all profiles by list view"""
    model = CustomUser
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):  # get all profile without own
        qs = CustomUser.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        """this function allows us to some additional context to the template"""

        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(username__iexact=self.request.user.username)  # it gets user the user
        profile = CustomUser.objects.get(id__exact=user.id)
        rel_r = Relationship.objects.filter(sender=profile)
        # relationships where we invited other users
        rel_s = Relationship.objects.filter(receiver=profile)
        # relationships where we are receiver of the invitation
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.username)
        for item in rel_s:
            rel_sender.append(item.sender.username)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            # if we will be the only profile 'is_empty' will be equall to True
            context['is_empty'] = True
        return context


@login_required
def send_invitation(request):
    """here we are the sender of invitation and we should choose the receiver,and the receiver is
    our profile pk,based on the profile pk which we get from profiles list,we get the receiver"""

    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = CustomUser.objects.get(id__exact=user.id)
        receiver = CustomUser.objects.get(pk=pk)  # primary key

        #  creating relationship
        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))  # in order to stay on the same page
    return redirect('profiles:my-profile-view')  # if access to this url directly


@login_required
def remove_from_friends(request):
    """here we dont know who is the sender and who is the receiver of the request,we have to delete
     the relationship after getting it we have to remove the person who we dont want to fried with from
      our friend list and also remove ourself from that person friend list"""

    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = CustomUser.objects.get(id__exact=user.id)  # sender is us
        receiver = CustomUser.objects.get(pk=pk)  # profile we want to remove from friends

        # there is two senario here whether first we requested and we want to remove that guz from
        # out friends list or first that guz requested us and now we want to remove him from our friends list
        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )

        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))  # ??  # in order to stay on the same page
    return redirect('profiles:my-profile-view')  # if we are not dealing with post request
    # in order to get rid of user from friends list we use signals,'pre_delete signals function'


def autocomplete(request):
    if 'term' in request.GET:
        qs = CustomUser.objects.filter(username__icontains=request.GET.get('term'))
        titles = list()
        for person in qs:
            titles.append(person.username)
        return JsonResponse(titles, safe=False)
    return render(request, 'profiles/search.html')
