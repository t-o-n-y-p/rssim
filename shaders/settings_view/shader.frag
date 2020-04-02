#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform int settings_opacity = 0;
uniform int is_button_activated[26];
uniform int button_x[26];
uniform int button_y[26];
uniform int button_w[26];
uniform int button_h[26];
uniform int number_of_buttons = 26;

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
    // button borders are filled with red
    if (is_button_border())
        color_frag = vec4(1.0, 0.0, 0.0, float(settings_opacity) / 255.0);
    // all other pixels are transparent
    else
        color_frag = vec4(0.0);
}