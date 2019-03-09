"""
This game features several different car models, it would be boring if all trains were the same.
This module parses car models from DDS texture.
"""
from pyglet import resource as _resource


CAR_COLLECTIONS = 12
_resource.path = ['img', 'img/textures.zip']
_resource.reindex()
_cars_texture = _resource.texture('cars_in_one.dds')

# CAR_HEAD_IMAGE includes all textures for leading carriage
CAR_HEAD_IMAGE = []
for i in range(CAR_COLLECTIONS):
    CAR_HEAD_IMAGE.append([])
    for j in range(4):
        CAR_HEAD_IMAGE[i].append(_cars_texture.get_region(j * 251, i * 41, 251, 41))

# anchor is set to the carriage middle point
for i in range(len(CAR_HEAD_IMAGE)):
    for j in range(4):
        CAR_HEAD_IMAGE[i][j].anchor_x = CAR_HEAD_IMAGE[i][j].width // 2
        CAR_HEAD_IMAGE[i][j].anchor_y = CAR_HEAD_IMAGE[i][j].height // 2

# CAR_MID_IMAGE includes all textures for middle carriage
CAR_MID_IMAGE = []
for i in range(CAR_COLLECTIONS):
    CAR_MID_IMAGE.append([])
    for j in range(4):
        CAR_MID_IMAGE[i].append(_cars_texture.get_region((j + 4) * 251, i * 41, 251, 41))

# anchor is set to the carriage middle point
for i in range(len(CAR_MID_IMAGE)):
    for j in range(4):
        CAR_MID_IMAGE[i][j].anchor_x = CAR_MID_IMAGE[i][j].width // 2
        CAR_MID_IMAGE[i][j].anchor_y = CAR_MID_IMAGE[i][j].height // 2

# CAR_TAIL_IMAGE includes all textures for trailing carriage
CAR_TAIL_IMAGE = []
for i in range(CAR_COLLECTIONS):
    CAR_TAIL_IMAGE.append([])
    for j in range(4):
        CAR_TAIL_IMAGE[i].append(_cars_texture.get_region((j + 8) * 251, i * 41, 251, 41))

# anchor is set to the carriage middle point
for i in range(len(CAR_TAIL_IMAGE)):
    for j in range(4):
        CAR_TAIL_IMAGE[i][j].anchor_x = CAR_TAIL_IMAGE[i][j].width // 2
        CAR_TAIL_IMAGE[i][j].anchor_y = CAR_TAIL_IMAGE[i][j].height // 2

# BOARDING_LIGHT_IMAGE includes all textures for boarding lights - they are enabled if boarding is in progress
BOARDING_LIGHT_IMAGE = []
for i in range(CAR_COLLECTIONS):
    BOARDING_LIGHT_IMAGE.append(_cars_texture.get_region(12 * 251, i * 41, 251, 41))

# anchor is set to the carriage middle point
for i in range(len(BOARDING_LIGHT_IMAGE)):
    BOARDING_LIGHT_IMAGE[i].anchor_x = BOARDING_LIGHT_IMAGE[i].width // 2
    BOARDING_LIGHT_IMAGE[i].anchor_y = BOARDING_LIGHT_IMAGE[i].height // 2

# signal images
RED_SIGNAL_IMAGE = _resource.texture('signals.dds').get_region(0, 0, 7, 9)
GREEN_SIGNAL_IMAGE = _resource.texture('signals.dds').get_region(8, 0, 7, 9)
# anchor is set to the middle point
RED_SIGNAL_IMAGE.anchor_x = 3
RED_SIGNAL_IMAGE.anchor_y = 4
GREEN_SIGNAL_IMAGE.anchor_x = 3
GREEN_SIGNAL_IMAGE.anchor_y = 4

_flags = _resource.texture('flags.dds')
FLAG_GB = _flags.get_region(0, 0, 256, 256)
FLAG_RU = _flags.get_region(256, 0, 256, 256)
FLAG_GB.anchor_x = 128
FLAG_GB.anchor_y = 128
FLAG_RU.anchor_x = 128
FLAG_RU.anchor_y = 128
