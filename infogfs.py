from manim import *
import numpy as np
import random

def customwait(self,time):
    self.wait(time)

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
        y_range=[0, max(values) + 0.5, 5], 
        y_length=5
    )
    bars_group = bar_chart.bars
    bar_chart.bars.set_opacity(0)

    self.play(Create(bar_chart), run_time=1)
    bar_chart.bars.set_opacity(1)
    self.play(DrawBorderThenFill(bars_group),run_time=5)

    customwait(1.3*3)
    

    for i in range(5):
        bars_group = playsingleshuffle(self,bars_group,(5-i)/2)

    if(explain):
        customwait(1.3*15)
    else:
        customwait(1.3*3)
    

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
                customwait(1.3*waittime/2)
                sorted_group=swaptwo(self,sorted_group,i_bar,i_bar+1,waittime,prevcol1,prevcol2)
                
                swapped=True
            else:
                customwait(1.3*waittime)
                sorted_group[i_bar].set_color(prevcol1)
                sorted_group[i_bar+1].set_color(prevcol2)

    customwait(1.3*8)

    self.play(FadeOut(bar_chart))
    self.clear()


def setTitle(self,text,fontsize,dist):
    main_text = Text(text, font_size=fontsize)
    top_of_canvas = config.frame_height / 2
    self.play(DrawBorderThenFill(main_text), run_time=3)
    self.play(main_text.animate.shift(UP * (top_of_canvas - dist)))
    return main_text

def StableUnstableGraphic(self):
    stable_top_vals = [5, 8, 9, 8, 3]
    stable_bot_vals = [3, 5, 8, 8, 9]

    stable_x_positions = [-5, -3, -1, 1, 3]
    y_top = 1
    y_bot = -1

    stable_top_circles = VGroup()
    for x, val in zip(stable_x_positions, stable_top_vals):
        circle = Circle(radius=0.5, color=WHITE).move_to([x, y_top, 0])
        label = Text(str(val), font_size=50).move_to(circle.get_center())
        stable_top_circles.add(VGroup(circle, label))

    stable_bot_circles = VGroup()
    for x, val in zip(stable_x_positions, stable_bot_vals):
        circle = Circle(radius=0.5, color=YELLOW).move_to([x, y_bot, 0])
        label = Text(str(val), font_size=50).move_to(circle.get_center())
        stable_bot_circles.add(VGroup(circle, label))

    stable_arrows = VGroup()
    arrow_1 = Arrow(
        start=stable_top_circles[1].get_center()+(DOWN*0.5),
        end=stable_bot_circles[2].get_center()+(UP*0.5),
        color=YELLOW,
        buff=0
    )

    arrow_2 = Arrow(
        start=stable_top_circles[3].get_center()+(DOWN*0.5),
        end=stable_bot_circles[3].get_center()+(UP*0.5),
        color=YELLOW,
        buff=0
    )

    stable_arrows.add(arrow_1, arrow_2)

    unstable_top_vals = [5, 8, 9, 8, 3]
    unstable_bot_vals = [3, 5, 8, 8, 9]
    
    unstable_x_positions = [1, 3, 5, 7, 9]


    unstable_top_circles = VGroup()
    for x, val in zip(unstable_x_positions, unstable_top_vals):
        circle = Circle(radius=0.5, color=WHITE).move_to([x, y_top, 0])
        label = Text(str(val), font_size=50).move_to(circle.get_center())
        unstable_top_circles.add(VGroup(circle, label))


    unstable_bot_circles = VGroup()
    for x, val in zip(unstable_x_positions, unstable_bot_vals):
        circle = Circle(radius=0.5, color=YELLOW).move_to([x, y_bot, 0])
        label = Text(str(val), font_size=50).move_to(circle.get_center())
        unstable_bot_circles.add(VGroup(circle, label))


    unstable_arrows = VGroup()
    arrow_a = Arrow(
        start=unstable_top_circles[1].get_center()+(DOWN*0.5),
        end=unstable_bot_circles[3].get_center()+(UP*0.5),
        color=YELLOW,
        buff=0
    )
    arrow_b = Arrow(
        start=unstable_top_circles[3].get_center()+(DOWN*0.5),
        end=unstable_bot_circles[2].get_center()+(UP*0.5),
        color=YELLOW,
        buff=0
    )
    unstable_arrows.add(arrow_a, arrow_b)

    


    scenegroup = VGroup(stable_top_circles,stable_bot_circles,unstable_top_circles,unstable_bot_circles,stable_arrows,unstable_arrows)
    scenegroup.center()
    scenegroup.scale(0.6)
    scenegroup.shift(DOWN)

    stable_arrows.shift(LEFT*1.5)
    unstable_arrows.shift(RIGHT*1.5)

    leftgroup = VGroup(stable_top_circles,stable_bot_circles)
    rightgroup = VGroup(unstable_top_circles,unstable_bot_circles)
    leftgroup.shift(LEFT*1.5)
    rightgroup.shift(RIGHT*1.5)

    stable_title = Text("Stabil", font_size=32)\
        .next_to(scenegroup,UP,0.5)\
        .shift(LEFT*5)
    unstable_title = Text("Instabil", font_size=32)\
        .next_to(scenegroup,UP,0.5)\
        .shift(RIGHT*5)

    titles = VGroup(stable_title,unstable_title)
    titles.shift(UP*0)
    
    self.play(Create(Rectangle(WHITE,4,0.2).shift(DOWN)))

    self.play(FadeIn(stable_title), FadeIn(unstable_title))
    self.play(
        LaggedStart(
            *[Create(mob) for mob in stable_top_circles],
            *[Create(mob) for mob in unstable_top_circles],
            lag_ratio=0.1
        )
    )

    customwait(1.3*5)

    self.play(
        LaggedStart(
            *[Create(mob) for mob in stable_bot_circles],
            *[Create(mob) for mob in unstable_bot_circles],
            lag_ratio=0.1
        )
    )


    customwait(1.3*5)

    self.play(*[GrowArrow(arrow) for arrow in stable_arrows])

    customwait(1.3 * 3)

    self.play(*[GrowArrow(arrow) for arrow in unstable_arrows])

    customwait(1.3*5)

