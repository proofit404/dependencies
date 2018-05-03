from django.conf.urls import url

from .views import QuestionsStatView, UserListView, UserLogin, UserRetrieveView

urlpatterns = [
    url(r"^questions-stat/$", QuestionsStatView.as_view(), name="api-questions-stat"),
    url(r"^login/$", UserLogin.as_view(), name="api-login"),
    url(r"^users/$", UserListView.as_view(), name="api-user-list"),
    url(r"^users/(?P<nick>\w+)/$", UserRetrieveView.as_view(), name="api-user-detail"),
]
