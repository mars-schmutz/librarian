import random

def rand_scale_xyz(scale):
    x = 1 + random.uniform(-0.5, 0.7) * scale
    y = 1 + random.uniform(0.1, 0.1) * scale
    z = 1 + random.uniform(0.1, 0.1) * scale
    return (x, y, z)

def main():
    for i in range(20):
        coords = rand_scale_xyz(0.3)
        print('')
        print('X::{0}'.format(coords[0]))
        print('Y::{0}'.format(coords[1]))
        print('Z::{0}'.format(coords[2]))
        print('')

main()
