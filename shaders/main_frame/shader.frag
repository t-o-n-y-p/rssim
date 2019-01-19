#version 330 core
out vec4 color_frag;
layout(pixel_center_integer) in vec4 gl_FragCoord;
uniform ivec2 screen_resolution = ivec2(1280, 720);
uniform ivec2 base_offset = ivec2(0, 0);
uniform int bottom_bar_height = 72;
uniform int top_bar_height = 36;
uniform ivec2 top_left_cell = ivec2(0, 0);
uniform ivec2 top_right_cell = ivec2(0, 0);
uniform int game_frame_opacity = 0;
uniform int schedule_opacity = 0;
uniform int constructor_opacity = 0;
uniform int settings_is_activated = 0;
uniform int zoom_buttons_activated = 1;
uniform int track_build_button_is_activated = 0;
uniform int mini_map_opacity = 0;
uniform int zoom_out_activated = 0;
uniform ivec2 mini_map_position = ivec2(0, 0);
uniform int mini_map_width = 0;
uniform int mini_map_height = 0;
bool is_general_border()
{
    return gl_FragCoord[0] < 2 || gl_FragCoord[0] > screen_resolution[0] - 3
           || gl_FragCoord[1] < 2 || gl_FragCoord[1] > screen_resolution[1] - 3
           || gl_FragCoord[1] == screen_resolution[1] - top_bar_height + 1
           || gl_FragCoord[1] == screen_resolution[1] - top_bar_height;
}
bool is_top_bar_button_border()
{
    int margin = screen_resolution[0] - int(gl_FragCoord[0]);
    return gl_FragCoord[1] >= screen_resolution[1] - top_bar_height + 2 && gl_FragCoord[1] <= screen_resolution[1] - 3
           && (margin == top_bar_height || margin == top_bar_height - 1
               || margin == top_bar_height * 2 - 2 || margin == top_bar_height * 2 - 3
               || margin == top_bar_height * 3 - 4 || margin == top_bar_height * 3 - 5
              );
}
bool is_inside_top_bar()
{
    return gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3
           && gl_FragCoord[1] >= screen_resolution[1] - top_bar_height + 2
           && gl_FragCoord[1] <= screen_resolution[1] - 3;
}
bool is_inside_bottom_bar_or_bar_border()
{
    return gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3
           && gl_FragCoord[1] >= 2 && gl_FragCoord[1] <= bottom_bar_height - 1;
}
bool is_bottom_bar_border()
{
    return gl_FragCoord[1] == bottom_bar_height - 2 || gl_FragCoord[1] == bottom_bar_height - 1;
}
bool is_bottom_bar_button_border()
{
    int margin = screen_resolution[0] - int(gl_FragCoord[0]);
    int game_time_margin = int(3.5 * float(bottom_bar_height));
    return gl_FragCoord[0] == bottom_bar_height - 1 || gl_FragCoord[0] == bottom_bar_height - 2
           || margin == bottom_bar_height || margin == bottom_bar_height - 1
           || margin == game_time_margin + 1 || margin == game_time_margin + 2
           || margin == game_time_margin + bottom_bar_height || margin == game_time_margin + bottom_bar_height - 1
           || margin == game_time_margin + 2 * bottom_bar_height - 2
           || margin == game_time_margin + 2 * bottom_bar_height - 3;
}
bool is_accept_reject_settings_button_border()
{
    int margin = screen_resolution[0] - int(gl_FragCoord[0]);
    return margin == bottom_bar_height || margin == bottom_bar_height - 1
           || margin == 2 * bottom_bar_height - 2 || margin == 2 * bottom_bar_height - 3
           || ((gl_FragCoord[1] == bottom_bar_height - 1 || gl_FragCoord[1] == bottom_bar_height - 2)
               && margin > 2 && margin < 2 * bottom_bar_height - 2
              );
}
bool is_inside_main_part_of_the_window()
{
    return gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3
           && gl_FragCoord[1] >= bottom_bar_height && gl_FragCoord[1] <= screen_resolution[1] - top_bar_height - 1;
}
bool is_zoom_button_border_activated()
{
    return zoom_buttons_activated == 1
           && ((gl_FragCoord[1] >= screen_resolution[1] - (top_bar_height - 1 + bottom_bar_height - 1)
                && gl_FragCoord[1] <= screen_resolution[1] - (top_bar_height - 1)
                && (gl_FragCoord[0] == bottom_bar_height - 1 || gl_FragCoord[0] == bottom_bar_height - 2)
               )
               || (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= bottom_bar_height - 3
                   && (gl_FragCoord[1] == screen_resolution[1] - (top_bar_height - 1 + bottom_bar_height - 1)
                       || gl_FragCoord[1] == screen_resolution[1] - (top_bar_height - 1 + bottom_bar_height - 2)
                      )
                  )
              );
}
bool is_mini_map_border()
{
    return ((gl_FragCoord[0] == mini_map_position[0] || gl_FragCoord[0] == mini_map_position[0] + mini_map_width - 1)
            && gl_FragCoord[1] >= mini_map_position[1]
            && gl_FragCoord[1] <= mini_map_position[1] + mini_map_height - 1
           ) || ((gl_FragCoord[1] == mini_map_position[1]
                  || gl_FragCoord[1] == mini_map_position[1] + mini_map_height - 1
                 ) && gl_FragCoord[0] >= mini_map_position[0]
                   && gl_FragCoord[0] <= mini_map_position[0] + mini_map_width - 1
                );
}
bool is_mini_map_viewport_border()
{
    int margin_left, margin_right, margin_down, margin_up;
    if (zoom_out_activated == 1)
    {
        margin_left = int(float(base_offset[0]) / 4096.0 * mini_map_width);
        margin_right = margin_left + int(float(screen_resolution[0] - 1) / 4096.0 * mini_map_width);
        margin_down = int(float(base_offset[1]) / 2048.0 * mini_map_height);
        margin_up = margin_down + int(float(screen_resolution[1] - 1) / 2048.0 * mini_map_height);
    }
    else
    {
        margin_left = int(float(base_offset[0]) / 8192.0 * mini_map_width);
        margin_right = margin_left + int(float(screen_resolution[0] - 1) / 8192.0 * mini_map_width);
        margin_down = int(float(base_offset[1]) / 4096.0 * mini_map_height);
        margin_up = margin_down + int(float(screen_resolution[1] - 1) / 4096.0 * mini_map_height);
    }
    return ((gl_FragCoord[0] - mini_map_position[0] == margin_left
             || gl_FragCoord[0] - mini_map_position[0] == margin_right
            ) && gl_FragCoord[1] - mini_map_position[1] >= margin_down
              && gl_FragCoord[1] - mini_map_position[1] <= margin_up
           ) || ((gl_FragCoord[1] - mini_map_position[1] == margin_down
                  || gl_FragCoord[1] - mini_map_position[1] == margin_up
                 ) && gl_FragCoord[0] - mini_map_position[0] >= margin_left
                   && gl_FragCoord[0] - mini_map_position[0] <= margin_right
                );
}
bool is_setings_view_button_border()
{
    int medium_line = screen_resolution[1] / 2 + top_bar_height / 2;
    ivec2 decrement_resolution_button_position = ivec2(5 * screen_resolution[0] / 32 - top_bar_height / 2,
                                                       medium_line + top_bar_height / 2);
    ivec2 increment_resolution_button_position = ivec2(11 * screen_resolution[0] / 32 - top_bar_height / 2,
                                                       medium_line + top_bar_height / 2);
    int settings_decrement_x_margin = int(gl_FragCoord[0]) - decrement_resolution_button_position[0];
    int settings_resolution_y_margin = int(gl_FragCoord[1]) - decrement_resolution_button_position[1];
    int settings_increment_x_margin = int(gl_FragCoord[0]) - increment_resolution_button_position[0];
    return ((settings_decrement_x_margin == 0 || settings_decrement_x_margin == 1
             || settings_decrement_x_margin == top_bar_height - 2
             || settings_decrement_x_margin == top_bar_height - 1
             || settings_increment_x_margin == 0 || settings_increment_x_margin == 1
             || settings_increment_x_margin == top_bar_height - 2
             || settings_increment_x_margin == top_bar_height - 1
            ) && settings_resolution_y_margin >= 0 && settings_resolution_y_margin <= top_bar_height - 1
           ) || ((settings_resolution_y_margin == 0 || settings_resolution_y_margin == 1
                  || settings_resolution_y_margin == top_bar_height - 2
                  || settings_resolution_y_margin == top_bar_height - 1
                 ) && ((settings_decrement_x_margin >= 0 && settings_decrement_x_margin <= top_bar_height - 1)
                       || (settings_increment_x_margin >= 0 && settings_increment_x_margin <= top_bar_height - 1)
                      )
                );
}
bool is_schedule_left_line(int cell_width)
{
    return gl_FragCoord[0] >= top_left_cell[0] && gl_FragCoord[0] <= top_left_cell[0] + cell_width - 1
           && (gl_FragCoord[1] == top_left_cell[1] || gl_FragCoord[1] == top_left_cell[1] - 1);
}
bool is_schedule_right_line(int cell_width)
{
    return gl_FragCoord[0] >= top_right_cell[0] && gl_FragCoord[0] <= top_right_cell[0] + cell_width - 1
           && (gl_FragCoord[1] == top_left_cell[1] || gl_FragCoord[1] == top_left_cell[1] - 1);
}
bool is_constructor_cell_border(int cell_width, int cell_height, int interval_between_cells_height)
{
    for (int i = 0; i < 4; ++i)
    {
        int y_offset = top_left_cell[1] - i * (cell_height + interval_between_cells_height) - int(gl_FragCoord[1]);
        int x_left_offset = int(gl_FragCoord[0]) - top_left_cell[0];
        int x_right_offset = int(gl_FragCoord[0]) - top_right_cell[0];
        if (((gl_FragCoord[0] >= top_left_cell[0] && gl_FragCoord[0] <= top_left_cell[0] + cell_width - 1)
             || (gl_FragCoord[0] >= top_right_cell[0] && gl_FragCoord[0] <= top_right_cell[0] + cell_width - 1)
            ) && (y_offset == 0 || y_offset == 1 || y_offset == cell_height - 1 || y_offset == cell_height - 2)
           )
            return true;

        if (gl_FragCoord[1] >= top_left_cell[1] - i * (cell_height + interval_between_cells_height) - (cell_height - 1)
            && gl_FragCoord[1] <= top_left_cell[1] - i * (cell_height + interval_between_cells_height)
            && (x_left_offset == 0 || x_left_offset == 1
                || x_left_offset == cell_width - 1 || x_left_offset == cell_width - 2
                || x_right_offset == 0 || x_right_offset == 1
                || x_right_offset == cell_width - 1 || x_right_offset == cell_width - 2
               )
           )
            return true;
    }
    return false;
}
bool is_build_track_button_border_activated(int cell_width, int cell_height, int interval_between_cells_height)
{
    int x_left_offset = int(gl_FragCoord[0]) - top_left_cell[0];
    return gl_FragCoord[1] >= top_left_cell[1] - (cell_height - 1) && gl_FragCoord[1] <= top_left_cell[1]
           && (track_build_button_is_activated == 1
               && (x_left_offset == cell_width - cell_height || x_left_offset == cell_width - cell_height + 1)
              );
}
void main()
{
    if (is_general_border())
        color_frag = vec4(1.0, 0.0, 0.0, 1.0);
  
    if (is_inside_top_bar())
        if (is_top_bar_button_border())
            color_frag = vec4(1.0, 0.0, 0.0, 1.0);
        else
            color_frag = vec4(vec3(0.0), 0.94);

    if (is_inside_bottom_bar_or_bar_border())
    {
        vec4 game_frame_result, settings_result;
        if (game_frame_opacity > 0)
        {
            float real_game_frame_border_opacity = float(game_frame_opacity) / 255.0;
            float real_game_frame_opacity = float(game_frame_opacity) / 255.0 * 0.94;
            if (is_bottom_bar_border())
                game_frame_result = vec4(1.0, 0.0, 0.0, real_game_frame_border_opacity);
            else
                if (is_bottom_bar_button_border())
                    game_frame_result = vec4(1.0, 0.0, 0.0, real_game_frame_border_opacity);
                else
                    game_frame_result = vec4(vec3(0.0), real_game_frame_opacity);
        }
        else
            game_frame_result = vec4(0.0);

        if (settings_is_activated == 1)
            if (is_accept_reject_settings_button_border())
                settings_result = vec4(1.0, 0.0, 0.0, 1.0);
            else
                settings_result = vec4(0.0);
        else
            settings_result = vec4(0.0);

        color_frag = game_frame_result * float(game_frame_opacity) / 255.0 + settings_result;
    }

    if (is_inside_main_part_of_the_window())
    {
        vec4 schedule_result, constructor_result, zoom_buttons_result, settings_result, mini_map_result;
        float real_constructor_opacity = float(constructor_opacity) / 255.0 * 0.94;
        float gradient_coeff, schedule_coeff;
        int cell_height = int(0.05625 * float(screen_resolution[0]));
        int cell_width = int(6.875 * float(cell_height));
        int interval_between_cells_height = int(0.25 * float(cell_height));
        if (is_zoom_button_border_activated())
            zoom_buttons_result = vec4(1.0, 0.0, 0.0, 1.0);
        else
            zoom_buttons_result = vec4(0.0);

        if (mini_map_opacity > 0)
        {
            float real_mini_map_opacity = float(mini_map_opacity) / 255.0;
            if (is_mini_map_border())
                mini_map_result = vec4(vec3(0.0), real_mini_map_opacity);
            else
                mini_map_result = vec4(0.0);

            if (is_mini_map_viewport_border())
                mini_map_result = vec4(1.0, 0.5, 0.0, real_mini_map_opacity);
        }
        else
            mini_map_result = vec4(0.0);

        if (settings_is_activated == 1 && is_setings_view_button_border())
            settings_result = vec4(1.0, 0.0, 0.0, 1.0);
        else
            settings_result = vec4(0.0);

        if (schedule_opacity > 0)
        {
            float real_schedule_opacity = float(schedule_opacity) / 255.0 * 0.94;
            if (is_schedule_left_line(cell_width))
            {
                gradient_coeff = (float(top_left_cell[0]) + float(cell_width) / 2.0 - float(gl_FragCoord[0]))
                / (float(cell_width) / 2.0);
                schedule_coeff = (255.0 - abs(int(gradient_coeff * gradient_coeff * gradient_coeff * 255.0))) / 255.0;
                schedule_result = vec4(vec3(schedule_coeff), real_schedule_opacity);
            }
            else if (is_schedule_right_line(cell_width))
            {
                gradient_coeff = (float(top_right_cell[0]) + float(cell_width) / 2.0 - float(gl_FragCoord[0]))
                / (float(cell_width) / 2.0);
                schedule_coeff = (255.0 - abs(int(gradient_coeff * gradient_coeff * gradient_coeff * 255.0))) / 255.0;
                schedule_result = vec4(vec3(schedule_coeff), real_schedule_opacity);
            }
            else
                schedule_result = vec4(vec3(0.0), real_schedule_opacity);
        }
        else
            schedule_result = vec4(0.0);

        if (constructor_opacity > 0)
            if (is_constructor_cell_border(cell_width, cell_height, interval_between_cells_height)
                || is_build_track_button_border_activated(cell_width, cell_height, interval_between_cells_height)
               )
                constructor_result = vec4(1.0, 0.0, 0.0, real_constructor_opacity);
            else
                constructor_result = vec4(vec3(0.0), real_constructor_opacity);
        else
            constructor_result = vec4(0.0);

        color_frag = schedule_result * float(schedule_opacity) / 255.0
        + constructor_result * float(constructor_opacity) / 255.0
        + zoom_buttons_result + settings_result + mini_map_result * float(mini_map_opacity) / 255.0;
    }
}