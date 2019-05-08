/*
    Fragment shader for onboarding view.
    Input value:
        vec4 gl_FragCoord - pixel position in 3D homogeneous coordinates (from left bottom point)
    Output value:
        color_frag - calculated normalized RGBA color for the pixel
    Uniforms (all positions are in 2D Cartesian coordinates from the left bottom point):
        int onboarding_opacity - opacity of license screen
        int is_button_activated[] - indicates if button with given index is activated
        int button_x[] - X position of button with given index
        int button_y[] - Y position of button with given index
        int button_w[] - width of button with given index
        int button_h[] - height of button with given index
        int number_of_buttons - number of buttons on the screen
*/
#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform int onboarding_opacity = 0;
uniform int is_button_activated[3];
uniform int button_x[3];
uniform int button_y[3];
uniform int button_w[3];
uniform int button_h[3];
uniform int number_of_buttons = 3;
uniform ivec2 position = ivec2(0, 0);
uniform ivec2 size = ivec2(0, 0);
uniform int page_number = 0;


bool is_app_window_frame(int margin_x, int margin_y, int bottom_bar_height, int top_bar_height)
{
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
          || margin_x == size[0] / 2 - 4 * bottom_bar_height - 1 || margin_x == size[0] / 2 - 4 * bottom_bar_height
          || margin_x == size[0] / 2 - 5 * bottom_bar_height || margin_x == size[0] / 2 - 5 * bottom_bar_height + 1
          || margin_x == size[0] / 2 - 6 * bottom_bar_height + 1
          || margin_x == size[0] / 2 - 6 * bottom_bar_height + 2);
    bool is_zoom_button_border
    = (margin_x >= 0 && margin_x < top_bar_height * 2 - 3
       && (margin_y == size[1] - top_bar_height - top_bar_height * 2 + 4
           || margin_y == size[1] - top_bar_height - top_bar_height * 2 + 5)
      ) || (margin_y >= size[1] - top_bar_height - top_bar_height * 2 + 4 && margin_y < size[1] - top_bar_height
            && (margin_x == top_bar_height * 2 - 3 || margin_x == top_bar_height * 2 - 4));
    bool is_top_bar_button_border
    = margin_y >= size[1] - top_bar_height && margin_y < size[1]
      && (margin_x == top_bar_height - 1 || margin_x == top_bar_height - 2
          || margin_x == top_bar_height * 2 - 3 || margin_x == top_bar_height * 2 - 4
          || margin_x == size[0] / 2 - top_bar_height || margin_x == size[0] / 2 - top_bar_height + 1
          || margin_x == size[0] / 2 - top_bar_height * 2 + 2 || margin_x == size[0] / 2 - top_bar_height * 2 + 3
          || margin_x == size[0] / 2 - top_bar_height * 3 + 4 || margin_x == size[0] / 2 - top_bar_height * 3 + 5);
    return is_app_window_main_frame_border || is_app_window_frame_bar_border || is_bottom_bar_button_border
           || is_zoom_button_border || is_top_bar_button_border;
}

bool is_highlighted(int margin_x, int margin_y, int bottom_bar_height, int top_bar_height)
{
    if (page_number == 0)
        return (margin_x >= 2 && margin_x <= size[0] / 2 - 3
                && margin_y >= bottom_bar_height + 1 && margin_y <= size[1] - top_bar_height - top_bar_height * 2 + 3
               ) || (margin_x >= top_bar_height * 2 - 2 && margin_x <= size[0] / 2 - 3
                     && margin_y >= size[1] - top_bar_height - top_bar_height * 2 + 4
                     && margin_y <= size[1] - top_bar_height - 1);
    else
        return false;
}

bool is_button_border()
/*
    Returns "true" if pixel belongs to any button border and "false" if it does not.
*/
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
/*
    MAIN SHADER FUNCTION
    Calculates intermediate color for all possible cases and mixes it
*/
{
    int margin_x = int(gl_FragCoord[0]) - position[0];
    int margin_y = int(gl_FragCoord[1]) - position[1];
    int bottom_bar_height = int(size[1] / 10);
    int top_bar_height = int(size[1] / 20);
    // button borders are filled with red
    if (is_button_border() || is_app_window_frame(margin_x, margin_y, bottom_bar_height, top_bar_height))
        color_frag = vec4(1.0, 0.0, 0.0, float(onboarding_opacity) / 255.0);
    else if (is_highlighted(margin_x, margin_y, bottom_bar_height, top_bar_height))
        color_frag = vec4(0.25, 0.0, 0.0, float(onboarding_opacity) / 255.0);
    // all other pixels are transparent
    else
        color_frag = vec4(0.0);
}