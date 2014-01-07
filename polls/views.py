from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import loader
from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# pdf generation tool
from reportlab.pdfgen import canvas

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

def index(request):
    latest_poll= Poll.objects.order_by('-pub_date')
    paginator = Paginator(latest_poll, 10) # Show 25 latest_poll per page

    page = request.GET.get('page')
    try:
        latest_poll_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_poll_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_poll_list = paginator.page(paginator.num_pages)

    return render_to_response('polls/index.html', {"latest_poll_list": latest_poll_list})

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

# class IndexView(generic.ListView):
#     # By default, the ListView generic view uses a default template 
#     # called <app name>/<model name>_list.html
#     template_name = 'polls/index.html'
#     # for ListView, the automatically generated context variable is poll_list. 
#     # To override this we provide the context_object_name attribute
#     context_object_name = 'latest_poll_list'
#     def get_queryset(self):
#     	return Poll.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    # since we are using a Django model (Poll), 
    # Django is able to determine an appropriate name for the context variable
    model = Poll
    # By default, the DetailView generic view uses a template called 
    # <app name>/<model name>_detail.html. So we override this by
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())



class ResultsView(generic.DetailView):
    # since we are using a Django model (Poll), 
    # Django is able to determine an appropriate name for the context variable
    model = Poll
    template_name = 'polls/results.html'




# =====================================
# Using reportlab to generate PDF Files
# =====================================

def generatepdf(request, username):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'attachment: filename="username.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100,100, "Hello! {0}".format(username))

    # Close the PDF object cleanly, and we are done
    p.showPage()
    p.save()
    return response