import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Read data from CSV file
inputfile = "/Users/egonzale/Desktop/temp/GLDS-249/wgs_UMAP_may29th/umap_selected_DA_species/coordinates/coordinates_LAR.txt"
savefolder = "/Users/egonzale/Desktop/temp/GLDS-249/wgs_UMAP_may29th/umap_selected_DA_species/plotly"
outputFileName = "/Users/egonzale/Desktop/temp/GLDS-249/wgs_UMAP_may29th/umap_selected_DA_species/plotly/LAR_interactive_scatter.html"
data = pd.read_csv(inputfile, sep="\t")
data.columns = ["group", "x", "y", "Genus"]

# Unique groups sorted alphabetically with 'ALL' as the first option
groups = ["ALL"] + sorted(list(set(data['group'])))

# Create traces for each group and one for 'ALL'
traces = []
for group in groups:
    if group == "ALL":
        trace = go.Scatter(
            x=data['x'],
            y=data['y'],
            mode='markers',
            name=group,
            text=data['group'],  # Add group information for hover text
            hovertemplate='Group: %{text}<br>X: %{x}<br>Y: %{y}<extra></extra>'
        )
    else:
        filtered_data = data[data['group'] == group]
        trace = go.Scatter(
            x=filtered_data['x'],
            y=filtered_data['y'],
            mode='markers',
            name=group,
            text=filtered_data['group'],  # Add group information for hover text
            hovertemplate='Group: %{text}<br>X: %{x}<br>Y: %{y}<extra></extra>'
        )
    traces.append(trace)

# Create the initial plot
fig = make_subplots()
for trace in traces:
    fig.add_trace(trace)

# Determine the axis ranges
x_range = [min(data['x']), max(data['x'])]
y_range = [min(data['y']), max(data['y'])]

# Update layout for dropdown menu
buttons = []
for i, group in enumerate(groups):
    if group == "ALL":
        visibility = [True] * len(groups)
    else:
        visibility = [i == j for j in range(len(groups))]
    buttons.append(
        dict(
            label=group,
            method='update',
            args=[
                {'visible': visibility},
                {
                    'title': f'Scatter Plot: Group {group}',
                    'xaxis': {
                        'range': x_range,
                        'linecolor': '#f0f0f0',
                        'tickcolor': '#f0f0f0',
                        'gridcolor': '#f0f0f0',
                        'zerolinecolor': '#f0f0f0',
                        'zerolinewidth': 0.5,  # Set the zero line width to match the grid lines
                        'dtick': 5  # Set grid lines at intervals of 5 units
                    },
                    'yaxis': {
                        'range': y_range,
                        'linecolor': '#f0f0f0',
                        'tickcolor': '#f0f0f0',
                        'gridcolor': '#f0f0f0',
                        'zerolinecolor': '#f0f0f0',
                        'zerolinewidth': 0.5,  # Set the zero line width to match the grid lines
                        'dtick': 5  # Set grid lines at intervals of 5 units
                    },
                    'plot_bgcolor': 'rgba(0,0,0,0)',
                    'paper_bgcolor': 'rgba(0,0,0,0)',
                }
            ]
        )
    )

# Add dropdown to the layout
fig.update_layout(
    updatemenus=[
        dict(
            buttons=buttons,
            direction='down',
            showactive=True,
        )
    ],
    title_text='Interactive Scatter Plot',
    xaxis=dict(
        range=x_range,
        showgrid=True,
        zeroline=True,
        linecolor='#f0f0f0',
        tickcolor='#f0f0f0',
        gridcolor='#f0f0f0',
        zerolinecolor='#f0f0f0',
        zerolinewidth=0.5,  # Set the zero line width to match the grid lines
        dtick=5  # Set grid lines at intervals of 5 units
    ),
    yaxis=dict(
        range=y_range,
        showgrid=True,
        zeroline=True,
        linecolor='#f0f0f0',
        tickcolor='#f0f0f0',
        gridcolor='#f0f0f0',
        zerolinecolor='#f0f0f0',
        zerolinewidth=0.5,  # Set the zero line width to match the grid lines
        dtick=5  # Set grid lines at intervals of 5 units
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

# Initial visibility setting: Show all data initially
for i, trace in enumerate(fig.data):
    trace.visible = True

# Save the plot as an HTML file
pio.write_html(fig, file=outputFileName, auto_open=True)
