from django.conf.urls import include
from django.conf.urls import url

from django_project.views import _DispatchView
from django_project.views import _DynamicQuestionTemplateView
from django_project.views import _EmptyFormView
from django_project.views import _EmptyView
from django_project.views import _KwargsView
from django_project.views import _QuestionFormView
from django_project.views import _QuestionTemplateView
from django_project.views import _SelfView
from django_project.views import _UserView


urlpatterns = [
    url(r"^test_dispatch_request/(\d+)/(\w+)/$", _DispatchView.as_view()),
    url(r"^test_empty_request/(\d+)/(\w+)/$", _EmptyView.as_view()),
    url(r"^test_inject_user/(?P<pk>\d+)/(?P<slug>\w+)/$", _UserView.as_view()),
    url(r"^test_inject_kwargs/(?P<pk>\d+)/(?P<slug>\w+)/$", _KwargsView.as_view()),
    url(r"^test_inject_self/(?P<pk>\d+)/(?P<slug>\w+)/$", _SelfView.as_view()),
    url(r"^test_template_view/(?P<pk>\d+)/$", _QuestionTemplateView.as_view()),
    url(
        r"^test_template_view_dynamic/(?P<pk>\d+)/$",
        _DynamicQuestionTemplateView.as_view(),
    ),
    url(r"^test_form_view/(?P<pk>\d+)/$", _QuestionFormView.as_view()),
    url(r"^empty_form_view/$", _EmptyFormView.as_view()),
    url(r"^api/", include("django_project.api.urls")),
]
