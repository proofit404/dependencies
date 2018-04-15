from django.conf.urls import url

from .views import DispatchView, EmptyView, KwargsView, SelfView, UserView

urlpatterns = [
    url(r"^test_dispatch_request/(\d+)/(\w+)/$", DispatchView.as_view()),
    url(r"^test_empty_request/(\d+)/(\w+)/$", EmptyView.as_view()),
    url(r"^test_inject_user/(?P<pk>\d+)/(?P<slug>\w+)/$", UserView.as_view()),
    url(r"^test_inject_kwargs/(?P<pk>\d+)/(?P<slug>\w+)/$", KwargsView.as_view()),
    url(r"^test_inject_self/(?P<pk>\d+)/(?P<slug>\w+)/$", SelfView.as_view()),
]
