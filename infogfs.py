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

    group[i1].set_color(prevcol1)
    group[i2].set_color(prevcol2)
    group[i1], group[i2] = group[i2], group[i1]
    
    return group


def bubblesort(self,bars=10,func=lambda x:5*0.96**x,explain=False):
    colors = getcolorlist(bars) 
    values = getlist(bars)

    bar_chart = BarChart(
        values,
        bar_colors=colors,
        y_range=[0, max(values) + 1, 5], 
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

    if(explain):
        self.wait(15)
    else:
        self.wait(3)
    

    sorted_bars = sorted(bars_group, key=lambda bar: bar.get_x())
    sorted_group = VGroup(*sorted_bars)
    self.remove(bars_group)
    self.add(sorted_group)

    swapped=True

    iterations=0
    reps=0
    while(swapped):
        reps+=1
        if(explain):
            reps=1
        swapped=False
        for i_bar in range(bars-reps):
            iterations+=1
            prevcol1=str(sorted_group[i_bar].get_color())
            prevcol2=str(sorted_group[i_bar+1].get_color())
            sorted_group[i_bar].set_color(GREEN)
            sorted_group[i_bar+1].set_color(GREEN)
            
            waittime=func(iterations)

            if(sorted_group[i_bar].height>sorted_group[i_bar+1].height):
                self.wait(waittime/2)
                sorted_group=swaptwo(self,sorted_group,i_bar,i_bar+1,waittime,prevcol1,prevcol2)
                
                swapped=True
            else:
                self.wait(waittime)
                sorted_group[i_bar].set_color(prevcol1)
                sorted_group[i_bar+1].set_color(prevcol2)

    self.wait(8)

    self.play(FadeOut(bar_chart))
    self.clear()

def intro(self):
    main_text = Text("Sortierverfahren", font_size=100)
    self.play(DrawBorderThenFill(main_text), run_time=5)
    self.play(main_text.animate.shift(UP * 2))

    sub_text = Text("Informatik GFS", font_size=50)
    sub_text.next_to(main_text, DOWN, aligned_edge=LEFT)
    
    author_text = Text("Joel Dankert", font_size=40)
    author_text.next_to(sub_text, DOWN, aligned_edge=LEFT)
    self.play(Write(sub_text),Write(author_text), run_time=3)

    
    grade_text = Text("11", font_size=100)
    grade_text.next_to(main_text, DOWN, aligned_edge=RIGHT)
    self.play(Write(grade_text), run_time=3)
    self.wait(5)
    self.play(FadeOut(main_text,grade_text,author_text,sub_text))



class MainScene(Scene):
    def construct(self):
        
        intro(self)
        self.wait(3)

        

        bubblesort(self,5,lambda x:max(5*0.90**x,0.02),True)
        self.wait(3)
        bubblesort(self,15,lambda x:3*0.94**x+0.05,False)

        self.wait(3)


