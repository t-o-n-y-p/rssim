from typing import final

from database import CONFIG_DB_CURSOR
from ui import MAP_CAMERA
from ui.button_v2 import MapButtonV2


def shop_buttons(f):
    def _shop_buttons(*args, **kwargs):
        f(*args, **kwargs)
        CONFIG_DB_CURSOR.execute('''SELECT COUNT(*) FROM shops_config WHERE map_id = ?''', (args[0].map_id,))
        shop_buttons_list = [
            OpenShopDetailsButtonV2(
                logger=args[0].logger.getChild(f'shop_id.{shop_id}.open_shop_details_button_v2'),
                parent_viewport=args[0].viewport, map_id=args[0].map_id, shop_id=shop_id
            ) for shop_id in range(CONFIG_DB_CURSOR.fetchone()[0])
        ]
        args[0].__setattr__('shop_buttons', shop_buttons_list)
        args[0].ui_objects.extend(shop_buttons_list)
        for b in shop_buttons_list:
            def on_click():
                args[0].__getattribute__('on_click_action_open_shop_details_button_v2')(b.shop_id)

            def on_hover():
                args[0].__getattribute__('on_hover_action_open_shop_details_button_v2')()

            def on_leave():
                args[0].__getattribute__('on_leave_action_open_shop_details_button_v2')()

            b.__setattr__('on_click', on_click)
            b.__setattr__('on_hover', on_hover)
            b.__setattr__('on_leave', on_leave)
            args[0].fade_out_animation.child_animations.append(b.fade_out_animation)
            args[0].on_mouse_press_handlers.extend(b.on_mouse_press_handlers)
            args[0].on_mouse_release_handlers.extend(b.on_mouse_release_handlers)
            args[0].on_mouse_motion_handlers.extend(b.on_mouse_motion_handlers)
            args[0].on_mouse_leave_handlers.extend(b.on_mouse_leave_handlers)
            args[0].on_window_resize_handlers.extend(b.on_window_resize_handlers)

    return _shop_buttons


@final
class OpenShopDetailsButtonV2(MapButtonV2):
    def __init__(self, logger, parent_viewport, map_id, shop_id):
        super().__init__(logger, parent_viewport)
        CONFIG_DB_CURSOR.execute(
            '''SELECT button_x, button_y FROM shops_config WHERE map_id = ? AND shop_id = ?''', (map_id, shop_id)
        )
        self.x, self.y = CONFIG_DB_CURSOR.fetchone()
        self.shop_id = shop_id

    def get_width(self):
        return int(MAP_CAMERA.zoom * 250)

    def get_height(self):
        return int(MAP_CAMERA.zoom * 40)
