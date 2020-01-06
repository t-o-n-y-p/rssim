#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform int map_switcher_window_opacity = 0;
uniform ivec2 map_switcher_window_position = ivec2(0, 0);
uniform ivec2 map_switcher_window_size = ivec2(0, 0);
uniform int top_bar_height = 36;
uniform int is_button_activated[5];
uniform int button_x[5];
uniform int button_y[5];
uniform int button_w[5];
uniform int button_h[5];
uniform int number_of_buttons = 5;

bool is_map_switcher_window_border(int margin_x, int margin_y)
{
    bool is_side_border = margin_y >= 0 && margin_y <= map_switcher_window_size[1] - 1
         && (margin_x == 0 || margin_x == 1
             || margin_x == map_switcher_window_size[0] - 2 || margin_x == map_switcher_window_size[0] - 1);
    bool is_top_bottom_border = margin_x >= 0 && margin_x <= map_switcher_window_size[0] - 1
         && (margin_y == 0 || margin_y == 1
             || margin_y == map_switcher_window_size[1] - 2 || margin_y == map_switcher_window_size[1] - 1);
    return is_side_border || is_top_bottom_border;
}

bool is_top_bar_border(int margin_x, int margin_y)
{
    bool is_top_bar_border = margin_x >= 0 && margin_x <= map_switcher_window_size[0] - 1
                             && (margin_y == map_switcher_window_size[1] - top_bar_height
                                 || margin_y == map_switcher_window_size[1] - top_bar_height + 1);
    bool is_close_button_border = margin_y > map_switcher_window_size[1] - top_bar_height + 1
                                  && margin_y < map_switcher_window_size[1]
                                  && (margin_x == map_switcher_window_size[0] - top_bar_height
                                      || margin_x == map_switcher_window_size[0] - top_bar_height + 1);
    return is_top_bar_border || is_close_button_border;
}

bool is_inside_map_switcher_window(int margin_x, int margin_y)
{
    return margin_x >= 2 && margin_x <= map_switcher_window_size[0] - 3
           && margin_y >= 2 && margin_y <= map_switcher_window_size[1] - 3;
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
    int margin_x = int(gl_FragCoord[0]) - map_switcher_window_position[0];
    int margin_y = int(gl_FragCoord[1]) - map_switcher_window_position[1];
    // borders are filled with red
    if (is_map_switcher_window_border(margin_x, margin_y) || is_top_bar_border(margin_x, margin_y) || is_button_border())
        color_frag = vec4(1.0, 0.0, 0.0, float(map_switcher_window_opacity) / 255.0);
    else if (is_inside_map_switcher_window(margin_x, margin_y))
        color_frag = vec4(vec3(0.0), float(map_switcher_window_opacity) / 255.0);
    // all other pixels are transparent
    else
        color_frag = vec4(0.0);
}