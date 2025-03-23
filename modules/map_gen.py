from PIL import Image

tiles = {
    'sol':(6,1),
    'mur':(1,1),
    'depart':(11,2),
    'north':(1,0),
    'south':(1,3),
    'west':(0,1),
    'east':(3,1),
    'corner_nw':(0,0),
    'corner_ne':(3,0),
    'corner_sw':(0,3),
    'corner_se':(3,3),
    'biscorner_nw':(3,4),
    'biscorner_ne':(2,4),
    'biscorner_sw':(1,4),
    'biscorner_se':(0,4),
    'start':(12,0),
    'end':(12,1),
    'pierre':(12,2)
}


def get_tile(position, tile_size=(16, 16)):
    tileset = Image.open('assets/tileset.png')
    x, y = position
    tile_width, tile_height = tile_size
    left = x * tile_width
    upper = y * tile_height
    right = left + tile_width
    lower = upper + tile_height
    tile = tileset.crop((left, upper, right, lower))
    return tile

def draw_map(tile_matrix, tile_size=(16, 16)):
    rows = len(tile_matrix)
    cols = len(tile_matrix[0])
    map_width = cols * tile_size[0]
    map_height = rows * tile_size[1]
    map_image = Image.new('RGB', (map_width, map_height))

    for y, row in enumerate(tile_matrix):
        for x, tile in enumerate(row):
            tile = get_tile(tiles[tile], tile_size)
            map_image.paste(tile, (x * tile_size[0], y * tile_size[1]))

    return map_image


