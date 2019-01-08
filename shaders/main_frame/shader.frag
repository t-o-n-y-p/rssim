#version 330 core
out vec4 color_frag;
layout(pixel_center_integer) in vec4 gl_FragCoord;
uniform vec2 screen_resolution = vec2(300, 300);
uniform int game_frame_opacity = 0;
uniform int schedule_opacity = 0;
void main()
{
    color_frag = vec4(0.0);
    if (gl_FragCoord[0] < 2 || gl_FragCoord[0] > screen_resolution[0] - 3 || gl_FragCoord[1] < 2 || gl_FragCoord[1] > screen_resolution[1] - 3 || gl_FragCoord[1] == screen_resolution[1] - 33 || gl_FragCoord[1] == screen_resolution[1] - 34)
        color_frag = vec4(1.0, 0.0, 0.0, 1.0);
  
    if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && gl_FragCoord[1] >= screen_resolution[1] - 32 && gl_FragCoord[1] <= screen_resolution[1] - 3)
        color_frag = vec4(vec3(0.0), 0.94);

    if (game_frame_opacity > 0)
    {
        float real_game_frame_opacity = float(game_frame_opacity) / 255.0 * 0.94;
        float real_game_frame_border_opacity = float(game_frame_opacity) / 255.0;
        if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && (gl_FragCoord[1] == 78 || gl_FragCoord[1] == 79))
            color_frag = vec4(1.0, 0.0, 0.0, real_game_frame_border_opacity);

        if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && gl_FragCoord[1] >= 2 && gl_FragCoord[1] <= 77)
            color_frag = vec4(vec3(0.0), real_game_frame_opacity);
    }

    if (schedule_opacity > 0)
    {
        float real_schedule_opacity = float(schedule_opacity) / 255.0 * 0.94;
        float gradient_coeff, schedule_coeff;
        vec2 top_left_cell = vec2(int(0.0625 * float(screen_resolution[0])), screen_resolution[1] - 33 - int(float(screen_resolution[1] - 110 - 4 * int(0.0625 * float(screen_resolution[0])) - 3 * int(0.015625 * float(screen_resolution[0])) + int(0.025 * float(screen_resolution[0])) + int(0.01171875 * float(screen_resolution[0]))) / 2.0));
        vec2 top_right_cell = vec2(int(0.0078125 * float(screen_resolution[0])) + int(float(screen_resolution[0]) / 2.0), top_left_cell[1]);
        if (gl_FragCoord[0] >= 2 && gl_FragCoord[0] <= screen_resolution[0] - 3 && gl_FragCoord[1] >= 80 && gl_FragCoord[1] <= screen_resolution[1] - 35)
            if (gl_FragCoord[1] == top_left_cell[1] || gl_FragCoord[1] == top_left_cell[1] + 1)
            {
                if (gl_FragCoord[0] >= top_left_cell[0] && gl_FragCoord[0] <= top_left_cell[0] + int(0.4296875 * float(screen_resolution[0])) - 1)
                {
                    gradient_coeff = (float(top_left_cell[0]) + 0.21484375 * float(screen_resolution[0]) - float(gl_FragCoord[0])) / (0.21484375 * float(screen_resolution[0]));
                    schedule_coeff = (255.0 - abs(int(gradient_coeff * gradient_coeff * gradient_coeff * 255.0))) / 255.0;
                    color_frag = vec4(vec3(schedule_coeff), real_schedule_opacity);
                }
                else if (gl_FragCoord[0] >= top_right_cell[0] && gl_FragCoord[0] <= top_right_cell[0] + int(0.4296875 * float(screen_resolution[0])) - 1)
                {
                    gradient_coeff = (float(top_right_cell[0]) + 0.21484375 * float(screen_resolution[0]) - float(gl_FragCoord[0])) / (0.21484375 * float(screen_resolution[0]));
                    schedule_coeff = (255.0 - abs(int(gradient_coeff * gradient_coeff * gradient_coeff * 255.0))) / 255.0;
                    color_frag = vec4(vec3(schedule_coeff), real_schedule_opacity);
                }
                else
                    color_frag = vec4(vec3(0.0), real_schedule_opacity);
            }
            else
                color_frag = vec4(vec3(0.0), real_schedule_opacity);
    }
}