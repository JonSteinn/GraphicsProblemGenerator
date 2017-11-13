import sys

import bezier
import camera
import collision
import lighting
import rasterization
import window2viewport

if __name__ == '__main__':
    count = min(100, int(sys.argv[1])) if len(sys.argv) > 1 else 5
    collision.create_tex(count, 'Collision')
    camera.create_tex(count, 'Camera')
    lighting.create_tex(count, 'Lighting')
    rasterization.create_tex(count, 'Rasterization')
    bezier.create_tex(count, 'Bezier')
    window2viewport.create_tex(count, 'stuff')