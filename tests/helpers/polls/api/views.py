from dependencies import Injector, this
from dependencies.contrib.rest_framework import api_view, generic_api_view

from .commands import QuestionsGenericStat, QuestionsStat


@api_view
class QuestionsStatView(Injector):

    get = this.command.do
    command = QuestionsStat


@generic_api_view
class QuestionsGenericView(Injector):

    get = this.command.do
    command = QuestionsGenericStat
