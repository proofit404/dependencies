from flask import Flask

from flask_project.views import _DispatchView


def _create_app():
    app = Flask(__name__)
    app.add_url_rule(
        "/test_dispatch_request/<int:id>/<word>/",
        view_func=_DispatchView.as_view("dispatch"),
    )
    return app
