import sys

import bezier
import camera
import collision
import lighting
import rasterization

if __name__ == '__main__':
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    collision.create_tex(count, 'Collision', collision.Point2D(-25, -25), collision.Point2D(25, 25))
    camera.create_tex(count, 'Camera')
    lighting.create_tex(count, 'Lighting')
    rasterization.create_tex(count, 'Rasterization')
    bezier.create_tex(count, 'Bezier')