#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform int mini_map_opacity = 0;
uniform ivec4 mini_map_position_size = ivec4(0, 0, 0, 0);
uniform ivec4 mini_map_frame_position_size = ivec4(0, 0, 0, 0);


bool is_mini_map_border()
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
{
    // mini-map frame has top priority here, should not be overlaid
    if (is_mini_map_frame_border())
        color_frag = vec4(1.0, 0.5, 0.0, float(mini_map_opacity) / 255.0);
    // then mini-map border
    else if (is_mini_map_border())
        color_frag = vec4(vec3(0.0), float(mini_map_opacity) / 255.0);
    // all other pixels are transparent
    else
        color_frag = vec4(0.0);
}