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

def swaptwo(self, group, i1, i2,t,prevcol1,prevcol2):
    # Get the bars to be swapped
    bar1 = group[i1]
    bar2 = group[i2]

    # Calculate the shift vectors for the bars
    shift1 = bar2.get_x() - bar1.get_x()
    shift2 = bar1.get_x() - bar2.get_x()

    # Create animations for the swap
    self.play(bar1.animate.shift(RIGHT * shift1), bar2.animate.shift(RIGHT * shift2), run_time=t)

    print(prevcol1,prevcol2)
    group[i1].set_color(prevcol1)
    group[i2].set_color(prevcol2)
    group[i1], group[i2] = group[i2], group[i1]
    
    return group



class MainScene(Scene):
    def construct(self):
        bars = 10
        colors = getcolorlist(bars) 
        values = getlist(bars)

        bar_chart = BarChart(
            values,
            bar_colors=colors,
            y_range=[0, max(values) + 1, 10], 
            y_length=5
        )
        bars_group = bar_chart.bars
        bar_chart.bars.set_opacity(0)

        self.play(Create(bar_chart), run_time=1)
        bar_chart.bars.set_opacity(1)
        self.play(DrawBorderThenFill(bars_group),run_time=5)

        self.wait(3)
        

        for i in range(5):
            bars_group = playsingleshuffle(self,bars_group,(5-i)/2)

        self.wait(3)
        

        sorted_bars = sorted(bars_group, key=lambda bar: bar.get_x())
        sorted_group = VGroup(*sorted_bars)
        self.remove(bars_group)
        self.add(sorted_group)

        swapped=True
        while(swapped):
            swapped=False
            for i_bar in range(bars-1):
                prevcol1=str(sorted_group[i_bar].get_color())
                prevcol2=str(sorted_group[i_bar+1].get_color())
                sorted_group[i_bar].set_color(GREEN)
                sorted_group[i_bar+1].set_color(GREEN)
                


                if(sorted_group[i_bar].height>sorted_group[i_bar+1].height):
                    sorted_group=swaptwo(self,sorted_group,i_bar,i_bar+1,0.2,prevcol1,prevcol2)
                    
                    swapped=True
                else:
                    self.wait(0.1)
        
        
        self.wait(3)