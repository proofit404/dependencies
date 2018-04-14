from django.conf.urls import url

from .views import DispatchView, KwargsView, UserView

urlpatterns = [
    url(r"^test_dispatch_request/(\d+)/(\w+)/$", DispatchView.as_view()),
    url(r"^test_inject_user/(?P<pk>\d+)/(?P<slug>\w+)/$", UserView.as_view()),
    url(r"^test_pass_kwargs/(?P<pk>\d+)/(?P<slug>\w+)/$", KwargsView.as_view()),
]
