from django.conf.urls import url

from .views import QuestionsGenericView, QuestionsStatView

urlpatterns = [
    url(r"^questions-stat/$", QuestionsStatView.as_view(), name="api-questions-stat"),
    url(
        r"^questions-generic-stat/$",
        QuestionsGenericView.as_view(),
        name="api-questions-generic-stat",
    ),
]
