from logging import getLogger

from ui.button import Button


class SkipOnboardingButton(Button):
    """
    Implements Skip button on onboarding screen.
    For properties definition see base Button class.
    """
    def __init__(self, on_click_action):
        super().__init__(logger=getLogger('root.button.skip_onboarding_button'))
        self.to_activate_on_controller_init = True
        self.text = ''
        self.font_name = 'Webdings'
        self.base_font_size_property = 40 / 80
        self.on_click_action = on_click_action
