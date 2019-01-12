#version 330 core
out vec4 color_frag;
layout(pixel_center_integer) in vec4 gl_FragCoord;
uniform ivec2 screen_resolution = ivec2(1280, 720);
uniform int game_frame_opacity = 0;
uniform int schedule_opacity = 0;
uniform int constructor_opacity = 0;
uniform int settings_is_activated = 0;
uniform int zoom_buttons_activated = 1;
uniform int track_build_button_is_activated = 0;
void main()
{
    int bottom_bar_height = int(0.05625 * float(screen_resolution[0]));
    int top_bar_height = bottom_bar_height / 2;
    if (gl_FragCoord[0] < 2 || gl_FragCoord[0] > screen_resolution[0] - 3 || gl_FragCoord[1] < 2 || gl_FragCoord[1] > screen_resolution[1] - 3 || gl_FragCoord[1] == screen_resolution[1] - top_bar_height + 1 || gl_FragCoord[1] == screen_resolution[1] - top_bar_height)
        color_frag = vec4(1.0, 0.0, 0.0, 1.0);
  
    if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && gl_FragCoord[1] >= screen_resolution[1] - top_bar_height + 2 && gl_FragCoord[1] <= screen_resolution[1] - 3)
    {
        int margin = screen_resolution[0] - int(gl_FragCoord[0]);
        if (margin == top_bar_height || margin == top_bar_height - 1 || margin == top_bar_height * 2 - 2 || margin == top_bar_height * 2 - 3 || margin == top_bar_height * 3 - 4 || margin == top_bar_height * 3 - 5)
            color_frag = vec4(1.0, 0.0, 0.0, 1.0);
        else
            color_frag = vec4(vec3(0.0), 0.94);
    }

    if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && gl_FragCoord[1] >= 2 && gl_FragCoord[1] <= bottom_bar_height - 1)
    {
        vec4 game_frame_result, settings_result;
        if (game_frame_opacity > 0)
        {
            float real_game_frame_border_opacity = float(game_frame_opacity) / 255.0;
            float real_game_frame_opacity = float(game_frame_opacity) / 255.0 * 0.94;
            if (gl_FragCoord[1] == bottom_bar_height - 2 || gl_FragCoord[1] == bottom_bar_height - 1)
                game_frame_result = vec4(1.0, 0.0, 0.0, real_game_frame_border_opacity);
            else if (gl_FragCoord[1] >= 2 && gl_FragCoord[1] <= bottom_bar_height - 3)
            {
                int margin = screen_resolution[0] - int(gl_FragCoord[0]);
                int game_time_margin = int(3.5 * float(bottom_bar_height));
                if (gl_FragCoord[0] == bottom_bar_height - 1 || gl_FragCoord[0] == bottom_bar_height - 2 || margin == bottom_bar_height || margin == bottom_bar_height - 1 || margin == game_time_margin + 1 || margin == game_time_margin + 2 || margin == game_time_margin + bottom_bar_height || margin == game_time_margin + bottom_bar_height - 1 || margin == game_time_margin + 2 * bottom_bar_height - 2 || margin == game_time_margin + 2 * bottom_bar_height - 3)
                    game_frame_result = vec4(1.0, 0.0, 0.0, real_game_frame_border_opacity);
                else
                    game_frame_result = vec4(vec3(0.0), real_game_frame_opacity);
            }
        }
        else
            game_frame_result = vec4(0.0);

        if (settings_is_activated == 1)
        {
            int margin = screen_resolution[0] - int(gl_FragCoord[0]);
            if (margin == bottom_bar_height || margin == bottom_bar_height - 1 || margin == 2 * bottom_bar_height - 2 || margin == 2 * bottom_bar_height - 3 || ((gl_FragCoord[1] == bottom_bar_height - 1 || gl_FragCoord[1] == bottom_bar_height - 2) && margin > 2 && margin < 2 * bottom_bar_height - 2))
                settings_result = vec4(1.0, 0.0, 0.0, 1.0);
            else
                settings_result = vec4(0.0);
        }
        else
            settings_result = vec4(0.0);

        color_frag = game_frame_result * float(game_frame_opacity) / 255.0 + settings_result;
    }

    if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && gl_FragCoord[1] >= bottom_bar_height && gl_FragCoord[1] <= screen_resolution[1] - top_bar_height - 1)
    {
        vec4 schedule_result, constructor_result, zoom_buttons_result;
        float real_constructor_opacity = float(constructor_opacity) / 255.0 * 0.94;
        float gradient_coeff, schedule_coeff;
        int cell_height = int(0.05625 * float(screen_resolution[0]));
        int cell_width = int(6.875 * float(cell_height));
        int interval_between_cells_height = int(0.25 * float(cell_height));
        ivec2 top_left_cell = ivec2(int(float(screen_resolution[0]) / 2.0) - cell_width - int(float(interval_between_cells_height) / 2.0), screen_resolution[1] - (top_bar_height - 1) - int(float(screen_resolution[1] - (top_bar_height + bottom_bar_height - 4) - 4 * cell_height - 3 * interval_between_cells_height + int(0.02265625 * float(screen_resolution[0])) + int(0.01171875 * float(screen_resolution[0]))) / 2.0));
        ivec2 top_right_cell = ivec2(int(0.0078125 * float(screen_resolution[0])) + int(float(screen_resolution[0]) / 2.0), top_left_cell[1]);
        if (zoom_buttons_activated == 1 && ((gl_FragCoord[1] >= screen_resolution[1] - (top_bar_height - 1 + bottom_bar_height - 1) && gl_FragCoord[1] <= screen_resolution[1] - (top_bar_height - 1) && (gl_FragCoord[0] == bottom_bar_height - 1 || gl_FragCoord[0] == bottom_bar_height - 2)) || (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= bottom_bar_height - 3 && (gl_FragCoord[1] == screen_resolution[1] - (top_bar_height - 1 + bottom_bar_height - 1) || gl_FragCoord[1] == screen_resolution[1] - (top_bar_height - 1 + bottom_bar_height - 2)))))
            zoom_buttons_result = vec4(1.0, 0.0, 0.0, 1.0);
        else
            zoom_buttons_result = vec4(0.0);

        if (schedule_opacity > 0)
        {
            float real_schedule_opacity = float(schedule_opacity) / 255.0 * 0.94;
            if (gl_FragCoord[1] == top_left_cell[1] || gl_FragCoord[1] == top_left_cell[1] - 1)
            {
                if (gl_FragCoord[0] >= top_left_cell[0] && gl_FragCoord[0] <= top_left_cell[0] + cell_width - 1)
                {
                    gradient_coeff = (float(top_left_cell[0]) + float(cell_width) / 2.0 - float(gl_FragCoord[0])) / (float(cell_width) / 2.0);
                    schedule_coeff = (255.0 - abs(int(gradient_coeff * gradient_coeff * gradient_coeff * 255.0))) / 255.0;
                    schedule_result = vec4(vec3(schedule_coeff), real_schedule_opacity);
                }
                else if (gl_FragCoord[0] >= top_right_cell[0] && gl_FragCoord[0] <= top_right_cell[0] + cell_width - 1)
                {
                    gradient_coeff = (float(top_right_cell[0]) + float(cell_width) / 2.0 - float(gl_FragCoord[0])) / (float(cell_width) / 2.0);
                    schedule_coeff = (255.0 - abs(int(gradient_coeff * gradient_coeff * gradient_coeff * 255.0))) / 255.0;
                    schedule_result = vec4(vec3(schedule_coeff), real_schedule_opacity);
                }
                else
                    schedule_result = vec4(vec3(0.0), real_schedule_opacity);
            }
            else
                schedule_result = vec4(vec3(0.0), real_schedule_opacity);
        }
        else
            schedule_result = vec4(0.0);

        if (constructor_opacity > 0)
        {
            int is_on_cell_border = 0;
            for (int i = 0; i < 4; ++i)
            {
                int y_offset = top_left_cell[1] - i * (cell_height + interval_between_cells_height) - int(gl_FragCoord[1]);
                int x_left_offset = int(gl_FragCoord[0]) - top_left_cell[0];
                int x_right_offset = int(gl_FragCoord[0]) - top_right_cell[0];
                if (((gl_FragCoord[0] >= top_left_cell[0] && gl_FragCoord[0] <= top_left_cell[0] + cell_width - 1) || (gl_FragCoord[0] >= top_right_cell[0] && gl_FragCoord[0] <= top_right_cell[0] + cell_width - 1)) && (y_offset == 0 || y_offset == 1 || y_offset == cell_height - 1 || y_offset == cell_height - 2))
                    ++is_on_cell_border;

                if (gl_FragCoord[1] >= top_left_cell[1] - i * (cell_height + interval_between_cells_height) - (cell_height - 1) && gl_FragCoord[1] <= top_left_cell[1] - i * (cell_height + interval_between_cells_height) && (x_left_offset == 0 || x_left_offset == 1 || x_left_offset == cell_width - 1 || x_left_offset == cell_width - 2 || (track_build_button_is_activated == 1 && i == 0 && (x_left_offset == cell_width - cell_height || x_left_offset == cell_width - cell_height + 1)) || x_right_offset == 0 || x_right_offset == 1 || x_right_offset == cell_width - 1 || x_right_offset == cell_width - 2))
                    ++is_on_cell_border;
            }
            if (is_on_cell_border > 0)
                constructor_result = vec4(1.0, 0.0, 0.0, real_constructor_opacity);
            else
                constructor_result = vec4(vec3(0.0), real_constructor_opacity);
        }
        else
            constructor_result = vec4(0.0);

        color_frag = schedule_result * float(schedule_opacity) / 255.0 + constructor_result * float(constructor_opacity) / 255.0 + zoom_buttons_result;
    }
}