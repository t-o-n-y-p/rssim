from logging import getLogger

from ui.constructor_placeholder_container.constructor_environment_placeholder_container import \
    ConstructorEnvironmentPlaceholderContainer
from ui.constructor_placeholder_container.constructor_track_placeholder_container import \
    ConstructorTrackPlaceholderContainer
from view import *
from ui import *
from ui.constructor_cell.track_cell import TrackCell
from ui.constructor_cell.environment_cell import EnvironmentCell
from ui.button.close_constructor_button import CloseConstructorButton
from notifications.track_unlocked_notification import TrackUnlockedNotification
from notifications.environment_unlocked_notification import EnvironmentUnlockedNotification
from notifications.environment_construction_completed_notification import EnvironmentConstructionCompletedNotification
from notifications.track_construction_completed_notification import TrackConstructionCompletedNotification
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
                CONSTRUCTION_STATE_MATRIX[self.map_id][construction_type][entity_number][PRICE]
            )

        def on_reset_money_target_action():
            self.controller.on_deactivate_money_target()
            self.controller.parent_controller.parent_controller.on_update_money_target(0)

        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.constructor.view'))
        self.close_constructor_button = CloseConstructorButton(
            on_click_action=on_close_constructor, parent_viewport=self.viewport
        )
        self.buttons = [self.close_constructor_button, ]
        track_cells = []
        environment_cells = []
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            track_cells.append(
                TrackCell(
                    TRACKS, j, on_buy_construction_action, on_set_money_target_action,
                    on_reset_money_target_action, parent_viewport=self.viewport
                )
            )
            self.buttons.extend(track_cells[j].buttons)
            self.on_window_resize_handlers.extend(track_cells[j].on_window_resize_handlers)

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            environment_cells.append(
                EnvironmentCell(
                    ENVIRONMENT, j, on_buy_construction_action, on_set_money_target_action,
                    on_reset_money_target_action, parent_viewport=self.viewport
                )
            )
            self.buttons.extend(environment_cells[j].buttons)
            self.on_window_resize_handlers.extend(environment_cells[j].on_window_resize_handlers)

        self.constructor_cells = [track_cells, environment_cells]
        USER_DB_CURSOR.execute(
            '''SELECT money_target_activated FROM constructor WHERE map_id = ?''', (self.map_id, )
        )
        self.money_target_activated = USER_DB_CURSOR.fetchone()[0]
        USER_DB_CURSOR.execute(
            '''SELECT money_target_cell_position FROM constructor WHERE map_id = ?''', (self.map_id, )
        )
        self.money_target_cell_position = [int(p) for p in USER_DB_CURSOR.fetchone()[0].split(',')]
        self.shader_sprite = ConstructorViewShaderSprite(view=self)
        self.constructor_track_placeholder_container = ConstructorTrackPlaceholderContainer(
            bottom_parent_viewport=self.constructor_cells[TRACKS][-1].viewport,
            top_parent_viewport=self.constructor_cells[TRACKS][-1].viewport
        )
        self.constructor_environment_placeholder_container = ConstructorEnvironmentPlaceholderContainer(
            bottom_parent_viewport=self.constructor_cells[ENVIRONMENT][-1].viewport,
            top_parent_viewport=self.constructor_cells[ENVIRONMENT][-1].viewport
        )
        self.on_window_resize_handlers.extend(
            [
                self.shader_sprite.on_window_resize,
                *self.constructor_track_placeholder_container.on_window_resize_handlers,
                *self.constructor_environment_placeholder_container.on_window_resize_handlers
            ]
        )
        self.on_append_window_handlers()

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        if len(CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS]) < CONSTRUCTOR_VIEW_TRACK_CELLS:
            self.constructor_track_placeholder_container.on_activate()

        if len(CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT]) < CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS:
            self.constructor_environment_placeholder_container.on_activate()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        self.constructor_track_placeholder_container.on_deactivate()
        self.constructor_environment_placeholder_container.on_deactivate()
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            self.constructor_cells[TRACKS][j].on_deactivate()

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            self.constructor_cells[ENVIRONMENT][j].on_deactivate()

    @final
    @view_is_active
    def on_update(self):
        remaining_tracks = sorted(list(CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS].keys()))
        for j in range(min(len(remaining_tracks), CONSTRUCTOR_VIEW_TRACK_CELLS)):
            if not self.constructor_cells[TRACKS][j].is_activated:
                self.constructor_cells[TRACKS][j].on_activate()
                self.constructor_cells[TRACKS][j].on_assign_new_data(
                    remaining_tracks[j], CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][remaining_tracks[j]]
                )
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

        remaining_tiers = sorted(list(CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT].keys()))
        for j in range(min(len(remaining_tiers), CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS)):
            if not self.constructor_cells[ENVIRONMENT][j].is_activated:
                self.constructor_cells[ENVIRONMENT][j].on_activate()
                self.constructor_cells[ENVIRONMENT][j].on_assign_new_data(
                    remaining_tiers[j], CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][remaining_tiers[j]]
                )
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
        self.constructor_track_placeholder_container.on_update_current_locale(self.current_locale)
        self.constructor_environment_placeholder_container.on_update_current_locale(self.current_locale)
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            self.constructor_cells[TRACKS][j].on_update_current_locale(self.current_locale)

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            self.constructor_cells[ENVIRONMENT][j].on_update_current_locale(self.current_locale)

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.constructor_track_placeholder_container.on_update_opacity(self.opacity)
        self.constructor_environment_placeholder_container.on_update_opacity(self.opacity)
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
            remaining_tracks = sorted(list(CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS].keys()))
            if remaining_tracks.index(entity_number) < CONSTRUCTOR_VIEW_TRACK_CELLS:
                self.constructor_cells[construction_type][remaining_tracks.index(entity_number)].on_update_state()

        elif construction_type == ENVIRONMENT:
            remaining_tiers = sorted(list(CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT].keys()))
            if remaining_tiers.index(entity_number) < CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS:
                self.constructor_cells[construction_type][remaining_tiers.index(entity_number)].on_update_state()

    @final
    @view_is_active
    def on_unlock_construction(self, construction_type, entity_number):
        if self.money_target_activated and self.money_target_cell_position[0] == construction_type \
                and self.money_target_cell_position[1] > 0:
            self.money_target_cell_position[1] -= 1

        if construction_type == TRACKS:
            remaining_tracks = sorted(list(CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS].keys()))
            remaining_tracks.remove(entity_number)
            for j in range(min(len(remaining_tracks), CONSTRUCTOR_VIEW_TRACK_CELLS)):
                self.constructor_cells[TRACKS][j].on_assign_new_data(
                    remaining_tracks[j], CONSTRUCTION_STATE_MATRIX[self.map_id][TRACKS][remaining_tracks[j]]
                )
                if self.money_target_activated and self.money_target_cell_position == [TRACKS, j]:
                    self.constructor_cells[TRACKS][j].on_activate_money_target()
                else:
                    self.constructor_cells[TRACKS][j].on_deactivate_money_target()

            for j in range(len(remaining_tracks), CONSTRUCTOR_VIEW_TRACK_CELLS):
                self.constructor_cells[TRACKS][j].on_assign_new_data(0, [])

            if len(remaining_tracks) < CONSTRUCTOR_VIEW_TRACK_CELLS:
                self.constructor_track_placeholder_container.on_update_top_parent_viewport(
                    self.constructor_cells[TRACKS][len(remaining_tracks) - CONSTRUCTOR_VIEW_TRACK_CELLS].viewport
                )
                self.constructor_track_placeholder_container.on_activate()

        elif construction_type == ENVIRONMENT:
            remaining_tiers = sorted(list(CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT].keys()))
            remaining_tiers.remove(entity_number)
            for j in range(min(len(remaining_tiers), CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS)):
                self.constructor_cells[ENVIRONMENT][j].on_assign_new_data(
                    remaining_tiers[j], CONSTRUCTION_STATE_MATRIX[self.map_id][ENVIRONMENT][remaining_tiers[j]]
                )
                if self.money_target_activated and self.money_target_cell_position == [ENVIRONMENT, j]:
                    self.constructor_cells[ENVIRONMENT][j].on_activate_money_target()
                else:
                    self.constructor_cells[ENVIRONMENT][j].on_deactivate_money_target()

            for j in range(len(remaining_tiers), CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
                self.constructor_cells[ENVIRONMENT][j].on_assign_new_data(0, [])

            if len(remaining_tiers) < CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS:
                self.constructor_environment_placeholder_container.on_update_top_parent_viewport(
                    self.constructor_cells[ENVIRONMENT][
                        len(remaining_tiers) - CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS
                    ].viewport
                )
                self.constructor_environment_placeholder_container.on_activate()

    @final
    def on_activate_money_target(self, construction_type, row):
        self.money_target_activated = TRUE
        self.money_target_cell_position = [construction_type, row]
        for i in range(len(self.constructor_cells)):
            for j in range(len(self.constructor_cells[i])):
                if i == construction_type and j == row:
                    self.constructor_cells[i][j].on_activate_money_target()
                else:
                    self.constructor_cells[i][j].on_deactivate_money_target()

    @final
    def on_deactivate_money_target(self):
        self.money_target_activated = FALSE
        for i in range(len(self.constructor_cells)):
            for j in range(len(self.constructor_cells[i])):
                self.constructor_cells[i][j].on_deactivate_money_target()

    @final
    @game_progress_notifications_available
    @feature_unlocked_notification_enabled
    def on_send_track_unlocked_notification(self, track):
        self.game_progress_notifications.append(TrackUnlockedNotification(self.current_locale, self.map_id, track))

    @final
    @game_progress_notifications_available
    @feature_unlocked_notification_enabled
    def on_send_environment_unlocked_notification(self, tier):
        self.game_progress_notifications.append(EnvironmentUnlockedNotification(self.current_locale, self.map_id, tier))

    @final
    @game_progress_notifications_available
    @construction_completed_notification_enabled
    def on_send_track_construction_completed_notification(self, track):
        self.game_progress_notifications.append(
            TrackConstructionCompletedNotification(self.current_locale, self.map_id, track)
        )

    @final
    @game_progress_notifications_available
    @construction_completed_notification_enabled
    def on_send_environment_construction_completed_notification(self, tier):
        self.game_progress_notifications.append(
            EnvironmentConstructionCompletedNotification(self.current_locale, self.map_id, tier)
        )
