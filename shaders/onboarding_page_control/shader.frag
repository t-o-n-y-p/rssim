#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform int onboarding_page_control_opacity = 0;
uniform ivec2 position = ivec2(0, 0);
uniform ivec2 size = ivec2(0, 0);
uniform int page_number = 0;


bool is_app_window_frame(int margin_x, int margin_y, int bottom_bar_height, int top_bar_height) {
    bool is_app_window_main_frame_border
    = (margin_x >= 0 && margin_x < size[0] / 2
       && (margin_y == 0 || margin_y == 1 || margin_y == size[1] - 2 || margin_y == size[1] - 1)
      ) || (margin_y >= 0 && margin_y < size[1]
            && (margin_x == 0 || margin_x == 1 || margin_x == size[0] / 2 - 2 || margin_x == size[0] / 2 - 1));
    bool is_app_window_frame_bar_border
    = margin_x >= 0 && margin_x < size[0] / 2
      && (margin_y == bottom_bar_height || margin_y == bottom_bar_height - 1
          || margin_y == size[1] - top_bar_height || margin_y == size[1] - top_bar_height + 1);
    bool is_bottom_bar_button_border
    = margin_y >= 0 && margin_y < size[1] / 10
      && (margin_x == bottom_bar_height || margin_x == bottom_bar_height - 1
          || margin_x == size[0] / 2 - bottom_bar_height - 1 || margin_x == size[0] / 2 - bottom_bar_height
          || margin_x == size[0] / 2 - 5 * bottom_bar_height || margin_x == size[0] / 2 - 5 * bottom_bar_height + 1
          || margin_x == size[0] / 2 - 6 * bottom_bar_height + 1
          || margin_x == size[0] / 2 - 6 * bottom_bar_height + 2);
    bool is_top_bar_button_border
    = margin_y >= size[1] - top_bar_height && margin_y < size[1]
      && (margin_x == top_bar_height - 1 || margin_x == top_bar_height - 2
          || margin_x == top_bar_height * 2 - 3 || margin_x == top_bar_height * 2 - 4
          || margin_x == size[0] / 2 - top_bar_height || margin_x == size[0] / 2 - top_bar_height + 1
          || margin_x == size[0] / 2 - top_bar_height * 2 + 2 || margin_x == size[0] / 2 - top_bar_height * 2 + 3
          || margin_x == size[0] / 2 - top_bar_height * 3 + 4 || margin_x == size[0] / 2 - top_bar_height * 3 + 5);
    bool is_map_switcher_button_border
    = (margin_x >= size[0] / 4 - top_bar_height && margin_x <= size[0] / 4 - top_bar_height + bottom_bar_height
       && (margin_y == size[1] - 3 * top_bar_height / 2 - bottom_bar_height
           || margin_y == size[1] - 3 * top_bar_height / 2 - bottom_bar_height + 1
           || margin_y == size[1] - 3 * top_bar_height / 2 - 1
           || margin_y == size[1] - 3 * top_bar_height / 2
          ) || (margin_y >= size[1] - 3 * top_bar_height / 2 - bottom_bar_height
                && margin_y <= size[1] - 3 * top_bar_height / 2
                && (margin_x == size[0] / 4 - top_bar_height || margin_x == size[0] / 4 - top_bar_height + 1
                    || margin_x == size[0] / 4 - top_bar_height + bottom_bar_height - 1
                    || margin_x == size[0] / 4 - top_bar_height + bottom_bar_height))
      ) && page_number != 2;
    return is_app_window_main_frame_border || is_app_window_frame_bar_border || is_bottom_bar_button_border
           || is_top_bar_button_border || is_map_switcher_button_border;
}

