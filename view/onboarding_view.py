from logging import getLogger

from pyglet.text import Label

from view import *
from ui.page_control.onboarding_page_control import OnboardingPageControl
from ui.button.skip_onboarding_button import SkipOnboardingButton
from i18n import I18N_RESOURCES
from ui.shader_sprite.onboarding_view_shader_sprite import OnboardingViewShaderSprite


class OnboardingView(View):
    def __init__(self):
        """
        Button click handlers:
            on_skip_onboarding                  on_click handler for skip onboarding button

        Properties:
            onboarding_page_control             OnboardingPageControl object
            skip_onboarding_button              SkipOnboardingButton object
            buttons                             list of all buttons
            skip_onboarding_label               "Skip onboarding" prompt at the bottom of the screen

        """
        def on_skip_onboarding(button):
            """
            Notifies the controller to deactivate the view.

            :param button:                      button that was clicked
            """
            self.controller.parent_controller.on_close_onboarding()
            self.controller.parent_controller.on_resume_game()

        super().__init__(logger=getLogger('root.app.onboarding.view'))
        self.onboarding_page_control = OnboardingPageControl()
        self.skip_onboarding_button = SkipOnboardingButton(on_click_action=on_skip_onboarding)
        self.buttons = [*self.onboarding_page_control.buttons, self.skip_onboarding_button]
        self.shader_sprite = OnboardingViewShaderSprite(view=self)
        self.skip_onboarding_label = None
        self.on_init_graphics()

    def on_init_graphics(self):
        """
        Initializes the view based on saved screen resolution and base offset.
        """
        self.on_change_screen_resolution(self.screen_resolution)

    def on_update_opacity(self, new_opacity):
        """
        Updates view opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()
        self.onboarding_page_control.on_update_opacity(new_opacity)
        for b in self.buttons:
            b.on_update_opacity(new_opacity)

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.shader_sprite.delete()
            self.skip_onboarding_label.delete()
            self.skip_onboarding_label = None
        else:
            self.skip_onboarding_label.color = (*WHITE_RGB, self.opacity)

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.shader_sprite.create()
        if self.skip_onboarding_label is None:
            self.skip_onboarding_label = Label(I18N_RESOURCES['skip_onboarding_string'][self.current_locale],
                                               font_name='Arial', font_size=self.bottom_bar_height // 5,
                                               color=(*WHITE_RGB, self.opacity),
                                               x=self.screen_resolution[0] - 5 * self.bottom_bar_height // 4,
                                               y=self.bottom_bar_height // 2, anchor_x='right', anchor_y='center',
                                               batch=self.batches['ui_batch'], group=self.groups['button_text'])

        self.onboarding_page_control.on_activate()
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        self.onboarding_page_control.on_deactivate()
        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.onboarding_page_control.on_change_screen_resolution(screen_resolution)
        self.skip_onboarding_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        self.skip_onboarding_button.x_margin = self.screen_resolution[0] - self.bottom_bar_height
        if self.is_activated:
            self.skip_onboarding_label.x = self.screen_resolution[0] - 5 * self.bottom_bar_height // 4
            self.skip_onboarding_label.y = self.bottom_bar_height // 2
            self.skip_onboarding_label.font_size = self.bottom_bar_height // 5

        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        self.onboarding_page_control.on_update_current_locale(new_locale)
        if self.is_activated:
            self.skip_onboarding_label.text = I18N_RESOURCES['skip_onboarding_string'][self.current_locale]

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        """
        Activates the shader, initializes all shader uniforms, draws shader sprite and deactivates the shader.
        """
        self.shader_sprite.draw()
        self.onboarding_page_control.on_apply_shaders_and_draw_vertices()
