from carambar.carambar import CaramBar
import time


with CaramBar():
    for idx, i in enumerate('abcdef'):
        print(i)
        time.sleep(.5)
