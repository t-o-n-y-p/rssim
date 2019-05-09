#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform int onboarding_page_control_opacity = 0;
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
    else if (page_number == 1)
        return margin_x >= 2 && margin_x < top_bar_height * 2 - 4
               && margin_y >= size[1] - top_bar_height - top_bar_height * 2 + 6
               && margin_y < size[1] - top_bar_height;
    else if (page_number == 2)
        return margin_x >= 2 && margin_x <= bottom_bar_height - 2
               && margin_y >= 2 && margin_y <= bottom_bar_height - 2;
    else if (page_number == 3)
        return margin_x >= bottom_bar_height + 1 && margin_x <= size[0] / 2 - 6 * bottom_bar_height
               && margin_y >= 2 && margin_y <= bottom_bar_height - 2;
    else if (page_number == 4)
        return margin_x >= size[0] / 2 - 6 * bottom_bar_height + 3
               && margin_x <= size[0] / 2 - 5 * bottom_bar_height - 1
               && margin_y >= 2 && margin_y <= bottom_bar_height - 2;
    else if (page_number == 5)
        return margin_x >= size[0] / 2 - 5 * bottom_bar_height + 2
               && margin_x <= size[0] / 2 - 4 * bottom_bar_height - 2
               && margin_y >= 2 && margin_y <= bottom_bar_height - 2;
    else if (page_number == 6)
        return margin_x >= size[0] / 2 - 4 * bottom_bar_height - 1
               && margin_x <= size[0] / 2 - bottom_bar_height - 2
               && margin_y >= 2 && margin_y <= bottom_bar_height - 2;
    else if (page_number == 7)
        return margin_x >= size[0] / 2 - bottom_bar_height + 1 && margin_x <= size[0] / 2 - 3
               && margin_y >= 2 && margin_y <= bottom_bar_height - 2;
    else
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
    if (is_app_window_frame(margin_x, margin_y, bottom_bar_height, top_bar_height))
        color_frag = vec4(1.0, 0.0, 0.0, float(onboarding_page_control_opacity) / 255.0);
    else if (is_highlighted(margin_x, margin_y, bottom_bar_height, top_bar_height))
        color_frag = vec4(1.0, 0.0, 0.0, float(onboarding_page_control_opacity) / 255.0 * 0.5);
    // all other pixels are transparent
    else
        color_frag = vec4(0.0);
}