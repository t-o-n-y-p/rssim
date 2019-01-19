/*
    Fragment shader for "main frame" rectangle. "Main frame" is responsible for UI button borders, UI background,
    and general app red border. It calculates normalized RGBA color for each pixel inside the game window.
    Input value:
        vec4 gl_FragCoord - pixel position in 3D homogeneous coordinates (from left bottom point)
    Output value:
        color_frag - calculated normalized RGBA color for the pixel
    Uniforms (all positions are in 2D Cartesian coordinates from the left bottom point):
        ivec2 screen_resolution - current resolution of the game window
        ivec2 base_offset - sign-inverted game map offset; is used for viewport border on the mini-map
        int bottom_bar_height - height of the bottom bar; is provided already calculated for performance reasons
        int top_bar_height - height of the top bar; is provided already calculated for performance reasons
        ivec2 top_left_cell - position of the top left corner for the top left cell on constructor screen;
            schedule also uses it for gradient line
        ivec2 top_right_cell - position of the top left corner for the top right cell on constructor screen;
            schedule also uses it for gradient line
        int game_frame_opacity - opacity of the bottom bar, its edges, and button edges
        int schedule_opacity - opacity of the schedule screen
        int constructor_opacity - opacity of the constructor screen
        int settings_is_activated - flag to determine if we need to draw button borders for settings screen
        int zoom_buttons_activated - flag to determine if we need to draw map zoom button borders
        int track_build_button_is_activated - flag to determine if we need to draw track build button borders
        int mini_map_opacity - opacity of the mini-map
        int zoom_out_activated - flag to determine map scale; is used for viewport border on the mini-map
        ivec2 mini_map_position - position of the bottom left corner for the mini-map
        int mini_map_width - mini-map width; is provided already calculated for performance reasons
        int mini_map_height - minipmap height; is provided already calculated for performance reasons
*/
#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
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
/*
    is_general_border() function
    Returns "true" if pixel belongs to red app window border and "false" if it does not.
*/
bool is_general_border()
{
    return gl_FragCoord[0] < 2 || gl_FragCoord[0] > screen_resolution[0] - 3     // 2 pixels for left and right border
           || gl_FragCoord[1] < 2 || gl_FragCoord[1] > screen_resolution[1] - 3  // 2 pixels for bottom and top border
           || gl_FragCoord[1] == screen_resolution[1] - top_bar_height + 1       // 2 pixels for top bar border
           || gl_FragCoord[1] == screen_resolution[1] - top_bar_height;
}
/*
    is_top_bar_button_border() function
    Returns "true" if pixel belongs to any top bar button (close, iconify or fullscreen/restore) border
    and "false" if it does not.
*/
bool is_top_bar_button_border()
{
    int margin = screen_resolution[0] - int(gl_FragCoord[0]);
    return gl_FragCoord[1] >= screen_resolution[1] - top_bar_height + 2                // pixel Y is inside the top bar
           && gl_FragCoord[1] <= screen_resolution[1] - 3
           && (margin == top_bar_height || margin == top_bar_height - 1                // 2 pixels for close button
               || margin == top_bar_height * 2 - 2 || margin == top_bar_height * 2 - 3 // fullscreen/restore button
               || margin == top_bar_height * 3 - 4 || margin == top_bar_height * 3 - 5 // iconify button
              );
}
/*
    is_inside_top_bar() function
    Returns "true" if pixel belongs to the top bar excluding borders and "false" if it does not.
*/
bool is_inside_top_bar()
{
    return gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3  // between app window side borders
           && gl_FragCoord[1] >= screen_resolution[1] - top_bar_height + 2      // between bottom and top borders
           && gl_FragCoord[1] <= screen_resolution[1] - 3;
}
/*
    is_inside_bottom_bar_or_bar_border() function
    Returns "true" if pixel belongs to the bottom bar or its top border and "false" if it does not.
*/
bool is_inside_bottom_bar_or_bar_border()
{
    return gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3  // between app window side borders
           && gl_FragCoord[1] >= 2                                              // between bottom
           && gl_FragCoord[1] <= bottom_bar_height - 1;                         // and (including) top borders
}
/*
    is_bottom_bar_border() function
    Returns "true" if pixel belongs to the bottom bar top border and "false" if it does not.
*/
bool is_bottom_bar_border()
{
    return gl_FragCoord[1] == bottom_bar_height - 2 || gl_FragCoord[1] == bottom_bar_height - 1;
}
/*
    is_bottom_bar_button_border() function
    Returns "true" if pixel belongs to the bottom bar button borders and "false" if it does not.
*/
bool is_bottom_bar_button_border()
{
    int margin = screen_resolution[0] - int(gl_FragCoord[0]);
    int game_time_margin = int(3.5 * float(bottom_bar_height));
    return gl_FragCoord[0] == bottom_bar_height - 1                               // constructor button border
           || gl_FragCoord[0] == bottom_bar_height - 2
           || margin == bottom_bar_height || margin == bottom_bar_height - 1      // settings button border
           || margin == game_time_margin + 1 || margin == game_time_margin + 2    // pause/resume button right border
           || margin == game_time_margin + bottom_bar_height                      // pause/resume button left border
           || margin == game_time_margin + bottom_bar_height - 1
           || margin == game_time_margin + 2 * bottom_bar_height - 2              // schedule button border
           || margin == game_time_margin + 2 * bottom_bar_height - 3;
}
/*
    is_accept_reject_settings_button_border() function
    Returns "true" if pixel belongs to the accept/reject buttons borders and "false" if it does not.
*/
bool is_accept_reject_settings_button_border()
{
    int margin = screen_resolution[0] - int(gl_FragCoord[0]);
    return margin == bottom_bar_height || margin == bottom_bar_height - 1            // reject button side border
           || margin == 2 * bottom_bar_height - 2                                    // accept button side border
           || margin == 2 * bottom_bar_height - 3
           || ((gl_FragCoord[1] == bottom_bar_height - 1                             // top border for both buttons
                || gl_FragCoord[1] == bottom_bar_height - 2
               ) && margin > 2 && margin < 2 * bottom_bar_height - 2
              );
}
/*
    is_inside_main_part_of_the_window() function
    Returns "true" if pixel belongs to the large space between top and bottom bars and "false" if it does not.
*/
bool is_inside_main_part_of_the_window()
{
    return gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3   // between app window side borders
           && gl_FragCoord[1] >= bottom_bar_height                               // between bottom and top bars
           && gl_FragCoord[1] <= screen_resolution[1] - top_bar_height - 1;
}
/*
    is_zoom_button_border_activated() function
    Returns "true" if pixel belongs to the zoom button borders (and button is activated) and "false" if it does not.
*/
bool is_zoom_button_border_activated()
{
    return zoom_buttons_activated == 1                                                            // button activated
           && ((gl_FragCoord[1] >= screen_resolution[1] - (top_bar_height - 1 + bottom_bar_height - 1) // right border
                && gl_FragCoord[1] <= screen_resolution[1] - (top_bar_height - 1)
                && (gl_FragCoord[0] == bottom_bar_height - 1 || gl_FragCoord[0] == bottom_bar_height - 2)
               )
               || (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= bottom_bar_height - 3                    // bottom border
                   && (gl_FragCoord[1] == screen_resolution[1] - (top_bar_height - 1 + bottom_bar_height - 1)
                       || gl_FragCoord[1] == screen_resolution[1] - (top_bar_height - 1 + bottom_bar_height - 2)
                      )
                  )
              );
}
/*
    is_mini_map_border() function
    Returns "true" if pixel belongs to the mini-map borders and "false" if it does not.
*/
bool is_mini_map_border()
{
    return ((gl_FragCoord[0] == mini_map_position[0]                                        // left border
             || gl_FragCoord[0] == mini_map_position[0] + mini_map_width - 1                // right border
            ) && gl_FragCoord[1] >= mini_map_position[1]
              && gl_FragCoord[1] <= mini_map_position[1] + mini_map_height - 1
           ) || ((gl_FragCoord[1] == mini_map_position[1]                                   // bottom border
                  || gl_FragCoord[1] == mini_map_position[1] + mini_map_height - 1          // top border
                 ) && gl_FragCoord[0] >= mini_map_position[0]
                   && gl_FragCoord[0] <= mini_map_position[0] + mini_map_width - 1
                );
}
/*
    is_mini_map_border() function
    Returns "true" if pixel belongs to the mini-map viewport borders and "false" if it does not.
*/
bool is_mini_map_viewport_border()
{
    /*
        calculate viewport border positions based on map scale and mini-map position and size
        margin_left - left border X position
        margin_right - right border X position
        margin_down - bottom border Y position
        margin_up - top border Y position
    */
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
    return ((gl_FragCoord[0] - mini_map_position[0] == margin_left                  // left border in place
             || gl_FragCoord[0] - mini_map_position[0] == margin_right              // right border in place
            ) && gl_FragCoord[1] - mini_map_position[1] >= margin_down              // between top and bottom borders
              && gl_FragCoord[1] - mini_map_position[1] <= margin_up
           ) || ((gl_FragCoord[1] - mini_map_position[1] == margin_down             // top border in place
                  || gl_FragCoord[1] - mini_map_position[1] == margin_up            // bottom border in place
                 ) && gl_FragCoord[0] - mini_map_position[0] >= margin_left         // between left and right borders
                   && gl_FragCoord[0] - mini_map_position[0] <= margin_right
                );
}
/*
    is_settings_view_button_border() function
    Returns "true" if pixel belongs to settings view buttons borders and "false" if it does not.
*/
bool is_settings_view_button_border()
{
    // medium_line - Y position of settings screen center
    int medium_line = screen_resolution[1] / 2 + top_bar_height / 2;
    // decrement_resolution_button_position - position of the bottom left corner for decrement resolution button
    ivec2 decrement_resolution_button_position = ivec2(5 * screen_resolution[0] / 32 - top_bar_height / 2,
                                                       medium_line + top_bar_height / 2);
    // increment_resolution_button_position - position of the bottom left corner for increment resolution button
    ivec2 increment_resolution_button_position = ivec2(11 * screen_resolution[0] / 32 - top_bar_height / 2,
                                                       medium_line + top_bar_height / 2);
    int settings_decrement_x_margin = int(gl_FragCoord[0]) - decrement_resolution_button_position[0];
    int settings_resolution_y_margin = int(gl_FragCoord[1]) - decrement_resolution_button_position[1];
    int settings_increment_x_margin = int(gl_FragCoord[0]) - increment_resolution_button_position[0];
    return ((settings_decrement_x_margin == 0 || settings_decrement_x_margin == 1        // 2 pixels for left border
             || settings_decrement_x_margin == top_bar_height - 2                        // 2 pixels for right border
             || settings_decrement_x_margin == top_bar_height - 1
             || settings_increment_x_margin == 0 || settings_increment_x_margin == 1     // 2 pixels for left border
             || settings_increment_x_margin == top_bar_height - 2                        // 2 pixels for right border
             || settings_increment_x_margin == top_bar_height - 1
            ) && settings_resolution_y_margin >= 0                                 // between top and bottom borders
              && settings_resolution_y_margin <= top_bar_height - 1
           ) || ((settings_resolution_y_margin == 0 || settings_resolution_y_margin == 1 // 2 pixels for bottom border
                  || settings_resolution_y_margin == top_bar_height - 2                  // 2 pixels for top border
                  || settings_resolution_y_margin == top_bar_height - 1
                 ) && ((settings_decrement_x_margin >= 0       // between top and bottom borders for decrement button
                        && settings_decrement_x_margin <= top_bar_height - 1
                       ) || (settings_increment_x_margin >= 0  // between top and bottom borders for increment button
                             && settings_increment_x_margin <= top_bar_height - 1
                            )
                      )
                );
}
/*
    is_schedule_left_line(int line_width) function
    Returns "true" if pixel belongs to the left gradient line on schedule screen and "false" if it does not.
    Input value:
        int line_width - width of the gradient line
*/
bool is_schedule_left_line(int line_width)
{
    return gl_FragCoord[0] >= top_left_cell[0] && gl_FragCoord[0] <= top_left_cell[0] + line_width - 1
           && (gl_FragCoord[1] == top_left_cell[1] || gl_FragCoord[1] == top_left_cell[1] - 1);  // 2-pixel thick line
}
/*
    is_schedule_right_line(int line_width) function
    Returns "true" if pixel belongs to the right gradient line on schedule screen and "false" if it does not.
    Input value:
        int line_width - width of the gradient line
*/
bool is_schedule_right_line(int line_width)
{
    return gl_FragCoord[0] >= top_right_cell[0] && gl_FragCoord[0] <= top_right_cell[0] + line_width - 1
           && (gl_FragCoord[1] == top_left_cell[1] || gl_FragCoord[1] == top_left_cell[1] - 1);  // 2-pixel thick line
}
/*
    is_constructor_cell_border(int cell_width, int cell_height, int interval_between_cells_height) function
    Returns "true" if pixel belongs to any cell border on constructor screen and "false" if it does not.
    Input values:
        int cell_width - width of a cell
        int cell_height - height of a cell
        int interval_between_cells_height - vertical interval between cells
*/
bool is_constructor_cell_border(int cell_width, int cell_height, int interval_between_cells_height)
{
    for (int i = 0; i < 4; ++i)  // we have 4 cells in each column; right after first match function returns "true"
    {
        int y_offset = top_left_cell[1] - i * (cell_height + interval_between_cells_height) - int(gl_FragCoord[1]);
        int x_left_offset = int(gl_FragCoord[0]) - top_left_cell[0];
        int x_right_offset = int(gl_FragCoord[0]) - top_right_cell[0];
        // top and bottom borders for the current cell (left and right)
        if (((gl_FragCoord[0] >= top_left_cell[0] && gl_FragCoord[0] <= top_left_cell[0] + cell_width - 1)
             || (gl_FragCoord[0] >= top_right_cell[0] && gl_FragCoord[0] <= top_right_cell[0] + cell_width - 1)
            ) && (y_offset == 0 || y_offset == 1 || y_offset == cell_height - 1 || y_offset == cell_height - 2)
           )
            return true;

        // left and right borders for the current cell (left and right)
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
    return false;    // if no matches were found
}
/*
    is_build_track_button_border_activated(int cell_width, int cell_height) function
    Returns "true" if pixel belongs to track build button border on constructor screen and "false" if it does not.
    Input values:
        int cell_width - width of a cell
        int cell_height - height of a cell
*/
bool is_build_track_button_border_activated(int cell_width, int cell_height)
{
    int x_left_offset = int(gl_FragCoord[0]) - top_left_cell[0];
    return gl_FragCoord[1] >= top_left_cell[1] - (cell_height - 1)       // inside the cell from bottom to top
           && gl_FragCoord[1] <= top_left_cell[1]
           && (track_build_button_is_activated == 1
               && (x_left_offset == cell_width - cell_height             // 2-pixel thick line
                   || x_left_offset == cell_width - cell_height + 1
                  )
              );
}
/*
    MAIN SHADER FUNCTION
    Calculates intermediate color for all possible cases and mixes it
*/
void main()
{
    // draw app window border and top bar border
    if (is_general_border())
        color_frag = vec4(1.0, 0.0, 0.0, 1.0);

    // fill top bar with color and draw top bar buttons borders
    if (is_inside_top_bar())
        if (is_top_bar_button_border())
            color_frag = vec4(1.0, 0.0, 0.0, 1.0);
        else
            color_frag = vec4(vec3(0.0), 0.94);

    // calculate bottom bar color using game frame opacity and settings state
    if (is_inside_bottom_bar_or_bar_border())
    {
        vec4 game_frame_result, settings_result;
        if (game_frame_opacity > 0)
        {
            float real_game_frame_border_opacity = float(game_frame_opacity) / 255.0;
            float real_game_frame_opacity = float(game_frame_opacity) / 255.0 * 0.94;
            // draw bottom bar border
            if (is_bottom_bar_border())
                game_frame_result = vec4(1.0, 0.0, 0.0, real_game_frame_border_opacity);
            else
                // draw bottom bar buttons borders
                if (is_bottom_bar_button_border())
                    game_frame_result = vec4(1.0, 0.0, 0.0, real_game_frame_border_opacity);
                // fill bottom bar with color
                else
                    game_frame_result = vec4(vec3(0.0), real_game_frame_opacity);
        }
        // just transparent if there is not bottom bar on the screen
        else
            game_frame_result = vec4(0.0);

        // draw accert/reject settings buttons borders if settings screen is activated
        if (settings_is_activated == 1 && is_accept_reject_settings_button_border())
            settings_result = vec4(1.0, 0.0, 0.0, 1.0);
        else
            settings_result = vec4(0.0);

        // mix game frame and settings results proportionally
        color_frag = game_frame_result * float(game_frame_opacity) / 255.0 + settings_result;
    }

    // calculate main part of the window using results for every possible screen
    if (is_inside_main_part_of_the_window())
    {
        vec4 schedule_result, constructor_result, zoom_buttons_result, settings_result, mini_map_result;
        float real_constructor_opacity = float(constructor_opacity) / 255.0 * 0.94;
        float gradient_coeff, schedule_coeff;
        int cell_height = int(0.05625 * float(screen_resolution[0]));
        int cell_width = int(6.875 * float(cell_height));
        int interval_between_cells_height = int(0.25 * float(cell_height));
        // draw zoom button borders
        if (is_zoom_button_border_activated())
            zoom_buttons_result = vec4(1.0, 0.0, 0.0, 1.0);
        else
            zoom_buttons_result = vec4(0.0);

        if (mini_map_opacity > 0)
        {
            float real_mini_map_opacity = float(mini_map_opacity) / 255.0;
            // draw black mini-map border
            if (is_mini_map_border())
                mini_map_result = vec4(vec3(0.0), real_mini_map_opacity);
            else
                mini_map_result = vec4(0.0);

            // draw mini-map viewport border
            if (is_mini_map_viewport_border())
                mini_map_result = vec4(1.0, 0.5, 0.0, real_mini_map_opacity);
        }
        // just transparent if there is no mini-map on the screen
        else
            mini_map_result = vec4(0.0);

        // draw all buttons on settings screen
        if (settings_is_activated == 1 && is_settings_view_button_border())
            settings_result = vec4(1.0, 0.0, 0.0, 1.0);
        // just transparent if settings screen is not activated
        else
            settings_result = vec4(0.0);

        if (schedule_opacity > 0)
        {
            float real_schedule_opacity = float(schedule_opacity) / 255.0 * 0.94;
            // draw left gradient line
            if (is_schedule_left_line(cell_width))
            {
                // distance from the line center
                gradient_coeff = (float(top_left_cell[0]) + float(cell_width) / 2.0 - float(gl_FragCoord[0]))
                / (float(cell_width) / 2.0);
                // gradient color
                schedule_coeff = (255.0 - abs(int(gradient_coeff * gradient_coeff * gradient_coeff * 255.0))) / 255.0;
                schedule_result = vec4(vec3(schedule_coeff), real_schedule_opacity);
            }
            // draw right gradient line
            else if (is_schedule_right_line(cell_width))
            {
                // distance from the line center
                gradient_coeff = (float(top_right_cell[0]) + float(cell_width) / 2.0 - float(gl_FragCoord[0]))
                / (float(cell_width) / 2.0);
                // gradient color
                schedule_coeff = (255.0 - abs(int(gradient_coeff * gradient_coeff * gradient_coeff * 255.0))) / 255.0;
                schedule_result = vec4(vec3(schedule_coeff), real_schedule_opacity);
            }
            // background color for other pixels
            else
                schedule_result = vec4(vec3(0.0), real_schedule_opacity);
        }
        // just transparent if schedule screen is not activated
        else
            schedule_result = vec4(0.0);

        if (constructor_opacity > 0)
            // draw cells and button borders on constructor screen
            if (is_constructor_cell_border(cell_width, cell_height, interval_between_cells_height)
                || is_build_track_button_border_activated(cell_width, cell_height)
               )
                constructor_result = vec4(1.0, 0.0, 0.0, real_constructor_opacity);
            // background color for other pixels
            else
                constructor_result = vec4(vec3(0.0), real_constructor_opacity);
        // just transparent if constructor screen is not activated
        else
            constructor_result = vec4(0.0);

        // mix all results proportionally
        color_frag = schedule_result * float(schedule_opacity) / 255.0
        + constructor_result * float(constructor_opacity) / 255.0
        + zoom_buttons_result + settings_result + mini_map_result * float(mini_map_opacity) / 255.0;
    }
}