from manim import *
import numpy as np


class MainScene(Scene):
    def construct(self):
        a=Axes(x_range=[0,2*PI],y_range=[-1,1])        
        
        circle = Circle()
        circle.set_fill(opacity=0)
        circle.set_stroke(RED)
        
        
        a.stretch_to_fit_height(circle.height)
        a.stretch_to_fit_width(circle.width*3)

    
        graph = a.plot(lambda x: self.func(x), color=RED)

        self.add(circle)
        self.play(Transform(circle,graph),run_time=1)
        self.play(FadeOut(graph))

        vec = a.get_vector([0,1])
        self.play(GrowArrow(vec))

    def create_vector(start_coords, end_coords, axes):
        start_point = axes.c2p(*start_coords)
        end_point = axes.c2p(*end_coords)
        direction = end_point - start_point
        return Vector(direction).shift(start_point)



        

    def func(self,x):
        return np.sin(x)