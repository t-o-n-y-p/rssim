#version 330 core
layout(pixel_center_integer) in vec4 gl_FragCoord;
out vec4 color_frag;
uniform int shop_constructor_opacity = 0;
uniform ivec2 shop_stages_cells_position = ivec2(0, 0);
uniform ivec2 shop_stages_cells_size = ivec2(0, 0);
uniform int current_stage = 0;

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

void main()
/*
    MAIN SHADER FUNCTION
    Calculates intermediate color for all possible cases and mixes it
*/
{
    int margin_x = int(gl_FragCoord[0]) - shop_stages_cells_position[0];
    int margin_y = int(gl_FragCoord[1]) - shop_stages_cells_position[1];
    int vertical_line_width = int(shop_stages_cells_size[0] / 80);
    int number_of_stage_vertical_line = is_vertical_line(margin_x, margin_y, vertical_line_width);
    if (number_of_stage_vertical_line < 0)
        color_frag = vec4(0.0);
    else if (number_of_stage_vertical_line <= current_stage)
        color_frag = vec4(0.140625, 0.20703125, 0.3671875, float(shop_constructor_opacity) / 255.0);
    else
        color_frag = vec4(vec3(0.1), float(shop_constructor_opacity) / 255.0);
}