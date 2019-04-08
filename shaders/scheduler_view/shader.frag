/*
    Fragment shader for scheduler view.
    Input value:
        vec4 gl_FragCoord - pixel position in 3D homogeneous coordinates (from left bottom point)
    Output value:
        color_frag - calculated normalized RGBA color for the pixel
    Uniforms (all positions are in 2D Cartesian coordinates from the left bottom point):
        ivec2 screen_resolution - current resolution of the game window
        int schedule_opacity - current opacity of schedule screen
*/
#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform ivec2 screen_resolution = ivec2(1280, 720);
uniform int schedule_opacity = 0;

void main()
/*
    MAIN SHADER FUNCTION
    Calculates intermediate color for all possible cases and mixes it
*/
{
    float base_opacity = 0.97;
    // pixels between main borders are painted with background color
    if (gl_FragCoord[0] > 1 && gl_FragCoord[0] < screen_resolution[0] - 2)
        color_frag = vec4(vec3(0.0), base_opacity * schedule_opacity / 255.0);
    // others are transparent
    else
        color_frag = vec4(0.0);
}
