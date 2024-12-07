from typing import override

import jinja2
from scaffold.web.assets import Assets
from scaffold.web.base_app import BaseWebApp


class WebApp(BaseWebApp):
    @override
    def init(self) -> None:
        self.jinja_env.undefined = jinja2.StrictUndefined

        self.register_extension(Assets())
