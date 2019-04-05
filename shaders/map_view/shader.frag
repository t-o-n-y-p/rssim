/*
    Fragment shader for "main frame" rectangle. "Main frame" is responsible for UI button borders, UI background,
    and general app red border. It calculates normalized RGBA color for each pixel inside the game window.
    Input value:
        vec4 gl_FragCoord - pixel position in 3D homogeneous coordinates (from left bottom point)
    Output value:
        color_frag - calculated normalized RGBA color for the pixel
    Uniforms (all positions are in 2D Cartesian coordinates from the left bottom point):
        ivec2 screen_resolution - current resolution of the game window
        int is_button_activated[] - indicates if button with given index is activated
        int button_x[] - X position of button with given index
        int button_y[] - Y position of button with given index
        int button_w[] - width of button with given index
        int button_h[] - height of button with given index
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
/*
    MAIN SHADER FUNCTION
    Calculates intermediate color for all possible cases and mixes it
*/
{
    // calculate bottom bar color using game frame opacity and settings state
    if (is_button_border())
        color_frag = vec4(1.0, 0.0, 0.0, float(map_opacity) / 255.0);
    // just transparent if there is not bottom bar on the screen
    else
        color_frag = vec4(0.0);
}