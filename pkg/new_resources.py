import argparse
import colorsys
import math
import os
import shutil
import statistics
from base64 import b64decode
from io import BytesIO

from PIL import Image, ImageFile, ImageColor, ImageOps

ImageFile.LOAD_TRUNCATED_IMAGES = True


def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert a resource pack to a \'Minecraft Plus!\' resource pack')
    parser.add_argument('source', metavar='SOURCE', type=file_path,
                        help='the source resource pack')
    parser.add_argument('resolution', metavar='RESOLUTION', type=int,
                        help='the resolution of the resource pack')
    parser.add_argument('-t', '--tmp', metavar='TMPDIR', type=new_dir, default='tmpextract',
                        help='a temporary directory for extracting the resource pack')
    parser.add_argument('-r', '--resources', metavar='RESOURCES', type=dir_path, default='resources',
                        help='a temporary directory for extracting the resource pack')
    args = parser.parse_known_args()[0]
    parser.add_argument('-d', '--destination', metavar='DESTINATION', type=new_dir,
                        default='resources-' + os.path.splitext(os.path.basename(args.source))[0],
                        help='a temporary directory for extracting the resource pack')
    parser.add_argument('--fullblocklist', metavar='FULLBLOCKLISTPATH', type=full_block_list,
                        default=os.path.join(args.resources, 'full_blocks.txt'),
                        help='a temporary directory for extracting the resource pack')

    return parser.parse_args()


def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


def full_block_list(string):
    if os.path.isfile(string):
        with open(string) as f:
            blocklist = []
            line = f.readline()
            while line:
                split = list(line.strip().split(' '))
                last = split[len(split) - 1]
                if any(c.isalpha() for c in last):
                    blocklist.append(last)
                line = f.readline()
            return blocklist
    else:
        raise FileNotFoundError(string)


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise FileNotFoundError(string)


def new_dir(string):
    if os.path.exists(string):
        raise FileExistsError(string)
    else:
        return string


def copy_min_files(resources_path, dest_path):
    for f in ['copyright.txt', 'icon.ico', 'icon.png']:
        shutil.copy(os.path.join(resources_path, f), os.path.join(dest_path, f))
    for d in ['panoramas/fallback']:
        shutil.copytree(os.path.join(resources_path, d), os.path.join(dest_path, d))


def copy_panorama(resources_path, dest_path):
    if os.path.isdir(os.path.join(resources_path, "assets/minecraft/textures/gui/title/background")):
        shutil.copytree(os.path.join(resources_path, "assets/minecraft/textures/gui/title/background"), os.path.join(dest_path, 'panoramas/background'))
        with open(os.path.join(dest_path, 'panoramas.txt'), 'w') as txt:
            print("background", file=txt)
    else:
        print(' Not found...', end='')


def create_creeper_png(res, resources_path, dest_path):
    if os.path.isfile(os.path.join(resources_path, "assets/minecraft/textures/entity/creeper/creeper.png")):
        with Image.open(os.path.join(resources_path, "assets/minecraft/textures/entity/creeper/creeper.png")) as img:
            width, height = img.size
            img.crop((height/4, height/4, height/2, height/2)).save(os.path.join(dest_path, 'creeper.png'))
    else:
        print(' Not found...', end='')


def copy_footprint(resources_path, dest_path):
    if os.path.isfile(os.path.join(resources_path, "assets/minecraft/textures/particle/footprint.png")):
        shutil.copy(os.path.join(resources_path, "assets/minecraft/textures/particle/footprint.png"), os.path.join(dest_path, 'footprint.png'))
    else:
        print(' Not found...', end='')


def copy_grass(resources_path, dest_path):
    if os.path.isfile(os.path.join(resources_path, "assets/minecraft/textures/block/dirt.png")):
        os.mkdir(os.path.join(dest_path, 'grass'))
        shutil.copy(os.path.join(resources_path, "assets/minecraft/textures/block/dirt.png"), os.path.join(dest_path, 'grass/dirt.png'))
    else:
        print(' Dirt not found...', end='')
    if os.path.isfile(os.path.join(resources_path, "assets/minecraft/textures/block/grass_block_top.png")):
        if not os.path.isdir(os.path.join(dest_path, 'grass')):
            os.mkdir(os.path.join(dest_path, 'grass'))
        shutil.copy(os.path.join(resources_path, "assets/minecraft/textures/block/grass_block_top.png"), os.path.join(dest_path, 'grass/grass.png'))
    else:
        print(' Grass not found...', end='')
    if os.path.isfile(os.path.join(resources_path, "assets/minecraft/textures/colormap/grass.png")):
        if not os.path.isdir(os.path.join(dest_path, 'grass')):
            os.mkdir(os.path.join(dest_path, 'grass'))
        with Image.open(os.path.join(resources_path, "assets/minecraft/textures/colormap/grass.png")) as image:
            ImageOps.flip(image).save(os.path.join(dest_path, 'grass/colors.png'))
    else:
        print(' Colors not found...', end='')


