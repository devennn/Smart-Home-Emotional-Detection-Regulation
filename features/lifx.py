from time import sleep
from lifxlan import BLUE, CYAN, GREEN, LifxLAN, ORANGE, PINK, PURPLE, RED, YELLOW

class LIFX:
    def __init__(self, duration_secs=0.5, init_color=0):
        self.bulb = LifxLAN().get_lights()[0] #Get bulb
        self.colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
        self.duration_secs = duration_secs

        if init_color != 0:
            self.change_colors(seq='one', color_index=init_color)

        self.original_color = self.bulb.get_color()
        self.original_power = self.bulb.get_power()

    def change_colors(self, sleep_secs=0.5, smooth=False, seq='rbw', color_index=0):
        transition_time_ms = self.duration_secs*1000 if smooth else 0
        rapid = True if self.duration_secs < 1 else False
        self.bulb.set_brightness(brightness=1)

        if seq is "rbw":
            for color in self.colors:
                self.bulb.set_color(color, transition_time_ms, rapid)
                sleep(sleep_secs)
        elif seq is "one":
            color = self.colors[color_index]
            print('Apps LIFX: {}'.format(color))
            self.bulb.set_color(color, transition_time_ms, rapid)
            sleep(sleep_secs)

    def reset_original(self):
        self.bulb.set_power(self.original_power)
        sleep(0.5) # for looks
        self.bulb.set_color(self.original_color)

def main():
    lifx = LIFX()
    bulb = lifx.bulb
    print("Selected {}".format(bulb.get_label()))

    print("Turning on light...")
    bulb.set_power("on")

    print("Smooth slow rainbow...")
    lifx.change_colors(sleep_secs=1, smooth=True)

    print("One color...")
    lifx.change_colors(sleep_secs=1, smooth=True, seq='one', color_index=4)

    print("Restoring original power and color...")
    lifx.reset_original()

if __name__ == '__main__':
    main()
