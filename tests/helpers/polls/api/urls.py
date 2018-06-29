from django.conf.urls import include, url
from rest_framework.routers import SimpleRouter

from .views import (
    BadMetadata,
    BadNegotiation,
    BadVersion,
    LoginAll,
    ThrottleAll,
    UserAction,
    UserListView,
    UserLogin,
    UserRetrieveView,
    UserViewSet,
)


router = SimpleRouter()
router.register(r"user_set", UserViewSet.view_set_class)

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
    url(r"^", include(router.urls)),
]
