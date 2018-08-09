image_path = None
locked = False
busy = False
opened = False
under_construction = False
construction_time = 0
supported_carts = (12, 20)
trail_points = []
for i in range(5020):
    trail_points.append((6709 - i, 1908))

trail_points = tuple(trail_points)
stop_point = ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
              (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (2228, 1908), (2228, 1908),
              (2228, 1908), (1977, 1908), (1977, 1908), (1977, 1908), (1977, 1908), (1726, 1908), (1726, 1908))
start_point = None
exit_signal = None
exit_signal_placement = (1670, 1932)
flip_needed = True
invisible_signal = True


def put_route_under_construction(self):
    self.under_construction = True


def update_config(self):
    if self.under_construction:
        self.construction_time -= 1
        if self.construction_time == 0:
            self.locked = False
            self.under_construction = False
