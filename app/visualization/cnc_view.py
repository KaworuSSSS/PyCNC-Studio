import plotly.graph_objects as go

from app.visualization.cnc_machine_3d import CNCMachine3D


class CNCView:

    def __init__(self, simulator):

        self.simulator = simulator

    def create_figure(self):

        machine = CNCMachine3D()

        fig = machine.build()

        status = self.simulator.get_status()

        position = status["position"]

        toolpath = self.simulator.get_toolpath()

        # -------------------------------------------------
        # TOOLPATH
        # -------------------------------------------------

        if toolpath:

            x = [
                point["x"]
                for point in toolpath
            ]

            y = [
                point["y"]
                for point in toolpath
            ]

            z = [
                point["z"]
                for point in toolpath
            ]

            fig.add_trace(
                go.Scatter3d(
                    x=x,
                    y=y,
                    z=z,
                    mode="lines+markers",
                    name="Toolpath",
                    line=dict(width=6),
                    marker=dict(size=4),
                )
            )

        # -------------------------------------------------
        # POSICION DE LA HERRAMIENTA
        # -------------------------------------------------

        tool_x = position["x"]
        tool_y = position["y"]
        tool_z = position["z"]

        fig.add_trace(
            go.Scatter3d(
                x=[tool_x],
                y=[tool_y],
                z=[tool_z],
                mode="markers",
                name="Herramienta",
                marker=dict(
                    size=12,
                    symbol="diamond",
                ),
            )
        )

        # -------------------------------------------------
        # EJE X
        # -------------------------------------------------

        fig.add_trace(
            go.Scatter3d(
                x=[0, 30],
                y=[0, 0],
                z=[2, 2],
                mode="lines",
                name="X",
                line=dict(width=6),
            )
        )

        # -------------------------------------------------
        # EJE Y
        # -------------------------------------------------

        fig.add_trace(
            go.Scatter3d(
                x=[0, 0],
                y=[0, 30],
                z=[2, 2],
                mode="lines",
                name="Y",
                line=dict(width=6),
            )
        )

        # -------------------------------------------------
        # EJE Z
        # -------------------------------------------------

        fig.add_trace(
            go.Scatter3d(
                x=[0, 0],
                y=[0, 0],
                z=[2, 30],
                mode="lines",
                name="Z",
                line=dict(width=6),
            )
        )

        # -------------------------------------------------
        # ESCENA
        # -------------------------------------------------

        fig.update_layout(
            title="PyCNC Studio — Virtual CNC",

            scene=dict(

                xaxis=dict(
                    title="X (mm)",
                    range=[-10, 110],
                ),

                yaxis=dict(
                    title="Y (mm)",
                    range=[-10, 80],
                ),

                zaxis=dict(
                    title="Z (mm)",
                    range=[0, 80],
                ),

                aspectmode="manual",

                aspectratio=dict(
                    x=1.5,
                    y=1,
                    z=1,
                ),

                camera=dict(
                    eye=dict(
                        x=1.6,
                        y=1.6,
                        z=1.2,
                    )
                ),
            ),

            margin=dict(
                l=0,
                r=0,
                b=0,
                t=45,
            ),

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0,
            ),
        )

        return fig

    def show(self):

        fig = self.create_figure()

        fig.show()
