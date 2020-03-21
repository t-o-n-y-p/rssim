from logging import getLogger

from pyshaders import from_files_names

from ui.shader_sprite import ShaderSprite
from ui import *


@final
class ConstructorViewShaderSprite(ShaderSprite):
    def __init__(self, view):
        super().__init__(logger=getLogger('root.app.game.map.constructor.view.shader_sprite'), view=view)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/constructor_view/shader.frag')

    def get_bottom_edge(self):
        return get_bottom_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2 - 1

    def get_top_edge(self):
        return 1 - get_top_bar_height(self.screen_resolution) / self.screen_resolution[1] * 2

    def set_uniforms(self):
        self.shader.uniforms.screen_resolution = self.screen_resolution
        self.shader.uniforms.constructor_opacity = self.view.opacity
        cell_x = []
        cell_y = []
        cell_w = []
        cell_h = []
        cell_unlock_available = []
        cell_data_length = []
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            cell_x.append(self.view.constructor_cells[TRACKS][j].viewport.x1)
            cell_y.append(self.view.constructor_cells[TRACKS][j].viewport.y1)
            cell_w.append(self.view.constructor_cells[TRACKS][j].viewport.x2
                          - self.view.constructor_cells[TRACKS][j].viewport.x1)
            cell_h.append(self.view.constructor_cells[TRACKS][j].viewport.y2
                          - self.view.constructor_cells[TRACKS][j].viewport.y1)
            if self.view.constructor_cells[TRACKS][j].data is not None:
                if len(self.view.constructor_cells[TRACKS][j].data) > 0:
                    cell_unlock_available.append(self.view.constructor_cells[TRACKS][j].data[UNLOCK_AVAILABLE])
                else:
                    cell_unlock_available.append(FALSE)
            else:
                cell_unlock_available.append(FALSE)

            cell_data_length.append(len(self.view.constructor_cells[TRACKS][j].data))

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            cell_x.append(self.view.constructor_cells[ENVIRONMENT][j].viewport.x1)
            cell_y.append(self.view.constructor_cells[ENVIRONMENT][j].viewport.y1)
            cell_w.append(self.view.constructor_cells[ENVIRONMENT][j].viewport.x2
                          - self.view.constructor_cells[ENVIRONMENT][j].viewport.x1)
            cell_h.append(self.view.constructor_cells[ENVIRONMENT][j].viewport.y2
                          - self.view.constructor_cells[ENVIRONMENT][j].viewport.y1)
            if self.view.constructor_cells[ENVIRONMENT][j].data is not None:
                if len(self.view.constructor_cells[ENVIRONMENT][j].data) > 0:
                    cell_unlock_available.append(
                        self.view.constructor_cells[ENVIRONMENT][j].data[UNLOCK_AVAILABLE]
                    )
                else:
                    cell_unlock_available.append(FALSE)
            else:
                cell_unlock_available.append(FALSE)

            cell_data_length.append(len(self.view.constructor_cells[ENVIRONMENT][j].data))

        self.shader.uniforms.cell_x = cell_x
        self.shader.uniforms.cell_y = cell_y
        self.shader.uniforms.cell_w = cell_w
        self.shader.uniforms.cell_h = cell_h
        self.shader.uniforms.cell_unlock_available = cell_unlock_available
        self.shader.uniforms.number_of_cells = CONSTRUCTOR_VIEW_TRACK_CELLS + CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS
        self.shader.uniforms.data_length = cell_data_length
