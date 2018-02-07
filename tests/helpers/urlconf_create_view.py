from dependencies import Injector
from dependencies.contrib.django import create_view
from django.conf.urls import url
from polls.models import Question


@create_view
class Container(Injector):

    model_cls = Question
    fields = ['question_text', 'pub_date']
    success_url = '/polls/add/'


urlpatterns = [
    url(r'^polls/add/$', Container.as_view()),
]
