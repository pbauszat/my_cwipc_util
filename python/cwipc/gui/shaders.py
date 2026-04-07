"""
Contains the OpenGL shaders for the OpenGL pointcloud widget.
"""

VERTEX_SHADER: str = """
#version 430 core
        
layout(location=0) in vec3 position;

uniform mat4 transform;

void main() {
    gl_Position = transform * vec4(position, 1.0);
}
"""

FRAGMENT_SHADER: str = """
#version 430 core
        
out vec3 color;

void main() {
    color = vec3(0.0, 1.0, 0.0);
}
"""
