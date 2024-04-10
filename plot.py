import plotly.graph_objects as go


def plot(results, df):
    """Custom plot function to visualize trade entries and exits"""
    # Prepare the data
    indicators = results._strategy._indicators
    trades = results["_trades"]
    # Separate entries and exits
    entry_times = trades["EntryTime"]
    entry_prices = trades["EntryPrice"]
    exit_times = trades["ExitTime"]
    exit_prices = trades["ExitPrice"]

    # Create a line plot for the asset's price data
    price_trace = go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        line=dict(color="blue", width=2),
        name="Price",
    )

    # Create a scatter plot for entry trades
    entry_trace = go.Scatter(
        x=entry_times,
        y=entry_prices,
        mode="markers",
        marker=dict(color="yellow", size=10),
        name="Entry of Trade",
        hoverinfo="text",
        text=entry_times,  # Show entry time on hover
    )

    # Create a scatter plot for exit trades
    exit_trace = go.Scatter(
        x=exit_times,
        y=exit_prices,
        mode="markers",
        marker=dict(color="green", size=10),
        name="Exit of Trade",
        hoverinfo="text",
        text=exit_times,  # Show exit time on hover
    )

    # Combine the plots
    fig = go.Figure(data=[price_trace, entry_trace, exit_trace])

    # Plot each indicator
    for i, value in enumerate(indicators):
        fig.add_trace(go.Scatter(x=df.index, y=value, mode="lines", name=value.name))

    # Customize layout with a white background
    fig.update_layout(
        title="Trade Entries and Exits",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="closest",  # Update hover mode
        plot_bgcolor="white",  # Set the background color to white
        xaxis=dict(linecolor="black"),  # Set x-axis line color to black for visibility
        yaxis=dict(linecolor="black"),  # Set y-axis line color to black for visibility
    )

    # Set the grid color
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="lightgrey")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgrey")

    # Show the plot
    fig.show()
