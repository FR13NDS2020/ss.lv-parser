import matplotlib.pyplot as plt
from collections import Counter
import json
import matplotlib
import re


def reader(file_name):
    with open(f"{file_name}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def barplot(x_data, y_data, x_label="", y_label="count", title=""):
    _, ax = plt.subplots(figsize=(10, 7))

    cmap = plt.cm.get_cmap('Blues')
    norm = matplotlib.colors.Normalize(vmin=min(y_data), vmax=max(y_data))
    color = [cmap(norm(y)) for y in y_data]

    ax.barh(x_data, y_data, color=color, alpha=0.75)

    ax.grid(which='both', axis='x', linewidth=0.5, color='grey', alpha=0.25)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_title(title, fontsize=16)

    # add values to each bar
    for i, v in enumerate(y_data):
        ax.text(v, i, " " + str(v), fontsize=8, color='black', va='center')

    plt.tight_layout()
    plt.show()


def visualize(videocards):
    json_data = reader("parsedsska")
    keys = list(json_data[0].keys())
    print("\n".join(f"{i}. {key}" for i, key in enumerate(keys)))
    parameter = int(input("select parameter: "))

    models = [item[keys[parameter]] for item in json_data]

    if videocards:
        models = [max(map(int, re.findall('\d+', model)), default=0) for model in models]

    c = Counter(models)
    sorted_dict = dict(c.most_common())
    x = list(sorted_dict.keys())
    y = list(sorted_dict.values())

    barplot(x_data=x, y_data=y)