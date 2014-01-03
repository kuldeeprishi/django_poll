from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views import generic

from polls.models import Poll, Choice

# ===============================
# Without Generic Views
# ==============================
# def index(request):
	# latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
	# template = loader.get_template('polls/index.html')
	# context = {
	# 	'latest_poll_list': latest_poll_list,
	# 	}
	# return render(request, 'polls/index.html', context)

# def detail(request, poll_id):
	# poll = get_object_or_404(Poll, pk = poll_id)
	# return render(request, 'polls/detail.html', {'poll':poll})

# def results(request, poll_id):
# 	poll = get_object_or_404(Poll, pk=poll_id)
# 	return render(request, 'polls/results.html', {'poll': poll})

def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
				'poll': p,
				'error_message': "you didn't select a choice."
			})
	else:
		selected_choice.votes+=1
		selected_choice.save()

		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

# ===================================
# With Generic Views
# ===================================

class IndexView(generic.ListView):
	# By default, the ListView generic view uses a default template 
	# called <app name>/<model name>_list.html
	template_name = 'polls/index.html'
	# for ListView, the automatically generated context variable is poll_list. 
	# To override this we provide the context_object_name attribute
	context_object_name = 'latest_poll_list'
	def get_queryset(self):
		return Poll.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	# since we are using a Django model (Poll), 
	# Django is able to determine an appropriate name for the context variable
	model = Poll
	# By default, the DetailView generic view uses a template called 
	# <app name>/<model name>_detail.html. So we override this by
	template_name = 'polls/detail.html' 



class ResultsView(generic.DetailView):
	# since we are using a Django model (Poll), 
	# Django is able to determine an appropriate name for the context variable
	model = Poll
	template_name = 'polls/results.html'

