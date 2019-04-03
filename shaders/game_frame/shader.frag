/*
    Fragment shader for "main frame" rectangle. "Main frame" is responsible for UI button borders, UI background,
    and general app red border. It calculates normalized RGBA color for each pixel inside the game window.
    Input value:
        vec4 gl_FragCoord - pixel position in 3D homogeneous coordinates (from left bottom point)
    Output value:
        color_frag - calculated normalized RGBA color for the pixel
    Uniforms (all positions are in 2D Cartesian coordinates from the left bottom point):
        ivec2 screen_resolution - current resolution of the game window
        int bottom_bar_height - height of the bottom bar; is provided already calculated for performance reasons
        int game_frame_opacity - opacity of the bottom bar, its edges, and button edges
        int settings_is_activated - flag to determine if we need to draw button borders for settings screen
*/
#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform ivec2 screen_resolution = ivec2(1280, 720);
uniform int bottom_bar_height = 72;
uniform int game_frame_opacity = 0;
uniform int settings_is_activated = 0;

bool is_inside_bottom_bar_or_bar_border()
/*
    Returns "true" if pixel belongs to the bottom bar or its top border and "false" if it does not.
*/
{
    return gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3  // between app window side borders
           && gl_FragCoord[1] >= 2                                              // between bottom
           && gl_FragCoord[1] <= bottom_bar_height - 1;                         // and (including) top borders
}

bool is_bottom_bar_border()
/*
    Returns "true" if pixel belongs to the bottom bar top border and "false" if it does not.
*/
{
    return gl_FragCoord[1] == bottom_bar_height - 2 || gl_FragCoord[1] == bottom_bar_height - 1;
}

bool is_bottom_bar_button_border()
/*
    Returns "true" if pixel belongs to the bottom bar button borders and "false" if it does not.
*/
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

bool is_accept_reject_settings_button_border()
/*
    Returns "true" if pixel belongs to the accept/reject buttons borders and "false" if it does not.
*/
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

void main()
/*
    MAIN SHADER FUNCTION
    Calculates intermediate color for all possible cases and mixes it
*/
{
    float bottom_bar_opacity = 0.94;
    // calculate bottom bar color using game frame opacity and settings state
    if (is_inside_bottom_bar_or_bar_border())
    {
        vec4 game_frame_result, settings_result;
        if (game_frame_opacity > 0)
        {
            float real_game_frame_border_opacity = float(game_frame_opacity) / 255.0;
            float real_game_frame_opacity = float(game_frame_opacity) / 255.0 * bottom_bar_opacity;
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
    else
        color_frag = vec4(0.0);
}