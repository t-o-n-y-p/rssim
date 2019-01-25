Don't forget to patch cx_Freeze library 
if you use python 3.7+ like I do!

-------------------------------------------

New features:
- all user interface is now adaptive to screen resolution
- added mini-map: you can see where you are while dragging map
- game now is saved also when you close it, not only every 2 in-game hours
- crash logs and game update logs are now created in /logs folder

Fixed issues:
- trains on tracks 1 and 2 do not indicate opened doors now
- fixed crash which was observed if user closed game settings view, 
  returned to the game and some trains were under boarding
- further RAM usage improvements
- reduced number of game files and its size
