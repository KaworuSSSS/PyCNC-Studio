import plotly.graph_objects as go


class CNCView:

    def __init__(self, simulator):

        self.simulator = simulator

    def show(self):

        status = self.simulator.get_status()

        position = status["position"]

        toolpath = self.simulator.get_toolpath()

        fig = go.Figure()

        # -------------------------------------------------
        # Mesa CNC
        # -------------------------------------------------

        fig.add_trace(
            go.Mesh3d(
                x=[
                    0, 100, 100, 0,
                    0, 100, 100, 0
                ],
                y=[
                    0, 0, 60, 60,
                    0, 0, 60, 60
                ],
                z=[
                    0, 0, 0, 0,
                    -5, -5, -5, -5
                ],
                i=[0, 0, 0, 4, 4, 4],
                j=[1, 2, 3, 5, 6, 7],
                k=[2, 3, 1, 6, 7, 5],
                opacity=0.35,
                name="Mesa",
                hoverinfo="name",
            )
        )

        # -------------------------------------------------
        # Material
        # -------------------------------------------------

        fig.add_trace(
            go.Mesh3d(
                x=[
                    10, 90, 90, 10,
                    10, 90, 90, 10
                ],
                y=[
                    10, 10, 50, 50,
                    10, 10, 50, 50
                ],
                z=[
                    0, 0, 0, 0,
                    10, 10, 10, 10
                ],
                i=[0, 0, 0, 4, 4, 4],
                j=[1, 2, 3, 5, 6, 7],
                k=[2, 3, 1, 6, 7, 5],
                opacity=0.5,
                name="Material",
                hoverinfo="name",
            )
        )

        # -------------------------------------------------
        # Trayectoria
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
                    line=dict(
                        width=6
                    ),
                    marker=dict(
                        size=4
                    ),
                )
            )

        # -------------------------------------------------
        # Herramienta
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
                    size=10,
                    symbol="diamond",
                ),
            )
        )

        # -------------------------------------------------
        # Eje de herramienta
        # -------------------------------------------------

        fig.add_trace(
            go.Scatter3d(
                x=[
                    tool_x,
                    tool_x
                ],
                y=[
                    tool_y,
                    tool_y
                ],
                z=[
                    tool_z,
                    tool_z - 8
                ],
                mode="lines",
                name="Spindle",
                line=dict(
                    width=8
                ),
                showlegend=False,
            )
        )

        # -------------------------------------------------
        # Ejes
        # -------------------------------------------------

        fig.add_trace(
            go.Scatter3d(
                x=[0, 30],
                y=[0, 0],
                z=[-6, -6],
                mode="lines",
                name="X",
                line=dict(width=5),
            )
        )

        fig.add_trace(
            go.Scatter3d(
                x=[0, 0],
                y=[0, 30],
                z=[-6, -6],
                mode="lines",
                name="Y",
                line=dict(width=5),
            )
        )

        fig.add_trace(
            go.Scatter3d(
                x=[0, 0],
                y=[0, 0],
                z=[-6, 24],
                mode="lines",
                name="Z",
                line=dict(width=5),
            )
        )

        # -------------------------------------------------
        # Configuración
        # -------------------------------------------------

        fig.update_layout(
            title="PyCNC Studio — CNC Virtual 3D",

            scene=dict(
                xaxis=dict(
                    title="X (mm)",
                    range=[-10, 110],
                ),

                yaxis=dict(
                    title="Y (mm)",
                    range=[-10, 70],
                ),

                zaxis=dict(
                    title="Z (mm)",
                    range=[-15, 30],
                ),

                aspectmode="manual",

                aspectratio=dict(
                    x=1.5,
                    y=1,
                    z=0.6,
                ),
            ),

            margin=dict(
                l=0,
                r=0,
                b=0,
                t=40,
            ),
        )

        fig.show()
