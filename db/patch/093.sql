UPDATE tracks SET construction_time = 201600 WHERE track_number IN (9, 10) AND locked = 1 AND under_construction = 0
UPDATE tracks SET construction_time = 432000 WHERE track_number IN (15, 16, 25, 26) AND locked = 1 AND under_construction = 0
UPDATE tracks SET construction_time = 345600 WHERE track_number IN (17, 18) AND locked = 1 AND under_construction = 0
UPDATE tracks SET construction_time = 576000 WHERE track_number IN (19, 20) AND locked = 1 AND under_construction = 0
UPDATE tracks SET construction_time = 1728000 WHERE track_number IN (21, 22) AND locked = 1 AND under_construction = 0
UPDATE tracks SET construction_time = 720000 WHERE track_number IN (23, 24) AND locked = 1 AND under_construction = 0
UPDATE tracks SET construction_time = 792000 WHERE track_number IN (27, 28) AND locked = 1 AND under_construction = 0
ALTER TABLE graphics ADD track_money_target_activated integer
UPDATE graphics SET track_money_target_activated = 0
UPDATE version SET major = 0, minor = 9, patch = 3