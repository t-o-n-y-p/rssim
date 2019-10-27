from typing import Final

from pyglet import resource as _resource


__car_collections_implemented = [12, ]
MAXIMUM_CAR_COLLECTIONS: Final = [12, ]
_resource.path = ['font', 'img', 'img/textures.zip']
_resource.reindex()
_cars_texture = _resource.texture('cars_in_one.dds')
_resource.add_font('perfo-bold.ttf')

# CAR_HEAD_IMAGE includes all textures for leading carriage
PASSENGER_CAR_HEAD_IMAGE: Final = []
for i in range(__car_collections_implemented[0]):
    PASSENGER_CAR_HEAD_IMAGE.append([])
    for j in range(4):
        PASSENGER_CAR_HEAD_IMAGE[i].append(_cars_texture.get_region((j % 2) * 251, i * 47 + 3, 251, 41))

# anchor is set to the carriage middle point
for i in range(len(PASSENGER_CAR_HEAD_IMAGE)):
    for j in range(4):
        PASSENGER_CAR_HEAD_IMAGE[i][j].anchor_x = PASSENGER_CAR_HEAD_IMAGE[i][j].width // 2
        PASSENGER_CAR_HEAD_IMAGE[i][j].anchor_y = PASSENGER_CAR_HEAD_IMAGE[i][j].height // 2

# CAR_MID_IMAGE includes all textures for middle carriage
PASSENGER_CAR_MID_IMAGE: Final = []
for i in range(__car_collections_implemented[0]):
    PASSENGER_CAR_MID_IMAGE.append(_cars_texture.get_region(2 * 251, i * 47 + 3, 251, 41))

# anchor is set to the carriage middle point
for i in range(len(PASSENGER_CAR_MID_IMAGE)):
    PASSENGER_CAR_MID_IMAGE[i].anchor_x = PASSENGER_CAR_MID_IMAGE[i].width // 2
    PASSENGER_CAR_MID_IMAGE[i].anchor_y = PASSENGER_CAR_MID_IMAGE[i].height // 2

# CAR_TAIL_IMAGE includes all textures for trailing carriage
PASSENGER_CAR_TAIL_IMAGE: Final = []
for i in range(__car_collections_implemented[0]):
    PASSENGER_CAR_TAIL_IMAGE.append([])
    for j in range(4):
        PASSENGER_CAR_TAIL_IMAGE[i].append(_cars_texture.get_region((j % 2 + 3) * 251, i * 47 + 3, 251, 41))

# anchor is set to the carriage middle point
for i in range(len(PASSENGER_CAR_TAIL_IMAGE)):
    for j in range(4):
        PASSENGER_CAR_TAIL_IMAGE[i][j].anchor_x = PASSENGER_CAR_TAIL_IMAGE[i][j].width // 2
        PASSENGER_CAR_TAIL_IMAGE[i][j].anchor_y = PASSENGER_CAR_TAIL_IMAGE[i][j].height // 2

# BOARDING_LIGHT_IMAGE includes all textures for boarding lights - they are enabled if boarding is in progress
BOARDING_LIGHT_IMAGE: Final = []
for i in range(__car_collections_implemented[0]):
    BOARDING_LIGHT_IMAGE.append(_cars_texture.get_region(5 * 251, i * 47 + 3, 251, 41))

# anchor is set to the carriage middle point
for i in range(len(BOARDING_LIGHT_IMAGE)):
    BOARDING_LIGHT_IMAGE[i].anchor_x = BOARDING_LIGHT_IMAGE[i].width // 2
    BOARDING_LIGHT_IMAGE[i].anchor_y = BOARDING_LIGHT_IMAGE[i].height // 2

# signal images
RED_SIGNAL_IMAGE: Final = _resource.texture('signals.dds').get_region(0, 0, 7, 9)
GREEN_SIGNAL_IMAGE: Final = _resource.texture('signals.dds').get_region(8, 0, 7, 9)
# anchor is set to the middle point
RED_SIGNAL_IMAGE.anchor_x = 3
RED_SIGNAL_IMAGE.anchor_y = 4
GREEN_SIGNAL_IMAGE.anchor_x = 3
GREEN_SIGNAL_IMAGE.anchor_y = 4

# textures for localization buttons in the top left corner
_flags = _resource.texture('flags.dds')
FLAG_US: Final = _flags.get_region(0, 0, 128, 128)
FLAG_RU: Final = _flags.get_region(128, 0, 128, 128)
FLAG_US.anchor_x = FLAG_US.width // 2
FLAG_US.anchor_y = FLAG_US.height // 2
FLAG_RU.anchor_x = FLAG_RU.width // 2
FLAG_RU.anchor_y = FLAG_RU.height // 2

# textures for switches in crossovers in straight and diverging state
SWITCHES_STRAIGHT: Final = _resource.texture('switches_straight.dds')
SWITCHES_DIVERGING: Final = _resource.texture('switches_diverging.dds')


def get_full_map(map_id, tracks):
    return _resource.texture(f'full_map_{tracks}_{map_id}.dds')


def get_full_map_e(map_id, tiers):
    return _resource.texture(f'full_map_e_{tiers}_{map_id}.dds')
