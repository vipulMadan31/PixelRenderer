#version 450

// Output colour for the fragment
layout(location = 0) out vec4 outColor;

void main() {
    // Use pixel coordinates as UV (gl_FragCoord.xy gives pixel position)
    vec2 uv = gl_FragCoord.xy;

    outColor = vec4(
        floor(uv.x / 16.0) / 64.0,
        floor(uv.y / 16.0) / 64.0,
        0.0,
        1.0
    );
}