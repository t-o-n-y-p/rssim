from pyglet.image import load


car_collections = 4

car_head_image = []
for i in range(car_collections):
    car_head_image.append([])
    for j in range(4):
        car_head_image[i].append(load(f'img/cars/{i}/car_head_{j}.png'))

for i in range(len(car_head_image)):
    for j in range(4):
        car_head_image[i][j].anchor_x = car_head_image[i][j].width // 2
        car_head_image[i][j].anchor_y = car_head_image[i][j].height // 2

car_mid_image = []
for i in range(car_collections):
    car_mid_image.append([])
    for j in range(4):
        car_mid_image[i].append(load(f'img/cars/{i}/car_mid_{j}.png'))

for i in range(len(car_mid_image)):
    for j in range(4):
        car_mid_image[i][j].anchor_x = car_mid_image[i][j].width // 2
        car_mid_image[i][j].anchor_y = car_mid_image[i][j].height // 2

car_tail_image = []
for i in range(car_collections):
    car_tail_image.append([])
    for j in range(4):
        car_tail_image[i].append(load(f'img/cars/{i}/car_tail_{j}.png'))

for i in range(len(car_tail_image)):
    for j in range(4):
        car_tail_image[i][j].anchor_x = car_tail_image[i][j].width // 2
        car_tail_image[i][j].anchor_y = car_tail_image[i][j].height // 2

boarding_light_image = []
for i in range(car_collections):
    boarding_light_image.append(load(f'img/cars/{i}/boarding_lights.png'))

for i in range(len(boarding_light_image)):
    boarding_light_image[i].anchor_x = boarding_light_image[i].width // 2
    boarding_light_image[i].anchor_y = boarding_light_image[i].height // 2
