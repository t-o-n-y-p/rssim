/*
    Fragment shader for map view.
    Input value:
        vec4 gl_FragCoord - pixel position in 3D homogeneous coordinates (from left bottom point)
    Output value:
        color_frag - calculated normalized RGBA color for the pixel
    Uniforms (all positions are in 2D Cartesian coordinates from the left bottom point):
        int is_button_activated[] - indicates if button with given index is activated
        int button_x[] - X position of button with given index
        int button_y[] - Y position of button with given index
        int button_w[] - width of button with given index
        int button_h[] - height of button with given index
        int number_of_buttons - number of buttons on the screen
        int mini_map_opacity - opacity of mini-map
        ivec4 mini_map_position_size - x, y, width and height of mini-map border
        ivec4 mini_map_frame_position_size - x, y, width and height of mini-map frame border
                which indicates current position on map
*/
#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform int map_opacity = 0;
uniform int is_button_activated[1];
uniform int button_x[1];
uniform int button_y[1];
uniform int button_w[1];
uniform int button_h[1];
uniform int number_of_buttons = 1;
uniform int mini_map_opacity = 0;
uniform ivec4 mini_map_position_size = ivec4(0, 0, 0, 0);
uniform ivec4 mini_map_frame_position_size = ivec4(0, 0, 0, 0);

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

bool is_mini_map_border()
/*
    Returns "true" if pixel belongs to mini-map border and "false" if it does not.
*/
{
    int margin_x = int(gl_FragCoord[0]) - mini_map_position_size.x;
    int margin_y = int(gl_FragCoord[1]) - mini_map_position_size.y;
    return ((margin_x >= 0 && margin_x <= mini_map_position_size[2] - 1
             && (margin_y == 0 || margin_y == mini_map_position_size[3] - 1)
            ) || (margin_y >= 0 && margin_y <= mini_map_position_size[3] - 1
                  && (margin_x == 0 || margin_x == mini_map_position_size[2] - 1)
                 )
           );
}

bool is_mini_map_frame_border()
/*
    Returns "true" if pixel belongs to mini-map frame border and "false" if it does not.
*/
{
    int margin_x = int(gl_FragCoord[0]) - mini_map_frame_position_size.x;
    int margin_y = int(gl_FragCoord[1]) - mini_map_frame_position_size.y;
    return ((margin_x >= 0 && margin_x <= mini_map_frame_position_size[2] - 1
             && (margin_y == 0 || margin_y == mini_map_frame_position_size[3] - 1)
            ) || (margin_y >= 0 && margin_y <= mini_map_frame_position_size[3] - 1
                  && (margin_x == 0 || margin_x == mini_map_frame_position_size[2] - 1)
                 )
           );
}

void main()
/*
    MAIN SHADER FUNCTION
    Calculates intermediate color for all possible cases and mixes it
*/
{
    // mini-map frame has top priority here, should not be overlaid
    if (is_mini_map_frame_border())
        color_frag = vec4(1.0, 0.5, 0.0, float(mini_map_opacity) / 255.0);
    // then mini-map border
    else if (is_mini_map_border())
        color_frag = vec4(vec3(0.0), float(mini_map_opacity) / 255.0);
    // last but not least - button borders
    else if (is_button_border())
        color_frag = vec4(1.0, 0.0, 0.0, float(map_opacity) / 255.0);
    // all other pixels are transparent
    else
        color_frag = vec4(0.0);
}