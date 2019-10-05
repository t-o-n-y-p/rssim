#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform sampler2D height_map;
uniform ivec2 base_offset = (0, 0);
uniform int twilight_opacity = 255;
uniform float sun_phi_radians = 0.0;
uniform float sun_theta_radians = 0.0;
uniform float sun_brightness = 1.1;
uniform float sun_diffuse_brightness = 0.0;

float bresenham(ivec2 height_map_position, ivec2 ray_trace_finish_point)
{
    ivec2 current_point = height_map_position;
    ivec2 movement_from_height_map_position;
    float distance_from_height_map_position;
    vec4 current_height;
    float calculated_ray_height;
    int a = ray_trace_finish_point[1] - height_map_position[1];
    int b = height_map_position[0] - ray_trace_finish_point[0];
    int sign;
    if (abs(a) > abs(b))
        sign = 1;
    else
        sign = -1;

    int signa, signb;
    if (a < 0)
        signa = -1;
    else
        signa = 1;

    if (b < 0)
        signb = -1;
    else
        signb = 1;

    int f = 0;
    while (current_point[0] >= 0 && current_point[0] <= 8191 && current_point[1] >= 0 && current_point[1] <= 4095
           && current_point != ray_trace_finish_point)
    {
        current_height = texture2D(height_map, current_point);
        calculated_ray_height = current_height + length(current_point - height_map_position) * tan(sun_theta_radians);
        if (calculated_ray_height < current_height.r
            || (calculated_ray_height > current_height.g && calculated_ray_height < current_height.b))
            return 0.0;

        // find next intermediate point using bresenham algorithm
        if (sign == -1)
        {
            f += a*signa;
            if (f > 0)
            {
                f -= b*signb;
                current_point[1] += signa;
            }
            current_point[0] -= signb;
        }
        else
        {
            f += b*signb;
            if (f > 0)
            {
                f -= a*signa;
                current_point[0] -= signb;
            }
            current_point[1] += signa;
        }
    }
    return sun_brightness;
}

void main()
{
    vec3 sunlight_color = vec3(1.0, 1.0, 0.0);
    ivec2 height_map_position = base_offset + ivec2(gl_FragCoord[0], gl_FragCoord[1]);
    ivec2 ray_trace_finish_point = ivec2(height_map_position[0] + int(500 * cos(sun_phi_radians)),
                                         height_map_position[1] + int(500 * sin(sun_phi_radians)));
    float resultive_sun_brightness = bresenham(height_map_position, ray_trace_finish_point);
    resultive_sun_brightness += sun_diffuse_brightness;
    if (resultive_sun_brightness <= 1.0)
        color_frag = vec4(vec3(0.0), (1.0 - resultive_sun_brightness) * twilight_opacity / 255.0);
    else
        color_frag = vec4(sunlight_color, (resultive_sun_brightness - 1.0) * twilight_opacity / 255.0);
}