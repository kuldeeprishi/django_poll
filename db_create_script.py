


def createdb():
	from django.utils import timezone
	from polls.models import Poll, Choice
	n = int(raw_input("Enter no. of items to create: "))
	for i in xrange(n):
		p = Poll(question="Question = {0}".format(i), pub_date = timezone.now())
		p.save()
		for i in xrange(4):
			cycle = ['a', 'b', 'c', 'd']
			c = Choice(poll = p, choice_text = cycle[i], votes = 0)
			c.save()

