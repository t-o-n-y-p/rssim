ALTER TABLE graphics_config RENAME TO graphics
CREATE TABLE log_options (log_level integer)
INSERT INTO log_options VALUES (30)
ALTER TABLE game_progress ADD unlocked_car_collections text
UPDATE game_progress SET unlocked_car_collections = "0,1,2,3"
UPDATE game_progress SET supported_cars_min = supported_cars_min - 1 WHERE supported_cars_min > 6
UPDATE version SET major = 0, minor = 9, patch = 2