#version 330 core
out vec4 color_frag;
layout(pixel_center_integer) in vec4 gl_FragCoord;
uniform bool is_game_activated = false;
uniform vec2 screen_resolution = vec2(300, 300);
void main()
{
  if (gl_FragCoord[0] < 2 || gl_FragCoord[0] > screen_resolution[0] - 3 || gl_FragCoord[1] < 2 || gl_FragCoord[1] > screen_resolution[1] - 3 || gl_FragCoord[1] == screen_resolution[1] - 33 || gl_FragCoord[1] == screen_resolution[1] - 34 || (is_game_activated && (gl_FragCoord[1] == 78 || gl_FragCoord[1] == 79)))
    color_frag = vec4(1.0, 0.0, 0.0, 1.0);

  if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && gl_FragCoord[1] >= screen_resolution[1] - 32 && gl_FragCoord[1] <= screen_resolution[1] - 3)
    color_frag = vec4(vec3(0.0), 0.94);
}