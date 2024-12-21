from manim import *
import numpy as np


class MainScene(Scene):
    def construct(self):

        title = Text("trigonometric identity", font_size=30, color=WHITE).shift([0,3.5,0])
        subtitle = Text("phase shift", font_size=20, color=WHITE).shift([0,3.15,0])
        self.play(Create(title))
        self.play(Create(subtitle))
        


        a = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.25, 1.25, 1],
            x_axis_config={"include_ticks": True},
            y_axis_config={"include_ticks": True},
        )

        # Add custom x-axis labels (0 and π)
        a.x_axis.add_labels({
            PI: MathTex("\\pi"),
        })

        # Add custom y-axis labels (1, 0, -1)
        a.y_axis.add_labels({
            -1: MathTex("-1"),
            0: MathTex("0"),
            1: MathTex("1"),
        })

        self.play(Create(a))
        self.wait(1)

    
        graph = a.plot(lambda x: np.sin(x), color=RED)
        sinlabel = MathTex(r"\sin(x)",color=RED).shift([0.5,1,0])
        newsinlabel = MathTex(r"\sin\left(x+\frac{\pi}{2}\right)",color=GREEN).shift([5.5,1,0])
        graph2 = a.plot(lambda x: np.cos(x), color=GREEN)
        coslabel = MathTex(r"\cos(x)",color=GREEN).shift([-2.5,1,0])
        graph3 = a.plot(lambda x: -np.sin(x), color=GREEN)


        self.play(Create(graph),Create(sinlabel))
        self.play(Create(graph2),Create(coslabel))
        
        self.wait(2)

        self.play(
            sinlabel.animate.shift(a.c2p(PI/2,0)[0]*LEFT*1.6),
            coslabel.animate.shift(a.c2p(PI/2,0)[0]*LEFT*1.6)
        )

        self.wait(1)

        vec = self.create_vector((PI,0) ,(PI/2,0) ,a)
        veclabel = MathTex(r"+\frac{\pi}{2}").next_to(vec, UP*0.5).shift([-0.35,0,0])
        newvec = self.create_vector((PI/2,0) ,(PI/2,0) ,a)
        self.play(GrowArrow(vec))
        self.wait(1)
        self.play(Create(veclabel,run_time=1))
        self.wait(2)
        self.play(
            graph.animate.shift(a.c2p(PI/2,0)*RIGHT),
            Transform(vec,newvec),
            veclabel.animate.shift(a.c2p(PI/2,0)*RIGHT),
            FadeOut(veclabel,run_time=0.5),
            sinlabel.animate.shift(a.c2p(PI/2,0)[0]*RIGHT*0.15)
        )
        
        self.remove(newvec)

        graph3.shift(a.c2p(PI/2,0)*LEFT)
        self.play(
            Transform(sinlabel,newsinlabel),
            FadeIn(graph3),
            FadeToColor(graph,GREEN)
        )

        self.wait(1)

        self.play(
            coslabel.animate.shift([-4.25,0,0]),
            sinlabel.animate.shift([-4.25,0,0])
        )

        eqlabel = MathTex(r"=",color=GREEN).shift([-0.6,1,0])
        self.play(Create(eqlabel))

        self.wait(3)
       


    @staticmethod
    def create_vector(start_coords, end_coords, axes):
        start_point = axes.c2p(*start_coords)
        end_point = axes.c2p(*end_coords)
        direction = end_point - start_point
        return Vector(direction).shift(start_point)
    