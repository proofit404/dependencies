from django.conf.urls import url

from .views import QuestionsStatView

urlpatterns = [
    url(r"^questions-stat/$", QuestionsStatView.as_view(), name="api-questions-stat")
]
