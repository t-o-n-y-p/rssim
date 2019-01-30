from pyglet import resource


_car_collections = 4
resource.path = ['img', 'img/main_map.zip']
resource.reindex()
_cars_texture = resource.texture('cars_in_one.dds')

CAR_HEAD_IMAGE = []
for i in range(_car_collections):
    CAR_HEAD_IMAGE.append([])
    for j in range(4):
        CAR_HEAD_IMAGE[i].append(_cars_texture.get_region(j * 251, i * 41, 251, 41))

for i in range(len(CAR_HEAD_IMAGE)):
    for j in range(4):
        CAR_HEAD_IMAGE[i][j].anchor_x = CAR_HEAD_IMAGE[i][j].width // 2
        CAR_HEAD_IMAGE[i][j].anchor_y = CAR_HEAD_IMAGE[i][j].height // 2

CAR_MID_IMAGE = []
for i in range(_car_collections):
    CAR_MID_IMAGE.append([])
    for j in range(4):
        CAR_MID_IMAGE[i].append(_cars_texture.get_region((j + 4) * 251, i * 41, 251, 41))

for i in range(len(CAR_MID_IMAGE)):
    for j in range(4):
        CAR_MID_IMAGE[i][j].anchor_x = CAR_MID_IMAGE[i][j].width // 2
        CAR_MID_IMAGE[i][j].anchor_y = CAR_MID_IMAGE[i][j].height // 2

CAR_TAIL_IMAGE = []
for i in range(_car_collections):
    CAR_TAIL_IMAGE.append([])
    for j in range(4):
        CAR_TAIL_IMAGE[i].append(_cars_texture.get_region((j + 8) * 251, i * 41, 251, 41))

for i in range(len(CAR_TAIL_IMAGE)):
    for j in range(4):
        CAR_TAIL_IMAGE[i][j].anchor_x = CAR_TAIL_IMAGE[i][j].width // 2
        CAR_TAIL_IMAGE[i][j].anchor_y = CAR_TAIL_IMAGE[i][j].height // 2

BOARDING_LIGHT_IMAGE = []
for i in range(_car_collections):
    BOARDING_LIGHT_IMAGE.append(_cars_texture.get_region(12 * 251, i * 41, 251, 41))

for i in range(len(BOARDING_LIGHT_IMAGE)):
    BOARDING_LIGHT_IMAGE[i].anchor_x = BOARDING_LIGHT_IMAGE[i].width // 2
    BOARDING_LIGHT_IMAGE[i].anchor_y = BOARDING_LIGHT_IMAGE[i].height // 2
