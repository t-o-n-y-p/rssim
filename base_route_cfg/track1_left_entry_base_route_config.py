image_path = 'img/track1_left_entry_route.png'
locked = False
busy = False
opened = False
under_construction = False
construction_time = 0
supported_carts = (0, 20)
trail_points = []
for i in range(59):
    trail_points.append((760 + i, 1836))

pattern = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0),
           (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0),
           (18, -1), (19, -1), (20, -1), (21, -1), (22, -1), (23, -1), (24, -1),
           (25, -1), (26, -1), (27, -1), (28, -1), (29, -1), (30, -1),
           (31, -2), (32, -2), (33, -2), (34, -2), (35, -2), (36, -2), (37, -2), (38, -2), (39, -2),
           (40, -3), (41, -3), (42, -3), (43, -3), (44, -3), (45, -3), (46, -3),
           (47, -4), (48, -4), (49, -4), (50, -4), (51, -4), (52, -4),
           (53, -5), (54, -5), (55, -5), (56, -5), (57, -5), (58, -5),
           (59, -6), (60, -6), (61, -6), (62, -6), (63, -6),
           (64, -7), (65, -7), (66, -7), (67, -7), (68, -7),
           (68, -8), (69, -8), (70, -8), (71, -8),
           (72, -9), (73, -9), (74, -9), (75, -9),
           (76, -10), (77, -10), (78, -10), (79, -10),
           (80, -11), (81, -11), (82, -11), (83, -11),
           (84, -12), (85, -12), (86, -12), (87, -12),
           (88, -13), (89, -13), (90, -13),
           (91, -14), (92, -14), (93, -14), (94, -14),
           (94, -15), (95, -15), (96, -15),
           (97, -16), (98, -16), (99, -16),
           (100, -17), (101, -17), (102, -17),
           (103, -18), (104, -18), (105, -18),
           (106, -19), (107, -19), (108, -19),
           (109, -20), (110, -20), (111, -20),
           (111, -21), (112, -21), (113, -21),
           (114, -22), (115, -22),
           (116, -23), (117, -23), (118, -23),
           (119, -24), (120, -24), (121, -24),
           (122, -25), (123, -25),
           (123, -26), (124, -26), (125, -26),
           (126, -27), (127, -27),
           (128, -28), (129, -28),
           (130, -29), (131, -29), (132, -29),
           (133, -30), (134, -30),
           (134, -31), (135, -31),
           (136, -32), (137, -32), (138, -32),
           (139, -33), (140, -33),
           (141, -34), (142, -34),
           (142, -35), (143, -35),
           (144, -36), (145, -36),
           (146, -37), (147, -37),
           (148, -38), (149, -38),
           (149, -39), (150, -39),
           (151, -40), (152, -40),
           (153, -41), (154, -41), (155, -41),
           (156, -42), (157, -42),
           (157, -43), (158, -43),
           (159, -44), (160, -44), (161, -44),
           (162, -45), (163, -45),
           (164, -46), (165, -46),
           (166, -47), (167, -47), (168, -47),
           (168, -48), (169, -48),
           (170, -49), (171, -49), (172, -49),
           (173, -50), (174, -50), (175, -50),
           (176, -51), (177, -51),
           (178, -52), (179, -52), (180, -52),
           (180, -53), (181, -53), (182, -53),
           (183, -54), (184, -54), (185, -54),
           (186, -55), (187, -55), (188, -55),
           (189, -56), (190, -56), (191, -56),
           (192, -57), (193, -57), (194, -57),
           (195, -58), (196, -58), (197, -58),
           (197, -59), (198, -59), (199, -59), (200, -59),
           (201, -60), (202, -60), (203, -60),
           (204, -61), (205, -61), (206, -61), (207, -61),
           (208, -62), (209, -62), (210, -62), (211, -62),
           (212, -63), (213, -63), (214, -63), (215, -63),
           (216, -64), (217, -64), (218, -64), (219, -64),
           (220, -65), (221, -65), (222, -65), (223, -65),
           (223, -66), (224, -66), (225, -66), (226, -66), (227, -66),
           (228, -67), (229, -67), (230, -67), (231, -67), (232, -67),
           (233, -68), (234, -68), (235, -68), (236, -68), (237, -68), (238, -68),
           (239, -69), (240, -69), (241, -69), (242, -69), (243, -69), (244, -69),
           (245, -70), (246, -70), (247, -70), (248, -70), (249, -70), (250, -70), (251, -70),
           (252, -71), (253, -71), (254, -71), (255, -71), (256, -71), (257, -71), (258, -71), (259, -71), (260, -71),
           (261, -72), (262, -72), (263, -72), (264, -72), (265, -72), (266, -72), (267, -72),
           (268, -72), (269, -72), (270, -72), (271, -72), (272, -72), (273, -72),
           (274, -73), (275, -73), (276, -73), (277, -73), (278, -73), (279, -73), (280, -73), (281, -73), (282, -73),
           (283, -73), (284, -73), (285, -73), (286, -73), (287, -73), (288, -73), (289, -73), (290, -73), (291, -73)]

for i in pattern:
    trail_points.append((i[0] + 819, i[1] + 1836))

for i in range(579):
    trail_points.append((1111 + i, 1763))

trail_points = tuple(trail_points)
stop_point = None
start_point = None
exit_signal = None
exit_signal_placement = None
flip_needed = False


def put_route_under_construction(self):
    self.under_construction = True


def update_config(self):
    if self.under_construction:
        self.construction_time -= 1
        if self.construction_time == 0:
            self.locked = False
            self.under_construction = False
