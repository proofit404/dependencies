from django.conf.urls import include
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views import BadMetadata
from .views import BadNegotiation
from .views import BadVersion
from .views import DynamicUserViewSet
from .views import EmptyViewSet
from .views import InjectedGenericViewSet
from .views import InjectedViewSet
from .views import LoginAll
from .views import ThrottleAll
from .views import UserAction
from .views import UserListFilterFieldsView
from .views import UserListView
from .views import UserLogin
from .views import UserRetrieveView
from .views import UserViewSet


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
