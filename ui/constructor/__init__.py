from logging import getLogger

from database import USER_DB_CURSOR
from ui import *
from ui.button import create_two_state_button
from ui.button.build_construction_button import BuildConstructionButton
from ui.button.set_money_target_button import SetMoneyTargetButton
from ui.button.reset_money_target_button import ResetMoneyTargetButton
from ui.label.constructor_locked_label import ConstructorLockedLabel
from ui.label.constructor_level_placeholder_label import ConstructorLevelPlaceholderLabel
from ui.label.under_construction_days_label import UnderConstructionDaysLabel
from ui.label.under_construction_hours_minutes_label import UnderConstructionHoursMinutesLabel


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


def unlock_available(fn):
    """
    Use this decorator to execute function
    only if unlock_available flag is enabled for entity represented by this cell.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_unlock_available(*args, **kwargs):
        if len(args[0].data) > 0 and args[0].data[UNLOCK_AVAILABLE]:
            fn(*args, **kwargs)

    return _handle_if_unlock_available


class ConstructorCell:
    """
    Implements base class for constructor cell.
    """
    def __init__(self, construction_type, row, on_buy_construction_action, on_set_money_target_action,
                 on_reset_money_target_action, parent_viewport):
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
            opacity                             current opacity for the whole cell

        :param construction_type:               type of construction: track or environment
        :param row:                             number of cell on constructor screen
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
            button.on_deactivate(instant=True)
            self.enable_money_target_button.on_deactivate(instant=True)
            self.disable_money_target_button.on_deactivate(instant=True)
            self.on_buy_construction_action(self.construction_type, self.row, self.entity_number)

        self.logger = getLogger(f'root.app.game.map.constructor.view.cell.{construction_type}.{row}')
        self.is_activated = False
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        self.construction_type, self.row = construction_type, row
        self.surface, self.batches, self.groups = SURFACE, BATCHES, GROUPS
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.on_buy_construction_action = on_buy_construction_action
        self.on_set_money_target_action = on_set_money_target_action
        self.on_reset_money_target_action = on_reset_money_target_action
        self.entity_number = None
        self.data = []
        self.screen_resolution = (0, 0)
        self.locked_label = ConstructorLockedLabel(parent_viewport=self.viewport)
        self.title_label = None
        self.level_required_label = ConstructorLevelPlaceholderLabel(parent_viewport=self.viewport)
        self.previous_entity_required_label = None
        self.environment_required_label = None
        self.unlock_available_label = None
        self.under_construction_days_label = UnderConstructionDaysLabel(parent_viewport=self.viewport)
        self.under_construction_hours_minutes_label = UnderConstructionHoursMinutesLabel(parent_viewport=self.viewport)
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
            self.locked_label.delete()
            self.title_label.delete()
            self.level_required_label.delete()
            self.previous_entity_required_label.delete()
            if self.environment_required_label is not None:
                self.environment_required_label.delete()

            self.unlock_available_label.delete()
            self.under_construction_days_label.delete()
            self.under_construction_hours_minutes_label.delete()
            for b in self.buttons:
                b.on_deactivate()

        else:
            if not self.data[UNLOCK_AVAILABLE] and not self.data[UNDER_CONSTRUCTION]:
                self.locked_label.create()
            else:
                self.locked_label.delete()

            self.title_label.on_update_args((self.entity_number, ))
            self.title_label.create()
            self.unlock_available_label.on_update_args((self.data[PRICE], ))
            self.level_required_label.on_update_args((self.data[LEVEL_REQUIRED], ))
            self.previous_entity_required_label.on_update_args((self.entity_number - 1, ))
            if self.environment_required_label is not None:
                self.environment_required_label.on_update_args((self.data[ENVIRONMENT_REQUIRED], ))

            self.on_update_description_label()
            self.on_update_build_button_state()

    def on_update_description_label(self):
        """
        Updates cell description based on data.
        Different constructions have different states, so this method must be overridden by subclasses.
        """
        pass

    @cell_is_active
    def on_update_state(self):
        """
        Updates buttons and description state.
        """
        self.on_update_description_label()
        # when UNLOCK_AVAILABLE flag becomes enabled, we need to activate build button
        # (or locked label if there is no enough money) and set money target button
        if self.data[UNLOCK_AVAILABLE]:
            self.locked_label.delete()
            self.on_update_build_button_state()
            if not self.money_target_activated and not self.enable_money_target_button.is_activated \
                    and not self.disable_money_target_button.is_activated:
                self.on_deactivate_money_target()

    def on_update_money(self, money):
        """
        Updates cell state based on available money.

        :param money:                   amount of money the player can operate
        """
        self.money = money
        self.on_update_build_button_state()

    @cell_is_active
    @unlock_available
    def on_update_build_button_state(self):
        """
        Updates locked label and build button state based on available money.
        """
        self.build_button.opacity = self.opacity
        if self.money >= self.data[PRICE]:
            self.build_button.on_activate()
        else:
            self.build_button.on_disable()

    @cell_is_not_active
    def on_activate(self):
        """
        Activates the cell.
        """
        self.is_activated = True

    @cell_is_active
    def on_deactivate(self):
        """
        Deactivates the cell and all buttons, clears the data.
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
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        inner_area_rect = get_inner_area_rect(self.screen_resolution)
        self.viewport.x1 = inner_area_rect[0] \
                           + self.construction_type * (int(6.875 * bottom_bar_height) + bottom_bar_height // 4)
        self.viewport.x2 = self.viewport.x1 + int(6.875 * bottom_bar_height)
        if self.construction_type == TRACKS:
            self.viewport.y1 = inner_area_rect[1] \
                               + (CONSTRUCTOR_VIEW_TRACK_CELLS - 1 - self.row) \
                               * (bottom_bar_height + bottom_bar_height // 4)
        elif self.construction_type == ENVIRONMENT:
            self.viewport.y1 = inner_area_rect[1] \
                               + (CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS - 1 - self.row) \
                               * (bottom_bar_height + bottom_bar_height // 4)

        self.viewport.y2 = self.viewport.y1 + bottom_bar_height
        self.locked_label.on_change_screen_resolution(self.screen_resolution)
        self.title_label.on_change_screen_resolution(self.screen_resolution)
        self.level_required_label.on_change_screen_resolution(self.screen_resolution)
        self.previous_entity_required_label.on_change_screen_resolution(self.screen_resolution)
        if self.environment_required_label is not None:
            self.environment_required_label.on_change_screen_resolution(self.screen_resolution)

        self.unlock_available_label.on_change_screen_resolution(self.screen_resolution)
        self.under_construction_days_label.on_change_screen_resolution(self.screen_resolution)
        self.under_construction_hours_minutes_label.on_change_screen_resolution(self.screen_resolution)
        self.build_button.on_size_changed((bottom_bar_height, bottom_bar_height))
        self.enable_money_target_button.on_size_changed((bottom_bar_height, bottom_bar_height))
        self.disable_money_target_button.on_size_changed((bottom_bar_height, bottom_bar_height))
        self.build_button.x_margin = self.viewport.x2 - bottom_bar_height
        self.build_button.y_margin = self.viewport.y1
        self.enable_money_target_button.x_margin = self.viewport.x2 - bottom_bar_height * 2 + 2
        self.enable_money_target_button.y_margin = self.viewport.y1
        self.disable_money_target_button.x_margin = self.viewport.x2 - bottom_bar_height * 2 + 2
        self.disable_money_target_button.y_margin = self.viewport.y1

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        self.title_label.on_update_current_locale(self.current_locale)
        self.level_required_label.on_update_current_locale(self.current_locale)
        self.previous_entity_required_label.on_update_current_locale(self.current_locale)
        if self.environment_required_label is not None:
            self.environment_required_label.on_update_current_locale(self.current_locale)

        self.unlock_available_label.on_update_current_locale(self.current_locale)
        self.under_construction_days_label.on_update_current_locale(self.current_locale)
        self.under_construction_hours_minutes_label.on_update_current_locale(self.current_locale)

    def on_activate_money_target(self):
        """
        Activates money target for the cell and all appropriate buttons.
        """
        self.money_target_activated = True
        if self.is_activated and len(self.data) > 0:
            self.enable_money_target_button.on_deactivate(instant=True)
            if self.data[UNLOCK_AVAILABLE]:
                self.disable_money_target_button.opacity = self.opacity
                self.disable_money_target_button.on_activate()
            else:
                self.disable_money_target_button.on_deactivate(instant=True)

    def on_deactivate_money_target(self):
        """
        Deactivates money target for the cell and all appropriate buttons.
        """
        self.money_target_activated = False
        if self.is_activated and len(self.data) > 0:
            self.disable_money_target_button.on_deactivate(instant=True)
            if self.data[UNLOCK_AVAILABLE]:
                self.enable_money_target_button.opacity = self.opacity
                self.enable_money_target_button.on_activate()
            else:
                self.enable_money_target_button.on_deactivate(instant=True)

    def on_update_opacity(self, new_opacity):
        """
        Updates cell opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.locked_label.delete()
            self.title_label.delete()
            self.level_required_label.delete()
            self.previous_entity_required_label.delete()
            if self.environment_required_label is not None:
                self.environment_required_label.delete()

            self.unlock_available_label.delete()
            self.under_construction_days_label.delete()
            self.under_construction_hours_minutes_label.delete()
        else:
            self.locked_label.on_update_opacity(self.opacity)
            self.title_label.on_update_opacity(self.opacity)
            self.level_required_label.on_update_opacity(self.opacity)
            self.previous_entity_required_label.on_update_opacity(self.opacity)
            if self.environment_required_label is not None:
                self.environment_required_label.on_update_opacity(self.opacity)

            self.unlock_available_label.on_update_opacity(self.opacity)
            self.under_construction_days_label.on_update_opacity(self.opacity)
            self.under_construction_hours_minutes_label.on_update_opacity(self.opacity)