# Based in part on a script by ewanhowell5195#5195 on the DokuCraft Discord https://discord.gg/2MB8bRQ
def create_full_blocks_png(block_list, res, size, source_path, dest_path):
    if len(block_list) > pow(size, 2):
        raise RuntimeError('The file list is too long for a ' + size + 'x' + size + ' full_blocks.png')
    img = Image.new('RGB', (size * res, size * res))
    i = 0
    while i < len(block_list):
        if block_list[i] == 'creeper.png':
            texture = Image.open(BytesIO(b64decode(
                'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEUAAABSpTVPnM+eAAAAFUlEQVR4XmP4zzATCJ8zHAbC2wz/ATIsBnnEkuehAAAAAElFTkSuQmCC'
            ))).convert('RGBA').resize((res, res), Image.NEAREST)
        else:
            f = os.path.join(source_path, 'assets/minecraft/textures/block', block_list[i])
            if os.path.isfile(f):
                texture = Image.open(f).convert('RGBA').crop((0, 0, res, res))
                bg_h, bg_s, bg_v = colorsys.rgb_to_hsv(*average_color(texture)[0:3])
                bg_v = bg_v / 2
                texture = remove_transparency(texture, tuple([round(e) for e in colorsys.hsv_to_rgb(bg_h, bg_s, bg_v)]))
                if block_list[i] in [
                    'acacia_leaves.png',
                    'birch_leaves.png',
                    'dark_oak_leaves.png',
                    'jungle_leaves.png',
                    'oak_leaves.png',
                    'spruce_leaves.png'
                ]:
                    # texture = image_tint(texture, get_leaf_tint(source_path, list[i]))
                    texture = ImageOps.colorize(texture.convert("L"), (0, 0, 0, 0), get_leaf_tint(source_path, block_list[i]))
                if 'water' in block_list[i]:
                    texture = ImageOps.colorize(texture.convert("L"), (0, 0, 0, 0), "#3F76E4")
            else:
                print(" Couldn't find " + f + "...", end='')
                block_list.pop(i)
                continue
        img.paste(texture, ((i % size) * res, math.floor(i / size) * res))
        i += 1
    img.save(os.path.join(dest_path, 'full_blocks.png'))
    with open(os.path.join(dest_path, 'full_blocks.txt'), 'w') as txt:
        print(size, file=txt)
        print(len(block_list), file=txt)
        for i, block in enumerate(block_list):
            print(math.floor(i / size), (i % size), block, file=txt)


# Adapted from https://stackoverflow.com/a/33507138
def remove_transparency(src, color='#ffffff'):
    background = Image.new('RGBA', src.size, color)
    return Image.alpha_composite(background, src)


def average_color(src):
    pixel = src.copy()
    pixel.thumbnail((1, 1))
    return pixel.getpixel((0, 0))


def get_leaf_tint(src, name):
    return {
        "oak": lambda: get_tint(src, 'foliage', "Forest"),
        "spruce": lambda: "#619961",
        "birch": lambda: "#80a755",
        "jungle": lambda: get_tint(src, 'foliage', "Jungle"),
        "acacia": lambda: get_tint(src, 'foliage', "Savanna"),
        "dark_oak": lambda: get_tint(src, 'foliage', "Dark Forest"),
    }[name[:-11]]()


def get_tint(src, blend, biome):
    with Image.open(os.path.join(src, 'assets/minecraft/textures/colormap/' + blend + '.png')) as tints:
        out = tints.getpixel(
            {
                "The Void": (127, 191),
                "Plains": (50, 173),
                "Forest": (76, 112),
                "Jungle": (12, 36),
                "Savanna": (0, 255),
                "Dark Forest": (76, 122),
            }[biome]
        )[0:3]
        if biome == "Dark Forest":
            out = tuple(map(statistics.mean, zip(out, (40, 52, 10))))
        return out


def main():
    args = parse_arguments()
    print('Unpacking...', end='')
    shutil.unpack_archive(args.source, args.tmp, 'zip')
    print(' Done.')
    print('Basic setup...', end='')
    os.mkdir(args.destination)
    copy_min_files(args.resources, args.destination)
    print(' Done.')
    print('Creating full_blocks.png...', end='')
    create_full_blocks_png(args.fullblocklist, args.resolution, 32, args.tmp, args.destination)
    print(' Done.')
    print('Copying default panorama...', end='')
    copy_panorama(args.tmp, args.destination)
    print(' Done.')
    print('Creating creeper.png...', end='')
    create_creeper_png(args.resolution, args.tmp, args.destination)
    print(' Done.')
    print('Copying footprint...', end='')
    copy_footprint(args.tmp, args.destination)
    print(' Done.')
    print('Copying grass...', end='')
    copy_grass(args.tmp, args.destination)
    print(' Done.')
    print('Cleaning up...', end='')
    shutil.rmtree(args.tmp)
    print(' Done.')


if __name__ == '__main__':
    main()
