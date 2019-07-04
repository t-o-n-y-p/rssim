#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform ivec2 screen_resolution = ivec2(1280, 720);
uniform int constructor_opacity = 0;
uniform int cell_x[8];
uniform int cell_y[8];
uniform int cell_w[8];
uniform int cell_h[8];
uniform int cell_unlock_available[8];
uniform int number_of_cells = 8;
uniform int data_length[8];

bool is_cell_border()
{
    int margin_x, margin_y;
    for(int i = 0; i < number_of_cells; i++)
    {
        if (data_length[i] > 0)
        {
            margin_x = int(gl_FragCoord[0]) - cell_x[i];
            margin_y = int(gl_FragCoord[1]) - cell_y[i];
            if ((margin_x >= 0 && margin_x <= cell_w[i] - 1
                 && (margin_y == 0 || margin_y == 1 || margin_y == cell_h[i] - 2
                     || margin_y == cell_h[i] - 1)
                ) || (margin_y >= 0 && margin_y <= cell_h[i] - 1
                      && (margin_x == 0 || margin_x == 1 || margin_x == cell_w[i] - 2
                          || margin_x == cell_w[i] - 1)
                     )
            )
                return true;
        }
    }
    return false;
}

bool is_cell_button_border()
{
    int margin_x, margin_y;
    for(int i = 0; i < number_of_cells; i++)
    {
        if (cell_unlock_available[i] == 1)
        {
            margin_x = int(gl_FragCoord[0]) - cell_x[i];
            margin_y = int(gl_FragCoord[1]) - cell_y[i];
            if (margin_y >= 0 && margin_y <= cell_h[i] - 1
                && (margin_x == cell_w[i] - cell_h[i] || margin_x == cell_w[i] - cell_h[i] + 1
                    || margin_x == cell_w[i] - cell_h[i] * 2 + 2
                    || margin_x == cell_w[i] - cell_h[i] * 2 + 3)
            )
                return true;
        }
    }
    return false;
}

void main()
{
    float base_opacity = 0.97;
    // cell and button borders are red
    if (is_cell_border() || is_cell_button_border())
        color_frag = vec4(1.0, 0.0, 0.0, constructor_opacity / 255.0);
    // other cells between app window edges are filled with background color
    else if (gl_FragCoord[0] > 1 && gl_FragCoord[0] < screen_resolution[0] - 2)
        color_frag = vec4(vec3(0.0), base_opacity * constructor_opacity / 255.0);
    // just transparent otherwise
    else
        color_frag = vec4(0.0);
}