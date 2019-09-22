#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform sampler2D height_map;
uniform ivec2 base_offset = ivec2(0, 0);
uniform int scale = 1;
uniform float sun_phi_radians = 0.0;
uniform float sun_theta_radians = 0.0;
uniform float sun_brightness = 1.1;
uniform float sun_diffuse_brightness = 0.15;

void main()
{
    vec2 ray_direction = vec2(cos(sun_phi_radians), sin(sun_phi_radians));
    float resultive_sun_brightness = sun_brightness;
    vec3 sunlight_color = vec3(1.0, 1.0, 0.0);
    vec2 map_position = ((-1) * base_offset + vec2(gl_FragCoord[0], gl_FragCoord[1])) * scale;
    vec4 height_map_readings = texture(height_map, vec2(map_position[0] / 8191, map_position[1] / 4095));
    float actual_height = height_map_readings.r;
    for (int i = 1; i < 100; i++)
    {
        vec2 next_map_position = map_position + i * ray_direction;
        vec4 new_height_map_readings = texture(height_map,
                                               vec2(next_map_position[0] / 8191, next_map_position[1] / 4095));
        if (height_map_readings.r + float(i) / 255.0 * tan(sun_theta_radians) < new_height_map_readings.r)
        {
            resultive_sun_brightness = 0.0;
            break;
        }
    }
    resultive_sun_brightness += sun_diffuse_brightness;
    if (resultive_sun_brightness <= 1.0)
        color_frag = vec4(vec3(0.0), 1.0 - resultive_sun_brightness);
    else
        color_frag = vec4(sunlight_color, resultive_sun_brightness - 1.0);
}