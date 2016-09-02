# -*- coding: utf-8 -*-

"""Create an application instance."""


import os

from clovr_launcher.app import create_app
from clovr_launcher.settings import DevConfig, ProdConfig


CONFIG = ProdConfig if os.environ.get('CLOVR_LAUNCHER_ENV') == 'prod' else DevConfig

app = create_app(CONFIG)
