import matplotlib.pyplot as plt
import json
import matplotlib
import re
from collections import Counter


def read_data(file_name):
    with open(f"{file_name}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def create_bar_plot(x_data, y_data, x_label="", y_label="", title=""):
    fig, ax = plt.subplots(figsize=(10, 7))
    cmap = plt.cm.get_cmap('Blues')
    norm = matplotlib.colors.Normalize(vmin=min(y_data), vmax=max(y_data))
    color = [cmap(norm(y)) for y in y_data]

    ax.barh(x_data, y_data, color=color, alpha=0.75)
    ax.grid(which='both', axis='x', linewidth=0.5, color='grey', alpha=0.25)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_title(title, fontsize=16)

    for i, v in enumerate(y_data):
        ax.text(v, i, " " + str(v), fontsize=8, color='black', va='center')

    plt.tight_layout()
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
