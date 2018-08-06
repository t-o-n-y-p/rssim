image_path = 'img/track0_right_exit_route.png'
locked = False
busy = False
opened = False
under_construction = False
construction_time = 0
supported_carts = (0, 20)
trail_points = []
for i in range(6760):
    trail_points.append((8399 - 759 + i, 1836))

trail_points = tuple(trail_points)
stop_point = ((14240, 1836), (14240, 1836), (14240, 1836), (14240, 1836), (14240, 1836), (14240, 1836), (14240, 1836),
              (14240, 1836), (14240, 1836), (14240, 1836), (14240, 1836), (14240, 1836), (14240, 1836), (14240, 1836),
              (14240, 1836), (14240, 1836), (14240, 1836), (14240, 1836), (14240, 1836), (14240, 1836), (14240, 1836))
start_point = None
exit_signal = None
exit_signal_placement = (14287, 1860)
flip_needed = True


def put_route_under_construction(self):
    self.under_construction = True


def update_config(self):
    if self.under_construction:
        self.construction_time -= 1
        if self.construction_time == 0:
            self.locked = False
            self.under_construction = False
