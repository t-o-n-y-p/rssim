rssim.py run requires:

python 3.7

pygame 1.9.4

-------------------------------------------

rssim.exe build (python setup.py build) also requires:

cx_Freeze 5.1.1 with py3.7 fix

-------------------------------------------

New features:
- track 3
- more carts to make proccess less boring :)
- fixed incorrect dispatching in some cases

Known issues:
- sometimes dead lock is observed somewhere in dispatching or signalling logic, and trains are stuck
