from logging import getLogger

from button import Button


class IncrementWindowedResolutionButton(Button):
    """
    Implements "+" button for windowed resolution on settings screen.
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.increment_windowed_resolution_button'))
        self.logger.info('START INIT')
        self.to_activate_on_controller_init = False
        self.logger.debug(f'to_activate_on_controller_init: {self.to_activate_on_controller_init}')
        self.text = '+'
        self.logger.debug(f'text: {self.text}')
        self.font_name = 'Arial'
        self.logger.debug(f'font_name: {self.font_name}')
        self.font_size = 16
        self.logger.debug(f'font_size: {self.font_size}')
        self.x_margin = 300
        self.logger.debug(f'x_margin: {self.x_margin}')
        self.y_margin = 520
        self.logger.debug(f'y_margin: {self.y_margin}')
        self.button_size = (40, 40)
        self.logger.debug(f'button_size: {self.button_size}')
        self.on_click_action = on_click_action
        self.logger.debug('on_click_action set successfully')
        self.logger.info('END INIT')