def intro(self):
    main_text = setTitle(self,"Sortierverfahren",100,2)

    sub_text = Text("Informatik GFS", font_size=50)
    sub_text.next_to(main_text, DOWN, aligned_edge=LEFT)
    
    author_text = Text("Joel Dankert", font_size=40)
    author_text.next_to(sub_text, DOWN, aligned_edge=LEFT)
    self.play(Write(sub_text),Write(author_text), run_time=3)

    
    grade_text = Text("11", font_size=100)
    grade_text.next_to(main_text, DOWN, aligned_edge=RIGHT)
    self.play(Write(grade_text), run_time=3)
    image = ImageMobject(r"E:\tempdefault\manim shit\manim-shit\banner.png")
    image.scale(0.8)
    image.next_to(main_text,DOWN,aligned_edge=RIGHT)
    image.shift(LEFT*1.25)
    
    self.play(GrowFromCenter(image),run_time=3)
    customwait(1.3*5)
    self.play(FadeOut(*self.mobjects))


def F1_definition(self):
    main_text = setTitle(self,"Definition",50,1)

    
    second_text = Paragraph(
        "Sortierverfahren ordnen Elemente einer Liste oder",
        "eines Arrays in eine definierte Reihenfolge. (z.B. aufsteigend)",
        width=12,
        alignment="center",
        )
    
    second_text.to_edge(UP)
    second_text.shift(DOWN*2)
    self.play(Write(second_text))
    customwait(1.3*5)
    self.play(second_text.animate.shift(UP*0.7))

    Highlight = VGroup(
            second_text[0][30:44],
            second_text[1][0:11]
        )
    self.play(Highlight.animate.set_color(RED))
    customwait(1.3*2)

    bars=10
    values = getlist(bars)

    bar_chart = BarChart(
        values,
        bar_colors=[WHITE,WHITE],
        y_range=[0, max(values) + 0.5, 1], 
        y_length=5
    )
    bars_group = bar_chart.bars
    bar_chart.scale(0.8)
    bar_chart.shift(DOWN*1.5)
    bar_chart.bars.set_opacity(0)

    self.play(Create(bar_chart), run_time=1)
    bar_chart.bars.set_opacity(1)
    bars_old=bars_group.copy()
    self.play(DrawBorderThenFill(bars_group),run_time=5)

    playsingleshuffle(self,bars_group,3)
    customwait(1.3*5)
    self.play(Transform(bars_group,bars_old),run_time=3)
    customwait(1.3*3)
    self.play(FadeOut(*self.mobjects))

def F2_usages(self):
    main_text = setTitle(self,"Verwendungen",50,1)

    
    second_text = Paragraph(
        "Sortierverfahren werden in vielen Bereichen verwendet.",
        "Die Effizienz eines solchen Verfahrens ist essenziell.",
        width=12,
        alignment="center",
        )
    
    second_text.to_edge(UP)
    second_text.shift(DOWN*2)
    self.play(Write(second_text))
    customwait(1.3*5)
    self.play(second_text.animate.shift(UP*0.7))

    Highlight = VGroup(
            second_text[0][24:39],
            second_text[1][3:12]
        )
    self.play(Highlight.animate.set_color(RED))
    customwait(1.3*2)

    list_text = Paragraph(
        "> Softwareentwicklung - Allgemein",
        "> Datenbanken - Sortieren von Einträgen",
        "> Suchmaschienen - Sortieren nach Relevanz",
        width=10,
        alignment="left",
        )

    Highlight = VGroup(
            list_text[0][1:20],
            list_text[1][1:12],
            list_text[2][1:15]
        )
    Highlight.set_color(ORANGE)

    self.play(Write(list_text[0]))
    customwait(1.3*10)
    self.play(Write(list_text[1]))
    customwait(1.3*10)
    self.play(Write(list_text[2]))
    customwait(1.3*10)

    tex_text = Tex(
            r"\(\rightarrow\) Sortierung nach einem \textit{key}",  # Italicize "key"
            font_size=60,  # Adjust font size if needed
        )

    tex_text.shift(DOWN * 2)

    # Add and animate the text
    self.play(Write(tex_text))
    
    customwait(1.3*2)
    box = SurroundingRectangle(tex_text, color=RED, buff=0.3)
    self.play(Create(box),run_time=3)


    customwait(1.3*3)
    self.play(FadeOut(*self.mobjects))

