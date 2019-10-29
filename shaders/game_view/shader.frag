#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform ivec2 screen_resolution = ivec2(1280, 720);
uniform int bottom_bar_height = 72;
uniform int game_frame_opacity = 0;
uniform int is_button_activated[4];
uniform int button_x[4];
uniform int button_y[4];
uniform int button_w[4];
uniform int button_h[4];
uniform int number_of_buttons = 4;

bool is_inside_bottom_bar()
{
    return gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3  // between app window side borders
           && gl_FragCoord[1] >= 2                                              // between bottom
           && gl_FragCoord[1] <= bottom_bar_height - 3;                         // and top borders
}

bool is_bottom_bar_border()
{
    return gl_FragCoord[1] == bottom_bar_height - 2 || gl_FragCoord[1] == bottom_bar_height - 1
           || gl_FragCoord[1] == 0 || gl_FragCoord[1] == 1;
}

bool is_button_border()
{
    int margin_x, margin_y;
    for(int i = 0; i < number_of_buttons; i++)
    {
        if (is_button_activated[i] == 1)
        {
            margin_x = int(gl_FragCoord[0]) - button_x[i];
            margin_y = int(gl_FragCoord[1]) - button_y[i];
            if ((margin_x >= 0 && margin_x <= button_w[i] - 1
                 && (margin_y == 0 || margin_y == 1 || margin_y == button_h[i] - 2
                     || margin_y == button_h[i] - 1)
                ) || (margin_y >= 0 && margin_y <= button_h[i] - 1
                      && (margin_x == 0 || margin_x == 1 || margin_x == button_w[i] - 2
                          || margin_x == button_w[i] - 1)
                     )
            )
                return true;
        }
    }
    return false;
}


void main()
{
    if (is_button_border() || is_bottom_bar_border())
        color_frag = vec4(1.0, 0.0, 0.0, float(game_frame_opacity) / 255.0);
    // fill bottom bar with color
    else if (is_inside_bottom_bar())
        color_frag = vec4(vec3(0.0), float(game_frame_opacity) / 255.0);
    // just transparent if there is not bottom bar on the screen
    else
        color_frag = vec4(0.0);
}