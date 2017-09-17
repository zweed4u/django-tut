from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Question
from django.urls import reverse

# Create your views here.
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#output = ', '.join([q.question_text for q in latest_question_list])
	#template = loader.get_template('polls/index.html')
	context = {
		'latest_question_list': latest_question_list,
	}
	#return HttpResponse("Hello World. You're at the polls index\n{0}".format(template.render(context, request)))
	return render(request, 'polls/index.html', context)

def detail(request, question_id):
	'''
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	return HttpResponse("You're looking at question {0}".format(question_id))
	'''
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
	response = "You're looking at the results of question {0}".format(question_id)
	return HttpResponse(response)

def vote(request, question_id):
	#return HttpResponse("You're voting on question {0}".format(question_id))
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Display the question vote form
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': 'You didn\'t select a choice.',
		})
	else:
		selected_choice.votes +=1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully
		# dealing with POST data. (Prevents data from being POSTed
		# twice if a user hits the back button)
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

