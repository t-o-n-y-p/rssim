#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform ivec2 screen_resolution = ivec2(1280, 720);
uniform int top_bar_height = 36;
uniform int opacity = 0;

bool is_general_border() {
    return gl_FragCoord[0] < 2 || gl_FragCoord[0] > screen_resolution[0] - 3     // 2 pixels for left and right border
           || gl_FragCoord[1] < 2 || gl_FragCoord[1] > screen_resolution[1] - 3  // 2 pixels for bottom and top border
           || gl_FragCoord[1] == screen_resolution[1] - top_bar_height + 1       // 2 pixels for top bar border
           || gl_FragCoord[1] == screen_resolution[1] - top_bar_height;
}

bool is_top_bar_button_border() {
    int margin = screen_resolution[0] - int(gl_FragCoord[0]);
    return gl_FragCoord[1] >= screen_resolution[1] - top_bar_height + 2                // pixel Y is inside the top bar
           && gl_FragCoord[1] <= screen_resolution[1] - 3
           && (margin == top_bar_height || margin == top_bar_height - 1                // 2 pixels for close button
               || margin == top_bar_height * 2 - 2 || margin == top_bar_height * 2 - 3 // fullscreen/restore button
               || margin == top_bar_height * 3 - 4 || margin == top_bar_height * 3 - 5 // iconify button
               // locale buttons
               || gl_FragCoord[0] == top_bar_height - 1 || gl_FragCoord[0] == top_bar_height - 2
               || gl_FragCoord[0] == top_bar_height * 2 - 3 || gl_FragCoord[0] == top_bar_height * 2 - 4
              );
}

bool is_inside_top_bar() {
    return gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3  // between app window side borders
           && gl_FragCoord[1] >= screen_resolution[1] - top_bar_height + 2      // between bottom and top borders
           && gl_FragCoord[1] <= screen_resolution[1] - 3;
}

void main() {
    float top_bar_opacity = 1.0;
    // draw app window border and top bar border
    if (is_general_border())
        color_frag = vec4(1.0, 0.0, 0.0, float(opacity) / 255.0);
    // fill top bar with color and draw top bar buttons borders
    else if (is_inside_top_bar())
        if (is_top_bar_button_border())
            color_frag = vec4(1.0, 0.0, 0.0, float(opacity) / 255.0);
        else
            color_frag = vec4(vec3(0.0), top_bar_opacity * float(opacity) / 255.0);
    // all other pixels are transparent here
    else
        color_frag = vec4(0.0);
}