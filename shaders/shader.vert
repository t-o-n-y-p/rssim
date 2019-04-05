/*
    Vertex shader for "main frame" rectangle. "Main frame" is responsible for UI button borders, UI background,
    and general app red border. Since "main frame" does not move anywhere, vertices positions are never changed.
    Input value:
        vec2 vert - vertice position in 2D Cartesian coordinates
    Output value:
        vec4 gl_Position - vertice position in 3D homogeneous coordinates
*/
#version 330 core
in vec2 vert;
void main()
{
    gl_Position = vec4(vert, 1.0, 1.0);
}