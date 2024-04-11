import plotly.graph_objects as go


def plot(results, df):
    """Custom plot function to visualize trade entries and exits with indicators"""
    # Prepare the data
    indicators = results._strategy._indicators
    trades = results["_trades"]

    # Filter entries and exits
    long_entries = trades.loc[trades.Size > 0, "EntryTime"]
    long_entry_prices = trades.loc[trades.Size > 0, "EntryPrice"]
    short_entries = trades.loc[trades.Size < 0, "EntryTime"]
    short_entry_prices = trades.loc[trades.Size < 0, "EntryPrice"]

    long_exits = trades.loc[trades.Size > 0, "ExitTime"]
    long_exit_prices = trades.loc[trades.Size > 0, "ExitPrice"]
    short_exits = trades.loc[trades.Size < 0, "ExitTime"]
    short_exit_prices = trades.loc[trades.Size < 0, "ExitPrice"]

    # Create a line plot for the asset's price data
    price_trace = go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        line=dict(color="blue", width=2),
        name="Price",
    )

    # Create a scatter plot for long (buy) entries
    long_entry_trace = go.Scatter(
        x=long_entries,
        y=long_entry_prices,
        mode="markers",
        marker=dict(color="black", size=10),
        name="Long Entry",
        hoverinfo="text",
        text=long_entries,  # Show entry time on hover
    )

    # Create a scatter plot for exit trades
    exit_long_trace = go.Scatter(
        x=long_exits,
        y=long_exit_prices,
        mode="markers",
        marker=dict(color="green", size=10),
        name="Long Exit",
        hoverinfo="text",
        text=long_exits,  # Show exit time on hover
    )

    # Create a scatter plot for short (sell) entries
    short_entry_trace = go.Scatter(
        x=short_entries,
        y=short_entry_prices,
        mode="markers",
        marker=dict(color="orange", size=10),
        name="Short Entry",
        hoverinfo="text",
        text=short_entries,  # Show entry time on hover
    )

    # Create a scatter plot for short (sell) exit trades
    exit_short_trace = go.Scatter(
        x=short_exits,
        y=short_exit_prices,
        mode="markers",
        marker=dict(color="red", size=10),
        name="Short Exit",
        hoverinfo="text",
        text=short_exits,  # Show exit time on hover
    )

    # Combine the plots
    fig = go.Figure(
        data=[
            price_trace,
            long_entry_trace,
            short_entry_trace,
            exit_long_trace,
            exit_short_trace,
        ]
    )

    # Plot each indicator dynamically
    for _, value in enumerate(indicators):
        fig.add_trace(go.Scatter(x=df.index, y=value, mode="lines", name=value.name))

    # Customize layout with a white background
    fig.update_layout(
        title="Trade Entries and Exits",
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="closest",
        plot_bgcolor="white",
        xaxis=dict(linecolor="black"),
        yaxis=dict(linecolor="black"),
    )

    # Set the grid color
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="lightgrey")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgrey")

    # Show the plot
    fig.show()
