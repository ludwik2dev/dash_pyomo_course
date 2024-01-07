import dash

from .dashboard.callbacks import * 
from .dashboard.layout import layout as dashboard_layout


dash.register_page(__name__)


layout = dashboard_layout