#version 330 core
in vec2 vert;
void main()
{
  gl_Position = vec4(vert, 1, 1);
}