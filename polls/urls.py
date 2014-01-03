from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
	# ex: /polls/
	url(r'^$', views.IndexView.as_view(), name='index'),
	
	# ex: /polls/5/
	# the 'name' value as called by the {% url %} template tag
	# The DetailView generic view expects the primary key value captured 
	# from the URL to be called "pk", so we have changed poll_id to pk for the generic views.
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	
	# ex: /polls/5/results/
	url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
	
	# ex: /polls/5/vote/
	url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)