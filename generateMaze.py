import argparse
from PIL import Image
import random
import time
import os
import imageio

parser = argparse.ArgumentParser()
parser.add_argument("width", help="Width of the maze", type=int)
parser.add_argument("height", help="Height of the maze", type=int)
args = parser.parse_args()


def prims_algorithm(width: int, height: int, filled_color: tuple, empty_color: tuple):
    """Generates a maze using randomized Prim's algorithm width width x height cell dimensions with a 1px border."""

    # if width * height > 1000000:
    #     raise MemoryError("Maze too large")

    pixel_width = width * 2 + 1
    pixel_height = height * 2 + 1

    img = Image.new("RGB", (pixel_width, pixel_height), empty_color)
    px = img.load()

    px[1, 0] = (0, 255, 0)
    px[pixel_width - 2, pixel_height - 1] = (255, 0, 0)

    start_cell_x = 0
    start_cell_y = 0
    # +1 for border
    start_cell_x_pixel = start_cell_x * 2 + 1
    start_cell_y_pixel = start_cell_y * 2 + 1

    px[start_cell_x_pixel, start_cell_y_pixel] = filled_color
    wall_list = [
        (start_cell_x_pixel, start_cell_y_pixel - 1),
        (start_cell_x_pixel, start_cell_y_pixel + 1),
        (start_cell_x_pixel + 1, start_cell_y_pixel),
        (start_cell_x_pixel - 1, start_cell_y_pixel),
    ]

    counter = 0
    while len(wall_list) > 0:
        x, y = wall_list.pop(random.randrange(len(wall_list)))

        if x < 1 or y < 1 or x >= pixel_width - 1 or y >= pixel_height - 1:
            continue

        if px[x, y] == filled_color:
            continue

        if y % 2 == 0:
            cell1 = (x, y + 1)
            cell2 = (x, y - 1)
        else:
            cell1 = (x + 1, y)
            cell2 = (x - 1, y)

        if px[cell1[0], cell1[1]] != px[cell2[0], cell2[1]]:
            px[x, y] = filled_color

            for cell in (cell1, cell2):
                if px[cell[0], cell[1]] != filled_color:
                    px[cell[0], cell[1]] = filled_color
                    wall_list.append((cell[0], cell[1] - 1))
                    wall_list.append((cell[0], cell[1] + 1))
                    wall_list.append((cell[0] - 1, cell[1]))
                    wall_list.append((cell[0] + 1, cell[1]))
                    break
            img.save("temp/{}.png".format(counter))
            counter += 1

    img.save("{}x{}-{:.0f}.png".format(width, height, time.time()))


if __name__ == "__main__":
    start_time = time.time()
    prims_algorithm(args.width, args.height, (255, 255, 255), (0, 0, 0))

    print("That took {} seconds.".format(time.time() - start_time))
