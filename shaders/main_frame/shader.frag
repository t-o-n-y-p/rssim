#version 330 core
out vec4 color_frag;
layout(pixel_center_integer) in vec4 gl_FragCoord;
uniform ivec2 screen_resolution = ivec2(1280, 720);
uniform int schedule_is_activated = 0;
uniform int constructor_is_activated = 0;
uniform int game_frame_opacity = 0;
uniform int schedule_opacity = 0;
uniform int constructor_opacity = 0;
void main()
{
    int top_bar_height = 34, bottom_bar_height = 80;
    if (gl_FragCoord[0] < 2 || gl_FragCoord[0] > screen_resolution[0] - 3 || gl_FragCoord[1] < 2 || gl_FragCoord[1] > screen_resolution[1] - 3 || gl_FragCoord[1] == screen_resolution[1] - top_bar_height + 1 || gl_FragCoord[1] == screen_resolution[1] - top_bar_height)
        color_frag = vec4(1.0, 0.0, 0.0, 1.0);
  
    if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && gl_FragCoord[1] >= screen_resolution[1] - top_bar_height + 2 && gl_FragCoord[1] <= screen_resolution[1] - 3)
        color_frag = vec4(vec3(0.0), 0.94);

    if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && (gl_FragCoord[1] == bottom_bar_height - 2 || gl_FragCoord[1] == bottom_bar_height - 1))
        if (game_frame_opacity > 0)
        {
            float real_game_frame_border_opacity = float(game_frame_opacity) / 255.0;
            color_frag = vec4(1.0, 0.0, 0.0, real_game_frame_border_opacity);
        }

    if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && gl_FragCoord[1] >= 2 && gl_FragCoord[1] <= bottom_bar_height - 3)
        if (game_frame_opacity > 0)
        {
            float real_game_frame_opacity = float(game_frame_opacity) / 255.0 * 0.94;
            color_frag = vec4(vec3(0.0), real_game_frame_opacity);
        }

    if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && gl_FragCoord[1] >= bottom_bar_height && gl_FragCoord[1] <= screen_resolution[1] - top_bar_height - 1)
        if (schedule_opacity > 0 || constructor_opacity > 0)
        {
            vec4 schedule_result, constructor_result;
            float real_schedule_opacity = float(schedule_opacity) / 255.0 * 0.94;
            float real_constructor_opacity = float(constructor_opacity) / 255.0 * 0.94;
            float gradient_coeff, schedule_coeff;
            int cell_width = int(0.4296875 * float(screen_resolution[0]));
            int cell_height = int(0.0625 * float(screen_resolution[0]));
            int interval_between_cells_height = int(0.015625 * float(screen_resolution[0]));
            ivec2 top_left_cell = ivec2(cell_height, screen_resolution[1] - (top_bar_height - 1) - int(float(screen_resolution[1] - (top_bar_height + bottom_bar_height - 4) - 4 * cell_height - 3 * interval_between_cells_height + int(0.02265625 * float(screen_resolution[0])) + int(0.01171875 * float(screen_resolution[0]))) / 2.0));
            ivec2 top_right_cell = ivec2(int(0.0078125 * float(screen_resolution[0])) + int(float(screen_resolution[0]) / 2.0), top_left_cell[1]);
            if (gl_FragCoord[1] == top_left_cell[1] || gl_FragCoord[1] == top_left_cell[1] + 1)
            {
                if (gl_FragCoord[0] >= top_left_cell[0] && gl_FragCoord[0] <= top_left_cell[0] + cell_width - 1)
                {
                    gradient_coeff = (float(top_left_cell[0]) + 0.21484375 * float(screen_resolution[0]) - float(gl_FragCoord[0])) / (0.21484375 * float(screen_resolution[0]));
                    schedule_coeff = (255.0 - abs(int(gradient_coeff * gradient_coeff * gradient_coeff * 255.0))) / 255.0;
                    schedule_result = vec4(vec3(schedule_coeff), real_schedule_opacity);
                }
                else if (gl_FragCoord[0] >= top_right_cell[0] && gl_FragCoord[0] <= top_right_cell[0] + cell_width - 1)
                {
                    gradient_coeff = (float(top_right_cell[0]) + 0.21484375 * float(screen_resolution[0]) - float(gl_FragCoord[0])) / (0.21484375 * float(screen_resolution[0]));
                    schedule_coeff = (255.0 - abs(int(gradient_coeff * gradient_coeff * gradient_coeff * 255.0))) / 255.0;
                    schedule_result = vec4(vec3(schedule_coeff), real_schedule_opacity);
                }
                else
                {
                    schedule_result = vec4(vec3(0.0), real_schedule_opacity);
                }
            }
            else
                schedule_result = vec4(vec3(0.0), real_schedule_opacity);

            int is_on_cell_border = 0;
            for (int i = 0; i < 4; ++i)
            {
                int y_offset = top_left_cell[1] - i * (cell_height + interval_between_cells_height) - int(gl_FragCoord[1]);
                int x_left_offset = int(gl_FragCoord[0]) - top_left_cell[0];
                int x_right_offset = int(gl_FragCoord[0]) - top_right_cell[0];
                if (((gl_FragCoord[0] >= top_left_cell[0] && gl_FragCoord[0] <= top_left_cell[0] + cell_width - 1) || (gl_FragCoord[0] >= top_right_cell[0] && gl_FragCoord[0] <= top_right_cell[0] + cell_width - 1)) && (y_offset == 0 || y_offset == 1 || y_offset == cell_height - 1 || y_offset == cell_height - 2))
                    ++is_on_cell_border;

                if (gl_FragCoord[1] >= top_left_cell[1] - i * (cell_height + interval_between_cells_height) - (cell_height - 1) && gl_FragCoord[1] <= top_left_cell[1] - i * (cell_height + interval_between_cells_height) && (x_left_offset == 0 || x_left_offset == 1 || x_left_offset == cell_width - 1 || x_left_offset == cell_width - 2 || x_right_offset == 0 || x_right_offset == 1 || x_right_offset == cell_width - 1 || x_right_offset == cell_width - 2))
                    ++is_on_cell_border;
            }
            if (is_on_cell_border > 0)
                constructor_result = vec4(1.0, 0.0, 0.0, real_constructor_opacity);
            else
                constructor_result = vec4(vec3(0.0), real_constructor_opacity);

            if (schedule_is_activated == 1)
                color_frag = constructor_result * real_constructor_opacity + schedule_result * (1.0 - real_constructor_opacity);
            else if (constructor_is_activated == 1)
                color_frag = schedule_result * real_schedule_opacity + constructor_result * (1.0 - real_schedule_opacity);
            else
                if (constructor_opacity > schedule_opacity)
                    color_frag = schedule_result * real_schedule_opacity + constructor_result * (1.0 - real_schedule_opacity);
                else
                    color_frag = constructor_result * real_constructor_opacity + schedule_result * (1.0 - real_constructor_opacity);
        }
}