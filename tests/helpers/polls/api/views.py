from dependencies import Injector, this
from dependencies.contrib.rest_framework import api_view

from .commands import QuestionsStat


@api_view
class QuestionsStatView(Injector):

    get = this.command.do
    command = QuestionsStat
