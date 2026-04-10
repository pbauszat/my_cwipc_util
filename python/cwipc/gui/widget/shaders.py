"""
Contains the shader programs used by the renderer.
"""

"""
Simple shader.
"""

VERTEX_SHADER_SIMPLE: str = """
#version 430 core

layout(location=0) in vec3 position;
layout(location=1) in vec3 input_color;

uniform mat4 transform;

out vec3 color;

void main() {
    gl_Position = transform * vec4(position, 1.0);
    color = input_color;
}
"""

FRAGMENT_SHADER_SIMPLE: str = """
#version 430 core

in vec3 color;
out vec4 output_color;

void main() {
    output_color = vec4(color, 1.0);
}
"""
