from logging import getLogger

from button import Button


class ZoomInButton(Button):
    """
    Implements Zoom in button for game map on main game screen.
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action, on_hover_action, on_leave_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.zoom_in_button'))
        self.logger.info('START INIT')
        self.transparent = False
        self.logger.debug(f'transparent: {self.transparent}')
        self.to_activate_on_controller_init = False
        self.logger.debug(f'to_activate_on_controller_init: {self.to_activate_on_controller_init}')
        self.text = '< >'
        self.logger.debug(f'text: {self.text}')
        self.font_name = 'Perfo'
        self.logger.debug(f'font_name: {self.font_name}')
        self.is_bold = True
        self.logger.debug(f'is_bold: {self.is_bold}')
        self.font_size = 30
        self.logger.debug(f'font_size: {self.font_size}')
        self.x_margin = 0
        self.logger.debug(f'x_margin: {self.x_margin}')
        self.y_margin = 602
        self.logger.debug(f'y_margin: {self.y_margin}')
        self.button_size = (80, 80)
        self.logger.debug(f'button_size: {self.button_size}')
        self.on_click_action = on_click_action
        self.logger.debug('on_click_action set successfully')
        self.on_hover_action = on_hover_action
        self.logger.debug('on_hover_action set successfully')
        self.on_leave_action = on_leave_action
        self.logger.debug('on_leave_action set successfully')
        self.logger.info('END INIT')
