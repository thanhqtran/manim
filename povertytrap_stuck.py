#terminal: manim povertytrap_stuck.py Dynamics -pqm
from manim import *
import numpy as np


class Dynamics(Scene):
    def construct(self):
        # PARAMETERS (Based on Ceroni(2001))
        v = 1.2
        gamma = 8
        mu = np.log(v)
        phi = 0.3
        delta = 0.5
        h_thres = v / (delta * gamma)

        # Value tracker
        h = ValueTracker(h_thres+0.1)
        T = 9  # number of iterations
        x_endpoints = 2
        y_endpoints = 2
        x_stepsize = x_endpoints
        y_stepsize = y_endpoints
        func_label = "\phi(h)"
        x_label = 'h_t'
        y_label = 'h_{t+1}'
        x_range_points = [0, x_endpoints, 0.01]

        # DYNAMIC FUNCTION
        def f(h):
            if h <= h_thres:
                return mu
            else:
                return np.log(delta * (gamma * h + v) / (1 + delta))

        # Create the axes
        ax = Axes(
            x_range=[0, x_endpoints, x_stepsize],
            y_range=[0, y_endpoints, y_stepsize],
            axis_config={"include_tip": True},
            x_length=6,
            y_length=6,
            tips=True
        ).add_coordinates()
        labels = ax.get_axis_labels(
            x_label=MathTex(x_label),
            y_label=MathTex(y_label)
        )

        # PLOT THE GRAPH
        graph = ax.plot(
            lambda x: f(x),
            color=BLUE,
            x_range=x_range_points,
            use_smoothing=False
        )
        graph_label = MathTex(func_label).next_to(
            ax.c2p(x_endpoints, f(x_endpoints)), RIGHT)

        # 45 degree dashed line
        diag = DashedLine(ax.coords_to_point(
            0, 0), ax.coords_to_point(x_endpoints, x_endpoints), color=GREEN)
        diag_label = MathTex(
            x_label+'='+y_label).next_to(ax.c2p(x_endpoints, x_endpoints), RIGHT)

        self.add(ax, labels, graph, graph_label, diag, diag_label)

        h_labels = []  # List to store h_labels
        runtime = 0.2
        waittime = 0.2

        for _ in range(T):
            # CREATE THE PLOT RUNNING OVER TIME
            dot1 = Dot(ax.coords_to_point(h.get_value(), 0), color=RED)
            self.add(dot1)
            h_label = MathTex(f"{h.get_value():.2f}").next_to(
                dot1, DOWN, buff=0.1)
            self.add(h_label)  # Add label for h value
            h_labels.append(h_label)  # Append label to list
            trace1 = DashedLine(dot1.get_center(),
                                dot1.get_center(), color=YELLOW)
            self.add(trace1)
            self.play(
                MoveAlongPath(dot1, Line(dot1.get_center(), ax.coords_to_point(
                    h.get_value(), f(h.get_value())))),
                # run_time=1,  # Adjust the run time as needed
                rate_func=smooth
            )
            self.remove(trace1)
            self.wait()

            dot2 = Dot(ax.coords_to_point(
                h.get_value(), f(h.get_value())), color=RED)
            self.add(dot2)
            trace2 = DashedLine(dot1.get_center(),
                                dot2.get_center(), color=YELLOW)
            self.add(trace2)
            self.play(
                MoveAlongPath(dot2, Line(dot2.get_center(),
                              ax.coords_to_point(0, f(h.get_value())))),
                # run_time=runtime,
                rate_func=smooth
            )
            self.remove(trace2)
            self.wait(waittime)

            dot3 = Dot(ax.coords_to_point(
                0, f(h.get_value())), color=RED)
            self.add(dot3)
            h_label_y = MathTex(f"{f(h.get_value()):.2f}").next_to(
                dot3, LEFT, buff=0.1)
            self.add(h_label_y)  # Add label for h value on y-axis
            trace3 = DashedLine(dot2.get_center(),
                                dot3.get_center(), color=YELLOW)
            self.add(trace3)
            self.play(
                MoveAlongPath(dot3, Line(dot3.get_center(),
                              ax.coords_to_point(f(h.get_value()), 0))),
                # run_time=runtime,
                rate_func=smooth
            )
            self.remove(trace3)
            self.wait(waittime)

            dot4 = Dot(ax.coords_to_point(f(h.get_value()), 0), color=RED)
            self.add(dot4)
            trace4 = DashedLine(dot3.get_center(),
                                dot4.get_center(), color=YELLOW)
            self.add(trace4)
            self.play(
                UpdateFromFunc(dot4, lambda m: m.move_to(
                    ax.coords_to_point(f(h.get_value()), 0))),
                # run_time=runtime,
                rate_func=smooth
            )
            self.remove(trace4)
            self.wait(waittime)
            self.remove(h_label_y)  # Remove label after movement

            h.set_value(f(h.get_value()))

            # Remove previous h_labels
            for label in h_labels:
                self.remove(label)
            h_labels.clear()  # Clear the list for next iteration

        self.wait()