def F3_keys(self):
    main_text = setTitle(self,"Keys",50,1)

    second_text = Paragraph(
        "Ein Key setzt die zu erreichende Reihenfolge der Elemente fest.",
        "Er wird pro Element bestimmt, im Anschluss wird dann sortiert.",
        width=12,
        alignment="center",
        )
    
    second_text.to_edge(UP)
    second_text.shift(DOWN*2)
    self.play(Write(second_text))
    customwait(1.3*5)
    self.play(second_text.animate.shift(UP*0.7))

    Highlight = VGroup(
            second_text[0][27:343],
            second_text[1][9:16]
        )
    self.play(Highlight.animate.set_color(RED))
    customwait(1.3*2)

    list_text = Paragraph(
        "> Zahlen - Alter, Dauer, Temperatur, ...",
        "> Text - Alphabetisch, Länge, ...",
        "> Bilder - Helligkeit, Dateigröße, ...",
        width=10,
        alignment="left",
        )

    Highlight = VGroup(
            list_text[0][1:7],
            list_text[1][1:5],
            list_text[2][1:7]
        )
    Highlight.set_color(ORANGE)

    self.play(Write(list_text[0]))
    customwait(1.3*10)
    self.play(Write(list_text[1]))
    customwait(1.3*10)
    self.play(Write(list_text[2]))
    customwait(1.3*10)


    tex_text = Tex(
            r"Können auch \textit{reversed} werden.",  # Italicize "key"
            font_size=60,  # Adjust font size if needed
        )

    tex_text.shift(DOWN * 2)

    # Add and animate the text
    self.play(Write(tex_text))
    
    customwait(1.3*8)
    self.play(FadeOut(*self.mobjects))

def F4_ausprobieren(self):
    main_text = setTitle(self,"Spielkarten",50,1)

    second_text = Paragraph(
        "Spielkarten können folgendermaßen sortiert werden (Key):",
        width=12,
        alignment="center",
        )

    second_text.to_edge(UP)
    second_text.shift(DOWN*2)
    self.play(Write(second_text))
    customwait(1.3*2)
    self.play(second_text.animate.shift(UP*0.7))

    image = ImageMobject(r"E:\tempdefault\manim shit\manim-shit\cards.png")
    image.scale(1)
    
    
    self.play(GrowFromCenter(image),run_time=2)

    third_text = Paragraph(
        "(das Symbol der Karte ist egal)",
        width=5,
        alignment="center",
        )

    third_text.shift(DOWN*1.7)
    self.play(Write(third_text))

    customwait(1.3*5)
    fourth_text = Paragraph(
        "Probiert es aus!",
        width=8,
        alignment="center",
        )

    fourth_text.to_edge(DOWN)
    fourth_text.set_color(RED)
    fourth_text.shift(UP*0.25)
    self.play(Write(fourth_text))

    customwait(1.3*10)
    self.play(FadeOut(*self.mobjects))

def F5_stabilitaet(self):
    main_text = setTitle(self,"Stabilität",50,1)

    second_text = Paragraph(
        "Ein Sortierverfahren gilt als stabil, wenn gleichrangige Elemente",
        "auch nach dem Sortieren ihre ursprüngliche Reihenfolge beibehalten.",
        width=12,
        alignment="center",
        )

    second_text.to_edge(UP)
    second_text.shift(DOWN*2)
    self.play(Write(second_text))
    customwait(1.3*2)
    self.play(second_text.animate.shift(UP*0.7))

    StableUnstableGraphic(self)

    

    customwait(1.3*10)
    self.play(FadeOut(*self.mobjects))


class MainScene(Scene):
    def construct(self):
        self.final()

    def final(self):
        intro(self)
        customwait(1.3*3)
        F1_definition(self)
        customwait(1.3*3)
        F2_usages(self)
        customwait(1.3*3)
        F3_keys(self)
        customwait(1.3*3)
        F4_ausprobieren(self)
        customwait(1.3*3)
        F5_stabilitaet(self)


        customwait(1.3*3)
        setTitle(self,"Bubble Sort (5)",50,1)
        bubblesort(self,5,lambda x:max(5*0.90**x,0.02),True)
        customwait(1.3*3)
        setTitle(self,"Bubble Sort (15)",50,1)
        bubblesort(self,15,lambda x:3*0.94**x+0.05,False)

        customwait(1.3*3)