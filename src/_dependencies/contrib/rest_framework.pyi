from typing import Any
from typing import Callable
from typing import Dict
from typing import NoReturn
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from django.db.models import Model
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet
from typing_extensions import Literal

from _dependencies.injector import Injector

_T = TypeVar("_T", APIView, GenericAPIView, ViewSet, GenericViewSet, ModelViewSet)

def api_view(injector: Injector) -> Injector: ...
def generic_api_view(injector: Injector) -> Injector: ...
def list_api_view(injector: Injector) -> Injector: ...
def retrieve_api_view(injector: Injector) -> Injector: ...
def view_set(injector: Injector) -> Injector: ...
def generic_view_set(injector: Injector) -> Injector: ...
def model_view_set(injector: Injector) -> Injector: ...
def apply_api_view_attributes(handler: Type[_T], injector: Injector) -> None: ...
def apply_generic_api_view_attributes(
    handler: Type[_T], injector: Injector
) -> None: ...
def apply_view_set_methods(handler: Type[_T], injector: Injector) -> None: ...
def apply_model_view_set_methods(handler: Type[_T], injector: Injector) -> None: ...
def get_validated_data(view: _T, request: Request) -> Dict[str, Any]: ...
def build_view_action(
    injector: Injector, action: str, detail: bool, validated_data: Dict[str, Any]
) -> Callable[[APIView, Request], Response]: ...
def build_view_set_method(
    injector: Injector,
    method: str,
    set_args: Callable[
        [Dict[str, Union[APIView, Serializer, Model]], Union[Serializer, Model]], None
    ],
    callback: Union[
        Callable[[Serializer, Model], None], Callable[[Model, Literal[None]], None]
    ],
) -> Callable[[Union[Serializer, Model]], None]: ...
def build_view_set_error(
    injector: Injector, method: str
) -> Callable[[Union[Serializer, Model]], NoReturn]: ...
