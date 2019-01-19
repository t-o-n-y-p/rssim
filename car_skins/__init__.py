from pyglet.image import load


CAR_COLLECTIONS = 4

CAR_HEAD_IMAGE = []
for i in range(CAR_COLLECTIONS):
    CAR_HEAD_IMAGE.append([])
    for j in range(4):
        CAR_HEAD_IMAGE[i].append(load(f'img/cars/{i}/car_head_{j}.png'))

for i in range(len(CAR_HEAD_IMAGE)):
    for j in range(4):
        CAR_HEAD_IMAGE[i][j].anchor_x = CAR_HEAD_IMAGE[i][j].width // 2
        CAR_HEAD_IMAGE[i][j].anchor_y = CAR_HEAD_IMAGE[i][j].height // 2

CAR_MID_IMAGE = []
for i in range(CAR_COLLECTIONS):
    CAR_MID_IMAGE.append([])
    for j in range(4):
        CAR_MID_IMAGE[i].append(load(f'img/cars/{i}/car_mid_{j}.png'))

for i in range(len(CAR_MID_IMAGE)):
    for j in range(4):
        CAR_MID_IMAGE[i][j].anchor_x = CAR_MID_IMAGE[i][j].width // 2
        CAR_MID_IMAGE[i][j].anchor_y = CAR_MID_IMAGE[i][j].height // 2

CAR_TAIL_IMAGE = []
for i in range(CAR_COLLECTIONS):
    CAR_TAIL_IMAGE.append([])
    for j in range(4):
        CAR_TAIL_IMAGE[i].append(load(f'img/cars/{i}/car_tail_{j}.png'))

for i in range(len(CAR_TAIL_IMAGE)):
    for j in range(4):
        CAR_TAIL_IMAGE[i][j].anchor_x = CAR_TAIL_IMAGE[i][j].width // 2
        CAR_TAIL_IMAGE[i][j].anchor_y = CAR_TAIL_IMAGE[i][j].height // 2

BOARDING_LIGHT_IMAGE = []
for i in range(CAR_COLLECTIONS):
    BOARDING_LIGHT_IMAGE.append(load(f'img/cars/{i}/boarding_lights.png'))

for i in range(len(BOARDING_LIGHT_IMAGE)):
    BOARDING_LIGHT_IMAGE[i].anchor_x = BOARDING_LIGHT_IMAGE[i].width // 2
    BOARDING_LIGHT_IMAGE[i].anchor_y = BOARDING_LIGHT_IMAGE[i].height // 2
