from typing import final

from view.dispatcher_view import DispatcherView
from database import FREIGHT_MAP


@final
class FreightMapDispatcherView(DispatcherView):
    def __init__(self, controller):
        super().__init__(controller, map_id=FREIGHT_MAP)
