#version 330 core
out vec4 color_frag;
layout(pixel_center_integer) in vec4 gl_FragCoord;
uniform int is_game_activated = 0;
uniform vec2 screen_resolution = vec2(300, 300);
uniform int game_frame_opacity = 0;
void main()
{
  float real_game_frame_opacity = float(game_frame_opacity) / 255.0 * 0.94;
  float real_game_frame_border_opacity = float(game_frame_opacity) / 255.0 * 1.0;

  if (gl_FragCoord[0] < 2 || gl_FragCoord[0] > screen_resolution[0] - 3 || gl_FragCoord[1] < 2 || gl_FragCoord[1] > screen_resolution[1] - 3 || gl_FragCoord[1] == screen_resolution[1] - 33 || gl_FragCoord[1] == screen_resolution[1] - 34 || (is_game_activated == 1 && (gl_FragCoord[1] == 78 || gl_FragCoord[1] == 79)))
    color_frag = vec4(1.0, 0.0, 0.0, 1.0);
  else if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && gl_FragCoord[1] >= screen_resolution[1] - 32 && gl_FragCoord[1] <= screen_resolution[1] - 3)
    color_frag = vec4(vec3(0.0), 0.94);
  else if (is_game_activated == 1 && gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && (gl_FragCoord[1] == 78 || gl_FragCoord[1] == 79))
    color_frag = vec4(1.0, 0.0, 0.0, real_game_frame_border_opacity);
  else if (is_game_activated == 1 && gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && gl_FragCoord[1] >= 2 && gl_FragCoord[1] <= 77)
    color_frag = vec4(vec3(0.0), real_game_frame_opacity);
  else
    color_frag = vec4(0.0);
}