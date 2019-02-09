from logging import getLogger

from button import Button


class ResumeGameButton(Button):
    """
    Implements Resume button on main game screen.
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.resume_game_button'))
        self.logger.info('START INIT')
        self.to_activate_on_controller_init = False
        self.logger.debug(f'to_activate_on_controller_init: {self.to_activate_on_controller_init}')
        self.text = ''
        self.logger.debug(f'text: {self.text}')
        self.font_name = 'Webdings'
        self.logger.debug(f'font_name: {self.font_name}')
        self.font_size = 40
        self.logger.debug(f'font_size: {self.font_size}')
        self.x_margin = 920
        self.logger.debug(f'x_margin: {self.x_margin}')
        self.y_margin = 0
        self.logger.debug(f'y_margin: {self.y_margin}')
        self.button_size = (80, 80)
        self.logger.debug(f'button_size: {self.button_size}')
        self.on_click_action = on_click_action
        self.logger.debug('on_click_action set successfully')
        self.logger.info('END INIT')
