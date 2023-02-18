import matplotlib.pyplot as plt
import json
import matplotlib
import matplotlib.colors
import re
from collections import Counter


def read_data(file_name):
    with open(f"{file_name}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def create_bar_plot(x_data, y_data, x_label="", y_label="", title="", color_map='Blues'):
    fig, ax = plt.subplots(figsize=(10, 7))
    cmap = plt.cm.get_cmap(color_map)
    norm = matplotlib.colors.Normalize(vmin=min(y_data), vmax=max(y_data))
    color = [cmap(norm(y)) for y in y_data]

    # Convert the x-axis data to strings if they are numbers
    x_data_str = [str(x) if isinstance(x, (int, float)) else x for x in x_data]

    # Add a background grid that shows the x-axis data
    ax.set_facecolor('#f0f0f0')
    ax.xaxis.grid(color='white', linestyle='dashed', linewidth=0.5)
    ax.set_axisbelow(True)

    # Plot the bars and adjust their color
    bars = ax.barh(x_data_str, y_data, color=color, alpha=0.75, edgecolor='grey')

    # Add a custom color bar to the plot
    cbar = plt.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
    cbar.set_label(y_label, fontsize=12)
    cbar.ax.tick_params(labelsize=10)

    # Add data labels to the bars
    for i, bar in enumerate(bars):
        value = y_data[i]
        label = f"{value:.1f}"
        if value < 1:
            label = f"{value:.3f}"
        bar_width = bar.get_width()
        ax.text(bar_width, i, label, fontsize=8, color='black', va='center')

    # Set the axis labels and title
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_title(title, fontsize=16)

    # Remove the top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Adjust the layout of the plot
    plt.tight_layout()

    # Show the plot
    plt.show()


def visualize_parameter(videocards=False):
    data = read_data("parsedsska")
    keys = list(data[0].keys())
    print("\n".join(f"{i}. {key}" for i, key in enumerate(keys)))
    parameter = int(input("select parameter: "))

    models = [item[keys[parameter]] for item in data]

    if videocards:
        models = [max(map(int, re.findall('\d+', model)), default=0) for model in models]

    model_counts = Counter(models)
    sorted_dict = dict(model_counts.most_common())
    x = list(sorted_dict.keys())
    y = list(sorted_dict.values())

    create_bar_plot(x_data=x, y_data=y)
