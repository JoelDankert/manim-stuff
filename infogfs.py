from manim import *
import numpy as np
import random

bars = 50

def getrandlist(count):
    list = []
    for i in range(1,count+1):
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


class MainScene(Scene):
    def construct(self):
        colors = getcolorlist(bars)
        values = getrandlist(bars)
        bar_chart = BarChart(
            values,
            bar_colors=colors,
            y_range=[0, max(values) + 1, 1],  # Ticks every 1
            y_length=5
        )
        bar_chart.y_axis.numbers.set_opacity(0)

        # Adjust labels: Display labels only every 10
        bar_chart.y_axis.add_labels({
            i: str(i) for i in range(0, max(values) + 1, 10)
        })

        self.play(Create(bar_chart),run_time=5)
        self.wait(3)


