image_path = 'img/track1_route.png'
locked = False
busy = False
opened = False
under_construction = False
construction_time = 0
supported_carts = (0, 20)
trail_points = []
for i in range(5020):
    trail_points.append((1690 + i, 1763))

trail_points = tuple(trail_points)
stop_point = ((6674, 1763), (6674, 1763), (6674, 1763), (6674, 1763), (6674, 1763), (6674, 1763), (6674, 1763),
              (6674, 1763), (6674, 1763), (6674, 1763), (6674, 1763), (6674, 1763), (6674, 1763), (6674, 1763),
              (6674, 1763), (6674, 1763), (6674, 1763), (6674, 1763), (6674, 1763), (6674, 1763), (6674, 1763))
start_point = None
exit_signal = None
exit_signal_placement = (6720, 1787)
flip_needed = False
invisible_signal = True


def put_route_under_construction(self):
    self.under_construction = True


def update_config(self):
    if self.under_construction:
        self.construction_time -= 1
        if self.construction_time == 0:
            self.locked = False
            self.under_construction = False
