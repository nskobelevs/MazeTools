import argparse
from PIL import Image
import random
import time

parser = argparse.ArgumentParser()
parser.add_argument("width", help="Width of the maze", type=int)
parser.add_argument("height", help="Height of the maze", type=int)
args = parser.parse_args()


def prims_algorithm(width: int, height: int, filled_color: tuple, empty_color: tuple):
    """Generates a maze using randomized Prim's algorithm width width x height cell dimensions with a 1px border."""

    if width * height > 10000000:
        raise MemoryError("Maze too large")

    pixel_width = width * 2 + 1
    pixel_height = height * 2 + 1

    img = Image.new("RGB", (pixel_width, pixel_height), empty_color)
    px = img.load()

    # Mark start and end
    px[1, 0] = (0, 255, 0)
    px[pixel_width - 2, pixel_height - 1] = (255, 0, 0)

    # Mark top left cell as part of array and add it's walls to the list
    px[1, 1] = filled_color
    wall_list = [
        (2, 1),
        (1, 2)
    ]

    while len(wall_list) > 0:
        x, y = wall_list.pop(random.randrange(len(wall_list)))

        if px[x, y] == filled_color:
            continue

        if y % 2 == 0:
            cells = ((x, y+1), (x, y-1))
        else:
            cells = ((x+1, y), (x-1, y))

        # Only one of cells is visited
        if px[cells[0][0], cells[0][1]] != px[cells[1][0], cells[1][1]]:
            px[x, y] = filled_color

            for cell in cells:
                px[cell[0], cell[1]] = filled_color

                walls = (
                    (cell[0], cell[1] + 1),
                    (cell[0], cell[1] - 1),
                    (cell[0] + 1, cell[1]),
                    (cell[0] - 1, cell[1]),
                )

                for wall in walls:
                    wallx, wally = wall
                    if wallx < 1 or wally < 1 or wallx >= pixel_width-1 or wally >= pixel_height-1:
                        continue
                    if px[wallx, wally] == filled_color:
                        continue
                    wall_list.append(wall)

    img.save("{}x{}-{:.0f}.png".format(width, height, time.time()))


if __name__ == "__main__":
    start_time = time.time()
    prims_algorithm(args.width, args.height, (255, 255, 255), (0, 0, 0))

    print("That took {} seconds.".format(time.time() - start_time))
