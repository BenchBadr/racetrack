from PIL import Image

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
        for x, tile_pos in enumerate(row):
            tile = get_tile(tile_pos, tile_size)
            map_image.paste(tile, (x * tile_size[0], y * tile_size[1]))

    return map_image

# Example usage
tile_matrix = [
    [(0, 0), (6, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)]
]

map_image = draw_map(tile_matrix)
map_image.show()