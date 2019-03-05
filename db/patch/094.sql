CREATE TABLE game_progress_temp (unlocked_tracks integer, level integer, exp integer, money real, money_target integer, supported_cars_min integer, supported_cars_max integer, unlocked_car_collections text)
INSERT INTO game_progress_temp (unlocked_tracks, level, exp, money, money_target, supported_cars_min, supported_cars_max, unlocked_car_collections) SELECT unlocked_tracks, level, CAST(exp AS integer), money, money_target, supported_cars_min, supported_cars_max, unlocked_car_collections FROM game_progress
DROP TABLE game_progress
ALTER TABLE game_progress_temp RENAME TO game_progress
UPDATE base_schedule SET exp = CAST(exp AS integer)
UPDATE trains SET exp = CAST(exp AS integer)
CREATE TABLE localization (current_locale text)
INSERT INTO localization VALUES ("en")
CREATE TABLE notification_settings (level_up_notification_enabled integer, feature_unlocked_notification_enabled integer, construction_completed_notification_enabled integer, enough_money_notification_enabled integer)
INSERT INTO notification_settings VALUES (1, 1, 1, 1)
UPDATE version SET major = 0, minor = 9, patch = 4