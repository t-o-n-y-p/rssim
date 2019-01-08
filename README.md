Don't forget to patch cx_Freeze library 
if you use python 3.7+ like I do!

-------------------------------------------

New features:
- added 3 new skins for cars
- constructor and schedule screens are now screen-resolution-adaptive
- added 9 more screen resolutions, now 110 screen resolutions are supported

Fixed issues:
- side entry signals are now displayed correctly after track 21/22 is unlocked
- fixed issue when built tracks were not correctly saved
- fixed crash on launch when there is a train on red entry signal waiting for route
- fixed constructor and schedule screens being incorrectly displayed when game is paused
- fixed crash when user gets paid and all tracks are already built
- reduced RAM usage by 25%

Known issues:
- mini-map is still temporarily removed
- trains on tracks 1 and 2 erroneously indicate opened doors
