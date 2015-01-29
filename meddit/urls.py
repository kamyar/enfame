from django.conf.urls import patterns, url #, include
from . import views
#from django.contrib.auth.views import password_change
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from .decorators import anonymous_required
# from .forms import RegisterForm

urlpatterns = patterns('',
	url(r'^$', views.show_urls, name='show_urls'),
	url(r'^add/$', views.add_url, name='add_url'),
    url(r'^url/(?P<ext>\w{0,100})/edit/$', views.url_edit, name='url_edit'),
    url(r'^url/(?P<ext>\w{0,100})/remove/$', views.url_remove, name='url_remove'),
    #add url show detail :D

	# url(r'^register/$', views.registerUser, name='register_view'),
	url(r'^profile/edit/$', views.update_profile, name='update_profile'),
	url(r'^profile/(?P<pk>[0-9]+|$)', views.view_profile, name='view_profile'),
	# url(r'^profile/edit/password$', password_change, name='password_change'),
	url(r'^profile/edit/password$', 
	        'django.contrib.auth.views.password_change', 
	        {'post_change_redirect' : '/profile/succ/'}, 
	        name="password_change"), 
	    (r'^profile/succ/$', 
	        views.update_successful),
    url(r'^r/(?P<ext>\w{0,100})$', views.url_redirect, name='url_redirect'),
	url('^register/', anonymous_required(
						 CreateView.as_view(template_name='registration/register.html', form_class=UserCreationForm,
	            success_url='/')), name='register_view'),



    url(r'^posts/$', views.post_list),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
	url(r'^post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
	url(r'^post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),



)