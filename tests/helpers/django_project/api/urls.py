from django.conf.urls import include
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from django_project.api.views import _BadMetadata
from django_project.api.views import _BadNegotiation
from django_project.api.views import _BadVersion
from django_project.api.views import _CustomThrottleScope
from django_project.api.views import _DefaultThrottleScope
from django_project.api.views import _DynamicUserViewSet
from django_project.api.views import _EmptyViewSet
from django_project.api.views import _InjectedGenericViewSet
from django_project.api.views import _InjectedViewSet
from django_project.api.views import _LoginAll
from django_project.api.views import _ThrottleAll
from django_project.api.views import _UserAction
from django_project.api.views import _UserListFilterFieldsView
from django_project.api.views import _UserListView
from django_project.api.views import _UserLogin
from django_project.api.views import _UserRetrieveView
from django_project.api.views import _UserViewSet


router = SimpleRouter()

# FIXME: We can not user router without `basename` because `queryset`
# is a `property` and used as class attribute.
router.register(r"view_set", _InjectedViewSet.as_viewset(), basename="view_set")

router.register(
    r"generic_view_set",
    _InjectedGenericViewSet.as_viewset(),
    basename="generic_view_set",
)

router.register(r"user_set", _UserViewSet.as_viewset(), basename="user")

router.register(
    r"dynamic_user_set", _DynamicUserViewSet.as_viewset(), basename="dynamic_user"
)

router.register(r"empty_set", _EmptyViewSet.as_viewset(), basename="empty")


urlpatterns = [
    url(r"^action/$", _UserAction.as_view(), name="api-action"),
    url(r"^login/$", _UserLogin.as_view(), name="api-login"),
    url(r"^login_all/$", _LoginAll.as_view(), name="api-login-all"),
    url(r"^throttle_all/$", _ThrottleAll.as_view(), name="api-throttle-all"),
    url(
        r"^default_throttle_scope/$",
        _DefaultThrottleScope.as_view(),
        name="api-default-throttle-scope",
    ),
    url(
        r"^custom_throttle_scope/$",
        _CustomThrottleScope.as_view(),
        name="api-custom-throttle-scope",
    ),
    url(r"^negotiate/$", _BadNegotiation.as_view(), name="api-negotiate"),
    url(r"^versioning/$", _BadVersion.as_view(), name="api-version"),
    url(r"^metadata/$", _BadMetadata.as_view(), name="api-metadata"),
    url(r"^users/$", _UserListView.as_view(), name="api-user-list"),
    url(r"^users/(?P<nick>\w+)/$", _UserRetrieveView.as_view(), name="api-user-detail"),
    url(
        r"^user_fields/$",
        _UserListFilterFieldsView.as_view(),
        name="api-user-list-fields",
    ),
    url(r"^", include(router.urls)),
]
