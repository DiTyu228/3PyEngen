// Фрагментный шейдер (.frag)
#version 330
struct RayPayloadType {
  vec3 color;
}; // type of the "payload" variable

struct HitAttributeType {
  vec3 normal; // unused
}; // type of the "hit" variable

// Returns a camera ray for a camera at the origin that is looking in negative z-direction.
// "fieldOfViewY" must be given in degrees.
// "point" must be in range [0.0, 1.0] to cover the complete image plane.
//
vec3 getCameraRay(float fieldOfViewY, float aspectRatio, vec2 point) {
  // compute focal length from given field-of-view
  float focalLength = 1.0 / tan(0.5 * fieldOfViewY * 3.14159265359 / 180.0);
  // compute position in the camera's image plane in range [-1.0, 1.0]
  vec2 pos = 2.0 * (point - 0.5);
  return normalize(vec3(pos.x * aspectRatio, pos.y, -focalLength));
}

/**** COMMON END ****/

// Ray tracing shaders must be defined in the following order:
// ray generation, closest-hit, miss, intersection, any-hit

void main() { /**** RAY GENERATION SHADER ****/

  // compute the texture coordinate for the output image in range [0.0, 1.0]
  vec2 texCoord = (vec2(gl_LaunchIDEXT.xy) + 0.5) / vec2(gl_LaunchSizeEXT.xy);

  // camera's aspect ratio
  float aspect = float(gl_LaunchSizeEXT.x) / float(gl_LaunchSizeEXT.y);

  vec3 rayOrigin = vec3(0.0, 0.0, 0.0);
  vec3 rayDirection = getCameraRay(30.0, aspect, texCoord);

  uint rayFlags = gl_RayFlagsNoneEXT; // no ray flags
  float rayMin = 0.001; // minimum ray distance for a hit
  float rayMax = 10000.0; // maximum ray distance for a hit
  uint cullMask = 0xFFu; // no culling

  // Submitting the camera ray to the acceleration structure traversal.
  // The last parameter is the index of the "payload" variable (always 0)
  traceRayEXT(topLevelAS, rayFlags, cullMask, 0u, 0u, 0u,
         rayOrigin, rayMin, rayDirection, rayMax, 0);

  // result is in the "payload" variable
  gsnSetPixel(vec4(payload.color, 1.0));
}

void  main() { /**** CLOSEST-HIT SHADER ****/
   // set color to red
   payload.color = vec3(1.0, 0.0, 0.0);
}