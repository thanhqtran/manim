from manim import *
import numpy as np


class DualDynamics(Scene):
    def construct(self):
        # PARAMETERS
        v = 1.2
        gamma = 8
        mu = np.log(v)
        phi = 0.3
        delta = 0.5
        h_thres = v / (delta * gamma)

        # Value trackers for left and right dynamics
        h_left = ValueTracker(h_thres + 0.1)
        h_right = ValueTracker(h_thres + 0.15)
        T = 25  # number of iterations
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

        # Create the axes for left and right dynamics
        ax_left = Axes(
            x_range=[0, x_endpoints, x_stepsize],
            y_range=[0, y_endpoints, y_stepsize],
            axis_config={"include_tip": True},
            x_length=4,
            y_length=4,
            tips=True
        ).add_coordinates()
        # Move left axis to the left side of the screen
        ax_left.shift(3 * LEFT + 0.5 * UP)
        labels_left = ax_left.get_axis_labels(
            x_label=MathTex(x_label),
            y_label=MathTex(y_label)
        )

        ax_right = Axes(
            x_range=[0, x_endpoints, x_stepsize],
            y_range=[0, y_endpoints, y_stepsize],
            axis_config={"include_tip": True},
            x_length=4,
            y_length=4,
            tips=True
        ).add_coordinates()
        # Move right axis to the right side of the screen
        ax_right.shift(3 * RIGHT + 0.5 * UP)
        labels_right = ax_right.get_axis_labels(
            x_label=MathTex(x_label),
            y_label=MathTex(y_label)
        )

        # PLOT THE GRAPHS
        graph_left = ax_left.plot(
            lambda x: f(x),
            color=BLUE,
            x_range=x_range_points,
            use_smoothing=False
        )
        graph_right = ax_right.plot(
            lambda x: f(x),
            color=BLUE,
            x_range=x_range_points,
            use_smoothing=False
        )
        graph_label_left = MathTex(func_label).next_to(
            ax_left.c2p(x_endpoints, f(x_endpoints)), RIGHT)
        graph_label_right = MathTex(func_label).next_to(
            ax_right.c2p(x_endpoints, f(x_endpoints)), RIGHT)
        
        # 45 degree dashed line
        diag_left = DashedLine(ax_left.coords_to_point(
            0, 0), ax_left.coords_to_point(x_endpoints, x_endpoints), color=GREEN)
        diag_label_left = MathTex(
            x_label+'='+y_label).next_to(ax_left.c2p(x_endpoints, x_endpoints), UP)
        diag_right = DashedLine(ax_right.coords_to_point(
            0, 0), ax_right.coords_to_point(x_endpoints, x_endpoints), color=GREEN)
        diag_label_right = MathTex(
            x_label+'='+y_label).next_to(ax_right.c2p(x_endpoints, x_endpoints), UP)
        

        self.add(ax_left, labels_left, graph_left, graph_label_left, diag_left, diag_label_left)
        self.add(ax_right, labels_right, graph_right, graph_label_right, diag_right, diag_label_right)

        h_labels_left = []  # List to store h_labels for left dynamics
        h_labels_right = []  # List to store h_labels for right dynamics
        runtime = 0.3
        waittime = 0.3
        r = 0.06  # radius of the dots
        left_color = ORANGE
        right_color = RED

        for _ in range(T):
            # LEFT DYNAMICS
            dot1_left = Dot(ax_left.coords_to_point(
                h_left.get_value(), 0), color=left_color, radius=r)
            self.add(dot1_left)
            h_label_left = MathTex(f"{h_left.get_value():.2f}").next_to(
                dot1_left, DOWN, buff=0.1)
            self.add(h_label_left)
            h_labels_left.append(h_label_left)
            trace1_left = DashedLine(dot1_left.get_center(),
                                     dot1_left.get_center(), color=YELLOW)
            self.add(trace1_left)
            self.play(
                MoveAlongPath(dot1_left, Line(dot1_left.get_center(), ax_left.coords_to_point(
                    h_left.get_value(), f(h_left.get_value())))),
                rate_func=smooth,
                run_time=runtime
            )
            self.remove(trace1_left)
            self.wait()

            dot2_left = Dot(ax_left.coords_to_point(
                h_left.get_value(), f(h_left.get_value())), color=left_color, radius=r)
            self.add(dot2_left)
            trace2_left = DashedLine(dot1_left.get_center(),
                                     dot2_left.get_center(), color=YELLOW)
            self.add(trace2_left)
            self.play(
                MoveAlongPath(dot2_left, Line(dot2_left.get_center(),
                              ax_left.coords_to_point(0, f(h_left.get_value())))),
                rate_func=smooth,
                run_time=runtime
            )
            self.remove(trace2_left)
            self.wait(waittime)

            dot3_left = Dot(ax_left.coords_to_point(
                0, f(h_left.get_value())), color=left_color, radius=r)
            self.add(dot3_left)
            h_label_y_left = MathTex(f"{f(h_left.get_value()):.2f}").next_to(
                dot3_left, LEFT, buff=0.1)
            self.add(h_label_y_left)  # Add label for h value on y-axis
            trace3_left = DashedLine(dot2_left.get_center(),
                                    dot3_left.get_center(), color=YELLOW)
            self.add(trace3_left)
            self.play(
                MoveAlongPath(dot3_left, Line(dot3_left.get_center(),
                                            ax_left.coords_to_point(f(h_left.get_value()), 0))),
                rate_func=smooth,
                run_time=runtime
            )
            self.remove(trace3_left)
            self.wait(waittime)

            dot4_left = Dot(ax_left.coords_to_point(
                f(h_left.get_value()), 0), color=left_color, radius=r)
            self.add(dot4_left)
            trace4_left = DashedLine(dot3_left.get_center(),
                                    dot4_left.get_center(), color=YELLOW)
            self.add(trace4_left)
            self.play(
                UpdateFromFunc(dot4_left, lambda m: m.move_to(
                    ax_left.coords_to_point(f(h_left.get_value()), 0))),
                rate_func=smooth,
                run_time=runtime
            )
            self.remove(trace4_left)
            self.wait(waittime)
            self.remove(h_label_y_left)  # Remove label after movement

            # RIGHT DYNAMICS
            dot1_right = Dot(ax_right.coords_to_point(
                h_right.get_value(), 0), color=right_color, radius=r)
            self.add(dot1_right)
            h_label_right = MathTex(f"{h_right.get_value():.2f}").next_to(
                dot1_right, DOWN, buff=0.1)
            self.add(h_label_right)
            h_labels_right.append(h_label_right)
            trace1_right = DashedLine(dot1_right.get_center(),
                                      dot1_right.get_center(), color=YELLOW)
            self.add(trace1_right)
            self.play(
                MoveAlongPath(dot1_right, Line(dot1_right.get_center(), ax_right.coords_to_point(
                    h_right.get_value(), f(h_right.get_value())))),
                rate_func=smooth,
                run_time=runtime
            )
            self.remove(trace1_right)
            self.wait()

            dot2_right = Dot(ax_right.coords_to_point(
                h_right.get_value(), f(h_right.get_value())), color=right_color, radius=r)
            self.add(dot2_right)
            trace2_right = DashedLine(dot1_right.get_center(),
                                      dot2_right.get_center(), color=YELLOW)
            self.add(trace2_right)
            self.play(
                MoveAlongPath(dot2_right, Line(dot2_right.get_center(),
                              ax_right.coords_to_point(0, f(h_right.get_value())))),
                rate_func=smooth,
                run_time=runtime
            )
            self.remove(trace2_right)
            self.wait(waittime)

            dot3_right = Dot(ax_right.coords_to_point(
                0, f(h_right.get_value())), color=right_color, radius=r)
            self.add(dot3_right)
            h_label_y_right = MathTex(f"{f(h_right.get_value()):.2f}").next_to(
                dot3_right, LEFT, buff=0.1)
            self.add(h_label_y_right)  # Add label for h value on y-axis
            trace3_right = DashedLine(dot2_right.get_center(),
                                    dot3_right.get_center(), color=YELLOW)
            self.add(trace3_right)
            self.play(
                MoveAlongPath(dot3_right, Line(dot3_right.get_center(),
                                                ax_right.coords_to_point(f(h_right.get_value()), 0))),
                rate_func=smooth,
                run_time=runtime
            )
            self.remove(trace3_right)
            self.wait(waittime)

            dot4_right = Dot(ax_right.coords_to_point(f(h_right.get_value()), 0), color=right_color, radius=r)
            self.add(dot4_right)
            trace4_right = DashedLine(dot3_right.get_center(),
                                    dot4_right.get_center(), color=YELLOW)
            self.add(trace4_right)
            self.play(
                UpdateFromFunc(dot4_right, lambda m: m.move_to(
                    ax_right.coords_to_point(f(h_right.get_value()), 0))),
                rate_func=smooth,
                run_time=runtime
            )
            self.remove(trace4_right)
            self.wait(waittime)
            self.remove(h_label_y_right)  # Remove label after movement


            # Update h values for left and right dynamics
            h_left.set_value(f(h_left.get_value()))
            h_right.set_value(f(h_right.get_value()))

            # Remove previous h_labels for left dynamics
            for label in h_labels_left:
                self.remove(label)
            h_labels_left.clear()

            # Remove previous h_labels for right dynamics
            for label in h_labels_right:
                self.remove(label)
            h_labels_right.clear()

        self.wait()
