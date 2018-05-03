from django.conf.urls import url

from .views import QuestionsStatView, UserListView, UserRetrieveView

urlpatterns = [
    url(r"^questions-stat/$", QuestionsStatView.as_view(), name="api-questions-stat"),
    url(r"^users/$", UserListView.as_view(), name="api-user-list"),
    url(r"^users/(?P<nick>\w+)/$", UserRetrieveView.as_view(), name="api-user-detail"),
]
