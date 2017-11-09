import camera
import collision
import lighting
import rasterization

if __name__ == '__main__':
    collision.create_tex(1000, 'Collision', collision.Point2D(-25, -25), collision.Point2D(25, 25))
    camera.create_tex(1000, 'Camera')
    lighting.create_tex(1000, 'Lighting')
    rasterization.create_tex(1000, 'Rasterization')
    