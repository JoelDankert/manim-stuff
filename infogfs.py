from manim import *
import numpy as np
import random

def getlist(count):
    list = []
    for i in range(1, count + 1):
        list.append(i)

    return list

def getcolorlist(count):
    colors = []
    for i in range(count):
        # Calculate the red and green components for the gradient
        red = 255
        green = int(255 - (255 * (i / (count - 1))))
        blue = 0

        # Convert the RGB values to a hex color
        hex_color = f"#{red:02X}{green:02X}{blue:02X}"
        colors.append(hex_color)

    return colors

def shuffle_lists(values, colors):
    combined = list(zip(values, colors))  # Combine values and colors
    random.shuffle(combined)  # Shuffle the combined list
    shuffled_values, shuffled_colors = zip(*combined)  # Unzip into two lists
    return list(shuffled_values), list(shuffled_colors)

def playsingleshuffle(self,oldbar,t):
    newbar = oldbar.copy()
    indices = list(range(len(oldbar)))
    random.shuffle(indices)

    for i, index in enumerate(indices):
        target_position = oldbar[index].get_bottom()  # Get the bottom of the target bar
        current_bottom = newbar[i].get_bottom()  # Get the current bottom of the bar
        shift_vector = target_position - current_bottom  # Calculate the shift required
        newbar[i].shift(shift_vector)  # Apply the shift

    self.play(Transform(oldbar, newbar), run_time=t)

    return oldbar


class MainScene(Scene):
    def construct(self):
        bars = 50  # Example number of bars
        colors = getcolorlist(bars)  # Get sorted colors
        values = getlist(bars)  # Get sorted values

        bar_chart = BarChart(
            values,
            bar_colors=colors,
            y_range=[0, max(values) + 1, 10],  # Ticks every 1
            y_length=5
        )
        bars_group = bar_chart.bars
        bar_chart.bars.set_opacity(0)

        self.play(Create(bar_chart), run_time=1)
        bar_chart.bars.set_opacity(1)
        self.play(DrawBorderThenFill(bars_group),run_time=5)
        self.wait(3)
        

        for i in range(5):
            bars_group = playsingleshuffle(self,bars_group,5-i)

        bars_group = playsingleshuffle(self,bars_group,0.5)

        sorted_bars = sorted(bars_group, key=lambda bar: bar.get_x())
        sorted_group = VGroup(*sorted_bars)
        self.remove(bars_group)
        self.add(sorted_group)

        #for i in range(bars):
        #    sorted_group[0].color = GREEN      sorted group is sorted by indecies and perfectly available
    
        self.wait(3)