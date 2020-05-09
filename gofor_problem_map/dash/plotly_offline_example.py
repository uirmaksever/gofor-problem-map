from plotly.offline import plot
import plotly.graph_objects as go

def scatter():
    # Define data
    x1 = [1,2,3,4]
    y1 = [15, 20, 50, 25]

    # Put data in trace
    trace = go.Scatter(
        x = x1,
        y = y1,
    )

    # Create layout specs
    layout = dict(
        title = "Scatter graph",
        xaxis = dict(range=[min(x1), max(x1)]),
        yaxis = dict(range=[min(y1), max(y1)])
    )

    # Put the in plotly figure object
    fig = go.Figure(data=trace, layout=layout)

    # Put the figure in renderable component
    plot_div = plot(fig, output_type="div", include_plotlyjs=False, )
    return plot_div
