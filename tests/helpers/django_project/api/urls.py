from django.conf.urls import include
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from django_project.api.views import BadMetadata
from django_project.api.views import BadNegotiation
from django_project.api.views import BadVersion
from django_project.api.views import CustomThrottleScope
from django_project.api.views import DefaultThrottleScope
from django_project.api.views import DynamicUserViewSet
from django_project.api.views import EmptyViewSet
from django_project.api.views import InjectedGenericViewSet
from django_project.api.views import InjectedViewSet
from django_project.api.views import LoginAll
from django_project.api.views import ThrottleAll
from django_project.api.views import UserAction
from django_project.api.views import UserListFilterFieldsView
from django_project.api.views import UserListView
from django_project.api.views import UserLogin
from django_project.api.views import UserRetrieveView
from django_project.api.views import UserViewSet

router = SimpleRouter()
# FIXME: We can not user router without `basename` because `queryset`
# is a `property` and used as class attribute.
router.register(r"view_set", InjectedViewSet.as_viewset(), basename="view_set")
router.register(
    r"generic_view_set",
    InjectedGenericViewSet.as_viewset(),
    basename="generic_view_set",
)
router.register(r"user_set", UserViewSet.as_viewset(), basename="user")
router.register(
    r"dynamic_user_set", DynamicUserViewSet.as_viewset(), basename="dynamic_user"
)
router.register(r"empty_set", EmptyViewSet.as_viewset(), basename="empty")

urlpatterns = [
    url(r"^action/$", UserAction.as_view(), name="api-action"),
    url(r"^login/$", UserLogin.as_view(), name="api-login"),
    url(r"^login_all/$", LoginAll.as_view(), name="api-login-all"),
    url(r"^throttle_all/$", ThrottleAll.as_view(), name="api-throttle-all"),
    url(
        r"^default_throttle_scope/$",
        DefaultThrottleScope.as_view(),
        name="api-default-throttle-scope",
    ),
    url(
        r"^custom_throttle_scope/$",
        CustomThrottleScope.as_view(),
        name="api-custom-throttle-scope",
    ),
    url(r"^negotiate/$", BadNegotiation.as_view(), name="api-negotiate"),
    url(r"^versioning/$", BadVersion.as_view(), name="api-version"),
    url(r"^metadata/$", BadMetadata.as_view(), name="api-metadata"),
    url(r"^users/$", UserListView.as_view(), name="api-user-list"),
    url(r"^users/(?P<nick>\w+)/$", UserRetrieveView.as_view(), name="api-user-detail"),
    url(
        r"^user_fields/$",
        UserListFilterFieldsView.as_view(),
        name="api-user-list-fields",
    ),
    url(r"^", include(router.urls)),
]