bool is_highlighted(int margin_x, int margin_y, int bottom_bar_height, int top_bar_height) {
    if (page_number == 0)
        return ((margin_x >= 2 && margin_x <= size[0] / 2 - 3
                && margin_y >= bottom_bar_height + 1 && margin_y <= size[1] - top_bar_height - 1)
               ) && !(margin_x >= size[0] / 4 - top_bar_height
                      && margin_x <= size[0] / 4 - top_bar_height + bottom_bar_height
                      && margin_y >= size[1] - 3 * top_bar_height / 2 - bottom_bar_height
                      && margin_y <= size[1] - 3 * top_bar_height / 2);
    else if (page_number == 1)
        return margin_x >= size[0] / 4 - top_bar_height + 2
               && margin_x <= size[0] / 4 - top_bar_height + bottom_bar_height - 2
               && margin_y >= size[1] - 3 * top_bar_height / 2 - bottom_bar_height + 2
               && margin_y <= size[1] - 3 * top_bar_height / 2 - 2;
    else if (page_number == 2) {
        ivec2 cell_size = ivec2(int(6.875 * bottom_bar_height), bottom_bar_height);
        int interval_between_cells = int(bottom_bar_height / 4);
        int general_height = 4 * cell_size[1] + 3 * interval_between_cells;
        ivec2 fetched_coords = ivec2(int(size[0] / 4 - cell_size[0] - interval_between_cells / 2),
                                     int(size[1] / 2 + general_height / 2 - cell_size[1] / 4 - cell_size[1] / 2));
        return (margin_x >= 2 && margin_x <= bottom_bar_height - 2
                && margin_y >= 2 && margin_y <= bottom_bar_height - 2
               ) || (margin_y >= fetched_coords[1] + 2 && margin_y <= fetched_coords[1] + cell_size[1] - 3
                     && ((margin_x >= fetched_coords[0] + cell_size[0] - cell_size[1] * 2 + 4
                          && margin_x <= fetched_coords[0] + cell_size[0] - cell_size[1] - 1
                         ) || (margin_x >= fetched_coords[0] + cell_size[0] - cell_size[1] - 2
                               && margin_x <= fetched_coords[0] + cell_size[0] - 3)
                        )
                    );
    }
    else if (page_number == 3)
        return margin_x >= bottom_bar_height + 1 && margin_x <= size[0] / 2 - 6 * bottom_bar_height
               && margin_y >= 2 && margin_y <= bottom_bar_height - 2;
    else if (page_number == 4)
        return margin_x >= size[0] / 2 - 6 * bottom_bar_height + 3
               && margin_x <= size[0] / 2 - 5 * bottom_bar_height - 1
               && margin_y >= 2 && margin_y <= bottom_bar_height - 2;
    else if (page_number == 5)
        return margin_x >= size[0] / 2 - 5 * bottom_bar_height + 2
               && margin_x <= size[0] / 2 - bottom_bar_height - 2
               && margin_y >= 2 && margin_y <= bottom_bar_height - 2;
    else if (page_number == 6)
        return margin_x >= size[0] / 2 - bottom_bar_height + 1 && margin_x <= size[0] / 2 - 3
               && margin_y >= 2 && margin_y <= bottom_bar_height - 2;
    else
        return false;
}

bool is_constructor_cell(int margin_x, int margin_y, int bottom_bar_height, int top_bar_height) {
    if (page_number == 2) {
        ivec2 cell_size = ivec2(int(6.875 * bottom_bar_height), bottom_bar_height);
        int interval_between_cells = int(bottom_bar_height / 4);
        int general_height = 4 * cell_size[1] + 3 * interval_between_cells;
        ivec2 fetched_coords = ivec2(int(size[0] / 4 - cell_size[0] - interval_between_cells / 2),
                                     int(size[1] / 2 + general_height / 2 - cell_size[1] / 4 - cell_size[1] / 2));
        bool constructor_cell_border = false;
        for (int i=0; i<2; i++)
            for (int j=0; j<4; j++)
            {
                ivec2 cell_position = ivec2(fetched_coords[0] + i * (cell_size[0] + interval_between_cells),
                                            fetched_coords[1] - j * (cell_size[1] + interval_between_cells));
                if ((margin_x >= cell_position[0] && margin_x < cell_position[0] + cell_size[0]
                     && (margin_y == cell_position[1] || margin_y == cell_position[1] + 1
                         || margin_y == cell_position[1] + cell_size[1] - 1
                         || margin_y == cell_position[1] + cell_size[1] - 2)
                    ) || (margin_y >= cell_position[1] && margin_y < cell_position[1] + cell_size[1]
                          && (margin_x == cell_position[0] || margin_x == cell_position[0] + 1
                              || margin_x == cell_position[0] + cell_size[0] - 1
                              || margin_x == cell_position[0] + cell_size[0] - 2
                              || margin_x == cell_position[0] + cell_size[0] - cell_size[1]
                              || margin_x == cell_position[0] + cell_size[0] - cell_size[1] + 1
                              || margin_x == cell_position[0] + cell_size[0] - cell_size[1] * 2 + 2
                              || margin_x == cell_position[0] + cell_size[0] - cell_size[1] * 2 + 3)
                         )
                   )
                    constructor_cell_border = true;
            }

        return constructor_cell_border;
    }
    else
        return false;
}

void main() {
    int margin_x = int(gl_FragCoord[0]) - position[0];
    int margin_y = int(gl_FragCoord[1]) - position[1];
    int bottom_bar_height = int(size[1] / 10);
    int top_bar_height = int(size[1] / 20);
    // button borders are filled with red
    if (is_app_window_frame(margin_x, margin_y, bottom_bar_height, top_bar_height)
        || is_constructor_cell(margin_x, margin_y, bottom_bar_height, top_bar_height))
        color_frag = vec4(1.0, 0.0, 0.0, float(onboarding_page_control_opacity) / 255.0);
    else if (is_highlighted(margin_x, margin_y, bottom_bar_height, top_bar_height))
        color_frag = vec4(1.0, 0.0, 0.0, float(onboarding_page_control_opacity) / 255.0 * 0.5);
    // all other pixels are transparent
    else
        color_frag = vec4(0.0);
}