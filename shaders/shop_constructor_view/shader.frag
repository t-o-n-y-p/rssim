#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform int shop_constructor_opacity = 0;
uniform ivec2 shop_stages_cells_position = ivec2(0, 0);
uniform ivec2 shop_stages_cells_size = ivec2(0, 0);
uniform int current_stage = 0;
uniform int is_button_activated[5];
uniform int button_x[5];
uniform int button_y[5];
uniform int button_w[5];
uniform int button_h[5];
uniform int number_of_buttons = 5;


bool is_button_border()
{
    int button_margin_x, button_margin_y;
    for(int i = 0; i < number_of_buttons; i++)
    {
        if (is_button_activated[i] == 1)
        {
            button_margin_x = int(gl_FragCoord[0]) - button_x[i];
            button_margin_y = int(gl_FragCoord[1]) - button_y[i];
            if ((button_margin_x >= 0 && button_margin_x <= button_w[i] - 1
                 && (button_margin_y == 0 || button_margin_y == 1 || button_margin_y == button_h[i] - 2
                     || button_margin_y == button_h[i] - 1)
                ) || (button_margin_y >= 0 && button_margin_y <= button_h[i] - 1
                      && (button_margin_x == 0 || button_margin_x == 1 || button_margin_x == button_w[i] - 2
                          || button_margin_x == button_w[i] - 1)
                     )
            )
                return true;
        }
    }
    return false;
}

int is_vertical_line(int margin_x, int margin_y, int vertical_line_width)
{
    for (int i=0; i<=8; i+=2)
    {
        int baseline = int(i * (shop_stages_cells_size[0] - vertical_line_width) / 8);
        if (margin_x >= baseline && margin_x <= baseline + vertical_line_width - 1
            && margin_y >= 0 && margin_y <= shop_stages_cells_size[1] - 1)
        {
            if (i == 0)
                return 1;
            else
                return int(i / 2);
        }
    }
    for (int i=1; i<=7; i+=2)
    {
        int baseline = int(i * (shop_stages_cells_size[0] - vertical_line_width) / 8);
        if (margin_x >= baseline && margin_x <= baseline + vertical_line_width - 1
            && ((margin_y >= 0 && margin_y <= vertical_line_width * 3 - 1
                ) || (margin_y >= shop_stages_cells_size[1] - vertical_line_width * 3
                      && margin_y <= shop_stages_cells_size[1] - 1)))
            return int(i / 2) + 1;
    }
    return -1;
}

int is_grey_horizontal_line(int margin_x, int margin_y, int vertical_line_width)
{
    if (margin_x >= 0 && margin_x <= shop_stages_cells_size[0] - 1
        && ((margin_y >= 0 && margin_y <= vertical_line_width - 1)
            || (margin_y >= shop_stages_cells_size[1] - vertical_line_width
                && margin_y <= shop_stages_cells_size[1] - 1)))
    {
        int stage_value = -1;
        for (int i=4; i>=1; i--)
            if (margin_x < int(i * (shop_stages_cells_size[0] - vertical_line_width) / 4))
                stage_value = i;

        return stage_value;
    }
    else
        return -1;
}

int is_light_blue_horizontal_line(int margin_x, int margin_y, int vertical_line_width)
{
    if (margin_x >= 0 && margin_x <= shop_stages_cells_size[0] - 1
        && ((margin_y >= vertical_line_width && margin_y <= vertical_line_width * 3 - 1)
            || (margin_y >= shop_stages_cells_size[1] - vertical_line_width * 3
                && margin_y <= shop_stages_cells_size[1] - vertical_line_width - 1)))
    {
        int stage_value = -1;
        for (int i=4; i>=1; i--)
            if (margin_x < int(i * (shop_stages_cells_size[0] - vertical_line_width) / 4))
                stage_value = i;

        return stage_value;
    }
    else
        return -1;
}

void main()
{
    int margin_x = int(gl_FragCoord[0]) - shop_stages_cells_position[0];
    int margin_y = int(gl_FragCoord[1]) - shop_stages_cells_position[1];
    int vertical_line_width = int(shop_stages_cells_size[0] / 80);
    int number_of_stage_vertical_line = is_vertical_line(margin_x, margin_y, vertical_line_width);
    if (number_of_stage_vertical_line < 0)
    {
        int number_of_stage_horizontal_line = is_grey_horizontal_line(margin_x, margin_y, vertical_line_width);
        if (number_of_stage_horizontal_line < 0)
        {
            int number_of_light_blue_stage_horizontal_line
            = is_light_blue_horizontal_line(margin_x, margin_y, vertical_line_width);
            if (number_of_light_blue_stage_horizontal_line < 0)
            {
                if (is_button_border())
                    color_frag = vec4(1.0, 0.0, 0.0, float(shop_constructor_opacity) / 255.0);
                else
                    color_frag = vec4(0.0);
            }
            else if (number_of_light_blue_stage_horizontal_line <= current_stage)
                color_frag = vec4(0.42578125, 0.5, 0.61, float(shop_constructor_opacity) / 255.0);
            else
                color_frag = vec4(vec3(0.1), pow(float(shop_constructor_opacity) / 255.0, 3));
        }
        else if (number_of_stage_horizontal_line <= current_stage)
            color_frag = vec4(vec3(0.65), pow(float(shop_constructor_opacity) / 255.0, 3));
        else
            color_frag = vec4(vec3(0.1), pow(float(shop_constructor_opacity) / 255.0, 3));
    }
    else if (number_of_stage_vertical_line <= current_stage)
        color_frag = vec4(0.140625, 0.20703125, 0.3671875, float(shop_constructor_opacity) / 255.0);
    else
        color_frag = vec4(vec3(0.1), pow(float(shop_constructor_opacity) / 255.0, 3));
}