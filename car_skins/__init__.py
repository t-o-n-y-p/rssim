"""
This game features several different car models, it would be boring if all trains were the same.
This module parses car models from DDS texture.
"""
from pyglet import resource as _resource


_car_collections = 4
_resource.path = ['img', 'img/main_map.zip']
_resource.reindex()
_cars_texture = _resource.texture('cars_in_one.dds')

# CAR_HEAD_IMAGE includes all textures for leading carriage
CAR_HEAD_IMAGE = []
for i in range(_car_collections):
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
for i in range(_car_collections):
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
for i in range(_car_collections):
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
for i in range(_car_collections):
    BOARDING_LIGHT_IMAGE.append(_cars_texture.get_region(12 * 251, i * 41, 251, 41))

# anchor is set to the carriage middle point
for i in range(len(BOARDING_LIGHT_IMAGE)):
    BOARDING_LIGHT_IMAGE[i].anchor_x = BOARDING_LIGHT_IMAGE[i].width // 2
    BOARDING_LIGHT_IMAGE[i].anchor_y = BOARDING_LIGHT_IMAGE[i].height // 2
