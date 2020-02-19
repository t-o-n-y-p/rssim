from logging import getLogger

from view import *
from ui import *
from ui.constructor.track_cell import TrackCell
from ui.constructor.environment_cell import EnvironmentCell
from ui.button.close_constructor_button import CloseConstructorButton
from notifications.track_unlocked_notification import TrackUnlockedNotification
from notifications.environment_unlocked_notification import EnvironmentUnlockedNotification
from notifications.environment_construction_completed_notification import EnvironmentConstructionCompletedNotification
from notifications.track_construction_completed_notification import TrackConstructionCompletedNotification
from ui.label.no_more_tracks_available_label import NoMoreTracksAvailableLabel
from ui.label.no_more_environment_available_label import NoMoreEnvironmentAvailableLabel
from ui.shader_sprite.constructor_view_shader_sprite import ConstructorViewShaderSprite


class ConstructorView(MapBaseView, ABC):
    def __init__(self, controller, map_id):
        def on_close_constructor(button):
            self.controller.fade_out_animation.on_activate()
            self.controller.parent_controller.on_close_constructor()

        def on_buy_construction_action(construction_type, row, entity_number):
            self.controller.on_put_under_construction(construction_type, entity_number)
            if self.money_target_activated and self.money_target_cell_position == [construction_type, row]:
                self.controller.on_deactivate_money_target()
                self.controller.parent_controller.parent_controller.on_update_money_target(0)

        def on_set_money_target_action(construction_type, row, entity_number):
            self.controller.on_activate_money_target(construction_type, row)
            self.controller.parent_controller.parent_controller.on_update_money_target(
                self.construction_state_matrix[construction_type][entity_number][PRICE]
            )

        def on_reset_money_target_action():
            self.controller.on_deactivate_money_target()
            self.controller.parent_controller.parent_controller.on_update_money_target(0)

        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.constructor.view'))
        self.no_more_tracks_available_placeholder_viewport = Viewport()
        self.no_more_tiers_available_placeholder_viewport = Viewport()
        self.construction_state_matrix = CONSTRUCTION_STATE_MATRIX[self.map_id]
        self.close_constructor_button = CloseConstructorButton(on_click_action=on_close_constructor,
                                                               parent_viewport=self.viewport)
        self.buttons = [self.close_constructor_button, ]
        track_cells = []
        environment_cells = []
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            track_cells.append(
                TrackCell(TRACKS, j, on_buy_construction_action, on_set_money_target_action,
                          on_reset_money_target_action, parent_viewport=self.viewport)
            )
            self.buttons.extend(track_cells[j].buttons)
            self.on_window_resize_handlers.extend(track_cells[j].on_window_resize_handlers)

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            environment_cells.append(
                EnvironmentCell(ENVIRONMENT, j, on_buy_construction_action, on_set_money_target_action,
                                on_reset_money_target_action, parent_viewport=self.viewport)
            )
            self.buttons.extend(environment_cells[j].buttons)
            self.on_window_resize_handlers.extend(environment_cells[j].on_window_resize_handlers)

        self.constructor_cells = [track_cells, environment_cells]
        USER_DB_CURSOR.execute('''SELECT money_target_activated FROM constructor WHERE map_id = ?''',
                               (self.map_id, ))
        self.money_target_activated = bool(USER_DB_CURSOR.fetchone()[0])
        USER_DB_CURSOR.execute('''SELECT money_target_cell_position FROM constructor WHERE map_id = ?''',
                               (self.map_id, ))
        self.money_target_cell_position = [int(p) for p in USER_DB_CURSOR.fetchone()[0].split(',')]
        self.shader_sprite = ConstructorViewShaderSprite(view=self)
        self.no_more_tracks_available_label \
            = NoMoreTracksAvailableLabel(parent_viewport=self.no_more_tracks_available_placeholder_viewport)
        self.no_more_tiers_available_label \
            = NoMoreEnvironmentAvailableLabel(parent_viewport=self.no_more_tiers_available_placeholder_viewport)
        self.on_window_resize_handlers.extend([
            self.shader_sprite.on_window_resize, self.no_more_tracks_available_label.on_window_resize,
            self.no_more_tiers_available_label.on_window_resize
        ])
        self.on_append_window_handlers()

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        if len(self.construction_state_matrix[TRACKS]) < CONSTRUCTOR_VIEW_TRACK_CELLS:
            self.no_more_tracks_available_label.create()

        if len(self.construction_state_matrix[ENVIRONMENT]) < CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS:
            self.no_more_tiers_available_label.create()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            self.constructor_cells[TRACKS][j].on_deactivate()

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            self.constructor_cells[ENVIRONMENT][j].on_deactivate()

    @final
    @view_is_active
    def on_update(self):
        remaining_tracks = sorted(list(self.construction_state_matrix[TRACKS].keys()))
        for j in range(min(len(remaining_tracks), CONSTRUCTOR_VIEW_TRACK_CELLS)):
            if not self.constructor_cells[TRACKS][j].is_activated:
                self.constructor_cells[TRACKS][j].on_activate()
                self.constructor_cells[TRACKS][j]\
                    .on_assign_new_data(remaining_tracks[j],
                                        self.construction_state_matrix[TRACKS][remaining_tracks[j]])
                if self.money_target_activated and self.money_target_cell_position == [TRACKS, j]:
                    self.constructor_cells[TRACKS][j].on_activate_money_target()
                else:
                    self.constructor_cells[TRACKS][j].on_deactivate_money_target()

                return

        for j in range(len(remaining_tracks), CONSTRUCTOR_VIEW_TRACK_CELLS):
            if not self.constructor_cells[TRACKS][j].is_activated:
                self.constructor_cells[TRACKS][j].on_activate()
                self.constructor_cells[TRACKS][j].on_assign_new_data(0, [])
                return

        remaining_tiers = sorted(list(self.construction_state_matrix[ENVIRONMENT].keys()))
        for j in range(min(len(remaining_tiers), CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS)):
            if not self.constructor_cells[ENVIRONMENT][j].is_activated:
                self.constructor_cells[ENVIRONMENT][j].on_activate()
                self.constructor_cells[ENVIRONMENT][j]\
                    .on_assign_new_data(remaining_tiers[j],
                                        self.construction_state_matrix[ENVIRONMENT][remaining_tiers[j]])
                if self.money_target_activated and self.money_target_cell_position == [ENVIRONMENT, j]:
                    self.constructor_cells[ENVIRONMENT][j].on_activate_money_target()
                else:
                    self.constructor_cells[ENVIRONMENT][j].on_deactivate_money_target()

                return

        for j in range(len(remaining_tiers), CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            if not self.constructor_cells[ENVIRONMENT][j].is_activated:
                self.constructor_cells[ENVIRONMENT][j].on_activate()
                self.constructor_cells[ENVIRONMENT][j].on_assign_new_data(0, [])
                return

    @final
    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.no_more_tracks_available_label.on_update_current_locale(self.current_locale)
        self.no_more_tiers_available_label.on_update_current_locale(self.current_locale)
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            self.constructor_cells[TRACKS][j].on_update_current_locale(self.current_locale)

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            self.constructor_cells[ENVIRONMENT][j].on_update_current_locale(self.current_locale)

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        super().on_window_resize(width, height)
        self.no_more_tracks_available_placeholder_viewport.x1 = self.constructor_cells[TRACKS][-1].viewport.x1
        self.no_more_tracks_available_placeholder_viewport.x2 = self.constructor_cells[TRACKS][-1].viewport.x2
        self.no_more_tracks_available_placeholder_viewport.y1 = self.constructor_cells[TRACKS][-1].viewport.y1
        if len(self.construction_state_matrix[TRACKS]) < CONSTRUCTOR_VIEW_TRACK_CELLS:
            self.no_more_tracks_available_placeholder_viewport.y2 = self.constructor_cells[TRACKS][
                len(self.construction_state_matrix[TRACKS]) - CONSTRUCTOR_VIEW_TRACK_CELLS
            ].viewport.y2
        else:
            self.no_more_tracks_available_placeholder_viewport.y2 = self.constructor_cells[TRACKS][-1].viewport.y2

        self.no_more_tiers_available_placeholder_viewport.x1 = self.constructor_cells[ENVIRONMENT][-1].viewport.x1
        self.no_more_tiers_available_placeholder_viewport.x2 = self.constructor_cells[ENVIRONMENT][-1].viewport.x2
        self.no_more_tiers_available_placeholder_viewport.y1 = self.constructor_cells[ENVIRONMENT][-1].viewport.y1
        if len(self.construction_state_matrix[ENVIRONMENT]) < CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS:
            self.no_more_tiers_available_placeholder_viewport.y2 = self.constructor_cells[TRACKS][
                len(self.construction_state_matrix[ENVIRONMENT]) - CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS
            ].viewport.y2
        else:
            self.no_more_tiers_available_placeholder_viewport.y2 = self.constructor_cells[ENVIRONMENT][-1].viewport.y2

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.no_more_tracks_available_label.on_update_opacity(self.opacity)
        self.no_more_tiers_available_label.on_update_opacity(self.opacity)
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            self.constructor_cells[TRACKS][j].on_update_opacity(self.opacity)

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            self.constructor_cells[ENVIRONMENT][j].on_update_opacity(self.opacity)

    @final
    def on_update_money(self, money):
        super().on_update_money(money)
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            self.constructor_cells[TRACKS][j].on_update_money(money)

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            self.constructor_cells[ENVIRONMENT][j].on_update_money(money)

    @final
    def on_update_construction_state(self, construction_type, entity_number):
        if construction_type == TRACKS:
            remaining_tracks = sorted(list(self.construction_state_matrix[TRACKS].keys()))
            if remaining_tracks.index(entity_number) < CONSTRUCTOR_VIEW_TRACK_CELLS:
                self.constructor_cells[construction_type][remaining_tracks.index(entity_number)].on_update_state()

        elif construction_type == ENVIRONMENT:
            remaining_tiers = sorted(list(self.construction_state_matrix[ENVIRONMENT].keys()))
            if remaining_tiers.index(entity_number) < CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS:
                self.constructor_cells[construction_type][remaining_tiers.index(entity_number)].on_update_state()

    @final
    @view_is_active
    def on_unlock_construction(self, construction_type, entity_number):
        if self.money_target_activated and self.money_target_cell_position[0] == construction_type \
                and self.money_target_cell_position[1] > 0:
            self.money_target_cell_position[1] -= 1

        if construction_type == TRACKS:
            remaining_tracks = sorted(list(self.construction_state_matrix[TRACKS].keys()))
            remaining_tracks.remove(entity_number)
            for j in range(min(len(remaining_tracks), CONSTRUCTOR_VIEW_TRACK_CELLS)):
                self.constructor_cells[TRACKS][j] \
                    .on_assign_new_data(remaining_tracks[j],
                                        self.construction_state_matrix[TRACKS][remaining_tracks[j]])
                if self.money_target_activated and self.money_target_cell_position == [TRACKS, j]:
                    self.constructor_cells[TRACKS][j].on_activate_money_target()
                else:
                    self.constructor_cells[TRACKS][j].on_deactivate_money_target()

            for j in range(len(remaining_tracks), CONSTRUCTOR_VIEW_TRACK_CELLS):
                self.constructor_cells[TRACKS][j].on_assign_new_data(0, [])

            if len(remaining_tracks) < CONSTRUCTOR_VIEW_TRACK_CELLS:
                self.no_more_tracks_available_placeholder_viewport.y2 = self.constructor_cells[TRACKS][
                    len(remaining_tracks) - CONSTRUCTOR_VIEW_TRACK_CELLS
                ].viewport.y2
                self.no_more_tracks_available_label.on_position_changed()
                self.no_more_tracks_available_label.create()

        elif construction_type == ENVIRONMENT:
            remaining_tiers = sorted(list(self.construction_state_matrix[ENVIRONMENT].keys()))
            remaining_tiers.remove(entity_number)
            for j in range(min(len(remaining_tiers), CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS)):
                self.constructor_cells[ENVIRONMENT][j] \
                    .on_assign_new_data(remaining_tiers[j],
                                        self.construction_state_matrix[ENVIRONMENT][remaining_tiers[j]])
                if self.money_target_activated and self.money_target_cell_position == [ENVIRONMENT, j]:
                    self.constructor_cells[ENVIRONMENT][j].on_activate_money_target()
                else:
                    self.constructor_cells[ENVIRONMENT][j].on_deactivate_money_target()

            for j in range(len(remaining_tiers), CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
                self.constructor_cells[ENVIRONMENT][j].on_assign_new_data(0, [])

            if len(remaining_tiers) < CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS:
                self.no_more_tiers_available_placeholder_viewport.y2 = self.constructor_cells[TRACKS][
                    len(remaining_tiers) - CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS
                ].viewport.y2
                self.no_more_tiers_available_label.on_position_changed()
                self.no_more_tiers_available_label.create()

    @final
    def on_activate_money_target(self, construction_type, row):
        self.money_target_activated = True
        self.money_target_cell_position = [construction_type, row]
        for i in range(len(self.constructor_cells)):
            for j in range(len(self.constructor_cells[i])):
                if i == construction_type and j == row:
                    self.constructor_cells[i][j].on_activate_money_target()
                else:
                    self.constructor_cells[i][j].on_deactivate_money_target()

    @final
    def on_deactivate_money_target(self):
        self.money_target_activated = False
        for i in range(len(self.constructor_cells)):
            for j in range(len(self.constructor_cells[i])):
                self.constructor_cells[i][j].on_deactivate_money_target()

    @final
    @notifications_available
    @feature_unlocked_notification_enabled
    def on_send_track_unlocked_notification(self, track):
        self.notifications.append(TrackUnlockedNotification(self.current_locale, track))

    @final
    @notifications_available
    @feature_unlocked_notification_enabled
    def on_send_environment_unlocked_notification(self, tier):
        self.notifications.append(EnvironmentUnlockedNotification(self.current_locale, tier))

    @final
    @notifications_available
    @construction_completed_notification_enabled
    def on_send_track_construction_completed_notification(self, track):
        self.notifications.append(TrackConstructionCompletedNotification(self.current_locale, track))

    @final
    @notifications_available
    @construction_completed_notification_enabled
    def on_send_environment_construction_completed_notification(self, tier):
        self.notifications.append(EnvironmentConstructionCompletedNotification(self.current_locale, tier))
