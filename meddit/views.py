from django.shortcuts import render, get_object_or_404
from .models import Post, UrlEntry
from .forms import PostForm, UrlForm, UpdateProfile, RegisterForm
from .decorators import user_owns_url_or_admin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required #, permission_required
from django.contrib.auth.models import User



@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('meddit.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'meddit/post_edit.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'meddit/post_detail.html', {'post': post})

def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('published_date')

    return render(request, 'meddit/post_list.html', {'posts': posts})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'meddit/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('meddit.views.post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('meddit.views.post_list')

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('meddit.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'meddit/post_edit.html', {'form': form})

###########################################################################################
###                                  USER views                                         ###
###########################################################################################

@login_required
def update_profile(request):
    args = {}
    user = get_object_or_404(User, username=request.user)
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        # form.actual_user = request.user
        if form.is_valid():
            form.save()
            return redirect('meddit.views.update_successful')
    else:
        form = UpdateProfile(instance = user)

    args['form'] = form
    return render(request, 'registration/edit_profile.html', args)

def update_successful(request):
    return render(request, 'registration/update_successful.html', {})

def view_profile(request, pk=None):
    if pk:
        user = get_object_or_404(User, pk=pk)
    else:
        user = request.user
    return render(request, 'registration/profile.html', {'user': user})


# def registerUser(request):
#     print "hello"
#     # context = RequestContext(request)
#     registered = False
#     if request.method == 'POST':
#         newUser = RegisterUser(request.POST)
#         if newUser.is_valid():
#             user.set_password(newUser.password)
#             user.save()
#             registered = True
#         #raise something here, form is not valid
#     else:
#         newUser = RegisterUser(instance = None)
#     render('registration/register.html', {'newUser' : newUser, 'registered' : registered}, context)

###########################################################################################
###                                  URL SHORTENER VIEWS                                ###
###########################################################################################


@login_required
def show_urls(request):
    if request.user.is_superuser:
        urls = UrlEntry.objects.filter().order_by('created_date')
    else:
        urls = UrlEntry.objects.filter(author = request.user).order_by('created_date')
    return render(request, 'meddit/url_list.html', {'urls': urls})

@login_required
def add_url(request):
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            url.author = request.user
            url.save()
            return redirect('meddit.views.url_redirect', ext=url.extension)
    else:
        form = UrlForm()
    return render(request, 'meddit/add_url.html', {'form': form})


@user_owns_url_or_admin
@login_required
def url_edit(request, ext):
    url = get_object_or_404(UrlEntry, extension=ext)
    if request.method == "POST":
        form = UrlForm(request.POST, instance=url)
        if form.is_valid():
            url = form.save(commit=False)
            url.author = request.user
            url.save()
            return redirect('meddit.views.url_redirect', ext=url.extension)
    else:
        form = UrlForm(instance=url)
    return render(request, 'meddit/url_edit.html', {'form': form})



def url_redirect(request, ext): 
    url = get_object_or_404(UrlEntry, extension=ext)
    # url = UrlEntry.objects.get(extension=ext)
    return redirect(to=url.address)

@user_owns_url_or_admin
@login_required
def url_remove(request, ext):
    url = get_object_or_404(UrlEntry, extension=ext)
    url.delete()
    return redirect('meddit.views.show_urls')