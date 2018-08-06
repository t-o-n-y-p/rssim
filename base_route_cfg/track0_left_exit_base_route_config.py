image_path = 'img/track0_left_exit_route.png'
locked = False
busy = False
opened = False
under_construction = False
construction_time = 0
supported_carts = (0, 20)
trail_points = []
for i in range(6760):
    trail_points.append((759 - i, 1763))

trail_points = tuple(trail_points)
stop_point = ((-5841, 1763), (-5841, 1763), (-5841, 1763), (-5841, 1763), (-5841, 1763), (-5841, 1763), (-5841, 1763),
              (-5841, 1763), (-5841, 1763), (-5841, 1763), (-5841, 1763), (-5841, 1763), (-5841, 1763), (-5841, 1763),
              (-5841, 1763), (-5841, 1763), (-5841, 1763), (-5841, 1763), (-5841, 1763), (-5841, 1763), (-5841, 1763))
start_point = None
exit_signal = None
exit_signal_placement = (-5888, 1730)
flip_needed = False


def put_route_under_construction(self):
    self.under_construction = True


def update_config(self):
    if self.under_construction:
        self.construction_time -= 1
        if self.construction_time == 0:
            self.locked = False
            self.under_construction = False
