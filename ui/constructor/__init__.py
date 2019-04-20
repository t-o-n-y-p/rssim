from logging import getLogger

from pyglet.text import Label

from i18n import I18N_RESOURCES
from ui import *
from ui.button import create_two_state_button
from ui.button.build_construction_button import BuildConstructionButton
from ui.button.set_money_target_button import SetMoneyTargetButton
from ui.button.reset_money_target_button import ResetMoneyTargetButton


def cell_is_active(fn):
    """
    Use this decorator to execute function only if cell is active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_cell_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_cell_is_activated


def cell_is_not_active(fn):
    """
    Use this decorator to execute function only if cell is not active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_cell_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_cell_is_not_activated


class ConstructorCell:
    """
    Implements base class for constructor cell.
    """
    def __init__(self, construction_type, row, current_locale,
                 on_buy_construction_action, on_set_money_target_action, on_reset_money_target_action):
        """
        Button click handlers:
            on_set_money_target                 on_click handler for set money target button
            on_reset_money_target               on_click handler for reset money target button
            on_buy_construction                 on_click handler for build construction button

        Properties:
            logger                              telemetry instance
            is_activated                        indicates if cell is active
            construction_type                   type of construction: track or environment
            row                                 number of cell on constructor screen
            surface                             surface to draw all UI objects on
            batches                             batches to group all labels and sprites
            groups                              defines drawing layers (some labels and sprites behind others)
            current_locale                      current locale selected by player
            on_buy_construction_action          is activated when player buys construction
            on_set_money_target_action          is activated when money target is activated by player
            on_reset_money_target_action        is activated when money target is deactivated by player
            entity_number                       number of track or environment tier
            data                                one row of data from construction state matrix
            screen_resolution                   current game window resolution
            position                            position of the left bottom corner of the cell
            size                                cell width and height
            locked_label                        label for locked entity or not enough money case
            title_key                           resource key for cell title
            title_label                         label for cell title
            description_keys                    dictionary of resource keys for cell description
            description_label                   label for cell description
            placeholder_key                     resource key for cell placeholder
            placeholder_label                   label for cell placeholder
            enable_money_target_button          SetMoneyTargetButton object
            disable_money_target_button         ResetMoneyTargetButton object
            build_button                        BuildConstructionButton object
            buttons                             list of all buttons
            money                               amount of money the player can operate
            money_target_activated              indicates if money target is activated for this cell

        :param construction_type:               type of construction: track or environment
        :param row:                             number of cell on constructor screen
        :param current_locale:                  current locale selected by player
        :param on_buy_construction_action:      is activated when player buys construction
        :param on_set_money_target_action:      is activated when money target is activated by player
        :param on_reset_money_target_action:    is activated when money target is deactivated by player
        """
        def on_set_money_target(button):
            """
            Deactivates set target button, activated reset target button.
            Notifies the view about money target update.

            :param button:                      button that was clicked
            """
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate()
            self.on_set_money_target_action(self.construction_type, self.row, self.entity_number)

        def on_reset_money_target(button):
            """
            Deactivates reset target button, activated set target button.
            Notifies the view about money target update.

            :param button:                      button that was clicked
            """
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate()
            self.on_reset_money_target_action()

        def on_buy_construction(button):
            """
            Deactivates all buttons. Notifies the view about construction state update.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            self.enable_money_target_button.on_deactivate()
            self.disable_money_target_button.on_deactivate()
            self.on_buy_construction_action(self.construction_type, self.row, self.entity_number)

        self.logger = getLogger(f'root.app.game.map.constructor.view.cell.{construction_type}.{row}')
        self.is_activated = False
        self.construction_type, self.row = construction_type, row
        self.surface, self.batches, self.groups, self.current_locale = SURFACE, BATCHES, GROUPS, current_locale
        self.on_buy_construction_action = on_buy_construction_action
        self.on_set_money_target_action = on_set_money_target_action
        self.on_reset_money_target_action = on_reset_money_target_action
        self.entity_number = None
        self.data = None
        self.screen_resolution = (0, 0)
        self.position = [0, 0]
        self.size = [0, 0]
        self.locked_label = None
        self.title_key = None
        self.title_label = None
        self.description_keys = {}
        self.description_label = None
        self.placeholder_key = None
        self.placeholder_label = None
        self.enable_money_target_button, self.disable_money_target_button \
            = create_two_state_button(SetMoneyTargetButton(on_click_action=on_set_money_target),
                                      ResetMoneyTargetButton(on_click_action=on_reset_money_target))
        self.build_button = BuildConstructionButton(on_click_action=on_buy_construction)
        self.buttons = [self.enable_money_target_button, self.disable_money_target_button, self.build_button]
        self.money = 0
        self.money_target_activated = False
        self.opacity = 0

    @cell_is_active
    def on_assign_new_data(self, entity_number, data):
        """
        Fully updates data inside the cell.

        :param entity_number:           number of the track or environment tier
        :param data:                    one row of data from construction state matrix
        """
        self.entity_number = entity_number
        self.data = data
        # when data is empty, it means no more tracks/tiers are available, only placeholder is active
        if len(self.data) == 0 or self.entity_number == 0:
            if self.placeholder_label is None:
                self.placeholder_label = Label(I18N_RESOURCES[self.placeholder_key][self.current_locale],
                                               font_name='Arial', font_size=int(11 * self.size[1] / 40),
                                               color=(*GREY_RGB, self.opacity),
                                               x=self.position[0] + self.size[0] // 2,
                                               y=self.position[1] + self.size[1] // 2,
                                               anchor_x='center', anchor_y='center',
                                               batch=self.batches['ui_batch'], group=self.groups['button_text'])
            else:
                self.placeholder_label.text = I18N_RESOURCES[self.placeholder_key][self.current_locale]

            if self.locked_label is not None:
                self.locked_label.delete()
                self.locked_label = None

            if self.title_label is not None:
                self.title_label.delete()
                self.title_label = None

            if self.description_label is not None:
                self.description_label.delete()
                self.description_label = None

            for b in self.buttons:
                b.on_deactivate()

        else:
            if self.placeholder_label is not None:
                self.placeholder_label.delete()
                self.placeholder_label = None

            if not self.data[UNLOCK_AVAILABLE] and not self.data[UNDER_CONSTRUCTION]:
                if self.locked_label is None:
                    self.locked_label = Label('', font_name='Webdings',
                                              font_size=int(self.build_button.base_font_size_property * self.size[1]),
                                              color=(*GREY_RGB, self.opacity),
                                              x=self.position[0] + self.size[0] - self.size[1] // 2,
                                              y=self.position[1] + self.size[1] // 2,
                                              anchor_x='center', anchor_y='center',
                                              batch=self.batches['ui_batch'], group=self.groups['button_text'])
                else:
                    self.locked_label.text = ''

            if self.title_label is None:
                self.title_label = Label(I18N_RESOURCES[self.title_key][self.current_locale].format(self.entity_number),
                                         font_name='Arial', font_size=int(0.3 * self.size[1]),
                                         color=(*WHITE_RGB, self.opacity),
                                         x=self.position[0] + self.size[1] // 8,
                                         y=self.position[1] + int(0.7 * self.size[1]),
                                         anchor_x='left', anchor_y='center',
                                         batch=self.batches['ui_batch'], group=self.groups['button_text'])
            else:
                self.title_label.text = I18N_RESOURCES[self.title_key][self.current_locale].format(self.entity_number)

            if self.description_label is None:
                self.description_label = Label(' ', font_name='Arial', font_size=self.size[1] // 5,
                                               color=(*GREY_RGB, self.opacity),
                                               x=self.position[0] + self.size[1] // 8,
                                               y=self.position[1] + int(22 * self.size[1] / 80),
                                               anchor_x='left', anchor_y='center',
                                               batch=self.batches['ui_batch'], group=self.groups['button_text'])

            self.on_update_description_label()
            self.on_update_build_button_state()

    def on_update_description_label(self):
        """
        Updates cell description based on data.
        Different constructions have different states, so this method must be overridden by subclasses.
        """
        pass

    @cell_is_active
    def on_update_state(self, data):
        """
        Updates buttons and description state.

        :param data:                    one row of data from construction state matrix
        """
        self.data = data
        # when UNLOCK_AVAILABLE flag becomes enabled, we need to activate build button
        # (or locked label if there is no enough money) and set money target button
        if self.data[UNLOCK_AVAILABLE]:
            self.on_update_build_button_state()
            if not self.money_target_activated and not self.enable_money_target_button.is_activated \
                    and not self.disable_money_target_button.is_activated:
                self.on_deactivate_money_target()

        if self.is_activated:
            self.on_update_description_label()

    def on_update_money(self, money):
        """
        Updates cell state based on available money.

        :param money:                   amount of money the player can operate
        """
        self.money = money
        self.on_update_build_button_state()

    @cell_is_active
    def on_update_build_button_state(self):
        """
        Updates locked label and build button state based on available money.
        """
        if self.data[UNLOCK_AVAILABLE]:
            if self.money >= self.data[PRICE]:
                self.build_button.on_activate()
                if self.locked_label is not None:
                    self.locked_label.delete()
                    self.locked_label = None

            else:
                self.build_button.on_deactivate()
                if self.locked_label is None:
                    self.locked_label = Label('', font_name='Webdings',
                                              font_size=int(self.build_button.base_font_size_property * self.size[1]),
                                              color=(*GREY_RGB, self.opacity),
                                              x=self.position[0] + self.size[0] - self.size[1] // 2,
                                              y=self.position[1] + self.size[1] // 2,
                                              anchor_x='center', anchor_y='center',
                                              batch=self.batches['ui_batch'], group=self.groups['button_text'])
                else:
                    self.locked_label.text = ''

    @cell_is_not_active
    def on_activate(self):
        """
        Activates the cell.
        """
        self.is_activated = True

    @cell_is_active
    def on_deactivate(self):
        """
        Deactivates the cell, deletes all labels, deactivates all buttons.
        """
        self.is_activated = False
        self.data = []
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.screen_resolution = screen_resolution
        self.size = (int(6.875 * int(72 / 1280 * self.screen_resolution[0])),
                     int(72 / 1280 * self.screen_resolution[0]))
        interval_between_cells = int(72 / 1280 * self.screen_resolution[0]) // 4
        general_height = 4 * self.size[1] + 3 * interval_between_cells
        fetched_coords = (self.screen_resolution[0] // 2 - self.size[0] - interval_between_cells // 2,
                          self.screen_resolution[1] // 2 + general_height // 2 - self.size[1] // 4 - self.size[1] // 2)
        self.position = (fetched_coords[0] + self.construction_type * (self.size[0] + interval_between_cells),
                         fetched_coords[1] - self.row * (self.size[1] + interval_between_cells))
        if self.locked_label is not None:
            self.locked_label.x = self.position[0] + self.size[0] - self.size[1] // 2
            self.locked_label.y = self.position[1] + self.size[1] // 2
            self.locked_label.font_size = int(self.build_button.base_font_size_property * self.size[1])

        if self.title_label is not None:
            self.title_label.x = self.position[0] + self.size[1] // 8
            self.title_label.y = self.position[1] + int(0.7 * self.size[1])
            self.title_label.font_size = int(0.3 * self.size[1])

        if self.description_label is not None:
            self.description_label.x = self.position[0] + self.size[1] // 8
            self.description_label.y = self.position[1] + int(22 * self.size[1] / 80)
            self.description_label.font_size = self.size[1] // 5

        if self.placeholder_label is not None:
            self.placeholder_label.x = self.position[0] + self.size[0] // 2
            self.placeholder_label.y = self.position[1] + self.size[1] // 2
            self.placeholder_label.font_size = int(11 * self.size[1] / 40)

        self.build_button.on_size_changed((self.size[1], self.size[1]))
        self.enable_money_target_button.on_size_changed((self.size[1], self.size[1]))
        self.disable_money_target_button.on_size_changed((self.size[1], self.size[1]))
        self.build_button.x_margin = self.position[0] + self.size[0] - self.size[1]
        self.build_button.y_margin = self.position[1]
        self.enable_money_target_button.x_margin = self.position[0] + self.size[0] - self.size[1] * 2 + 2
        self.enable_money_target_button.y_margin = self.position[1]
        self.disable_money_target_button.x_margin = self.position[0] + self.size[0] - self.size[1] * 2 + 2
        self.disable_money_target_button.y_margin = self.position[1]

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.is_activated:
            if len(self.data) == 0 or self.entity_number == 0:
                self.placeholder_label.text = I18N_RESOURCES[self.placeholder_key][self.current_locale]
            else:
                self.title_label.text = I18N_RESOURCES[self.title_key][self.current_locale].format(self.entity_number)
                self.on_update_description_label()

    def on_activate_money_target(self):
        """
        Activates money target for the cell and all appropriate buttons.
        """
        self.money_target_activated = True
        if self.is_activated and len(self.data) > 0:
            self.enable_money_target_button.on_deactivate()
            if self.data[UNLOCK_AVAILABLE]:
                self.disable_money_target_button.on_activate()
            else:
                self.disable_money_target_button.on_deactivate()

    def on_deactivate_money_target(self):
        """
        Deactivates money target for the cell and all appropriate buttons.
        """
        self.money_target_activated = False
        if self.is_activated and len(self.data) > 0:
            self.disable_money_target_button.on_deactivate()
            if self.data[UNLOCK_AVAILABLE]:
                self.enable_money_target_button.on_activate()
            else:
                self.enable_money_target_button.on_deactivate()

    def on_update_opacity(self):
        if self.is_activated and self.opacity < 255:
            self.opacity += 15
            self.on_update_sprite_opacity()

        if not self.is_activated and self.opacity > 0:
            self.opacity -= 15
            self.on_update_sprite_opacity()

    def on_update_sprite_opacity(self):
        if self.opacity <= 0:
            if self.locked_label is not None:
                self.locked_label.delete()
                self.locked_label = None

            if self.title_label is not None:
                self.title_label.delete()
                self.title_label = None

            if self.description_label is not None:
                self.description_label.delete()
                self.description_label = None

            if self.placeholder_label is not None:
                self.placeholder_label.delete()
                self.placeholder_label = None

        else:
            if self.locked_label is not None:
                self.locked_label.color = (*GREY_RGB, self.opacity)

            if self.title_label is not None:
                self.title_label.color = (*WHITE_RGB, self.opacity)

            if self.description_label is not None:
                self.description_label.color = (*GREY_RGB, self.opacity)

            if self.placeholder_label is not None:
                self.placeholder_label.color = (*GREY_RGB, self.opacity)
