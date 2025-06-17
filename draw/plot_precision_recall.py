import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


# draw the picture
def draw(data, sv_type, repeat_type):
    data = data[(data["sv_type"].isin(sv_type)) & (data["repeat_type"] == repeat_type)].copy()

    # sort
    softwares = ["varigraph", "EVG", "vg-map", "vg-giraffe", "GraphAligner",
                 "Paragraph", "GraphTyper2", "BayesTyper", "PanGenie"]

    df_mapping = pd.DataFrame({'sort': softwares})
    sort_mapping = df_mapping.reset_index().set_index('sort')
    data['sort'] = data['software'].map(sort_mapping['index'])
    data = data.sort_values(by=['sort'], ascending=True)

    # Define colors for each software
    colors_type = {"varigraph": "#43b494", "EVG": "#75a2d1", "vg-map": "#e7d887",
                   "vg-giraffe": "#e48463", "GraphAligner": "#b3c43a", "Paragraph": "#efa5b6",
                   "GraphTyper2": "#9bd5f1", "BayesTyper": "#ca8eed", "PanGenie": "#525153"}

    # Define default color for software not in the list
    default_color = "#999999"

    # Map software to colors or use default color if software is not in the list
    data['colors'] = data['software'].map(colors_type).fillna(default_color)

    if len(sv_type) > 1:
        hue_type = "sv_type"
    else:
        hue_type = "software"

    sns.scatterplot(x="genotype", y="genotype_precision", data=data, hue="software", palette=colors_type,
                    style=hue_type, markers=True, size="F-measure (F)_genotype", alpha=1, edgecolor="#333333")

    plt.legend(loc="lower center", numpoints=1, bbox_to_anchor=(1.05, 1.0))

    # set X axis
    plt.xlabel("Recall", fontsize="x-large")

    # set Y axis
    plt.ylabel("Precision", fontsize="x-large")

    # set figure information
    plt.title(f"{'_'.join(sv_type)}-{repeat_type}", fontsize="x-large")

    # Draw grid lines behind the scatter plot points
    plt.grid(True, linestyle='--', zorder=0)

    # # Add contour lines
    x = np.linspace(data['genotype'].min(), data['genotype'].max(), 100)
    y = np.linspace(data['genotype_precision'].min(), data['genotype_precision'].max(), 100)
    X, Y = np.meshgrid(x, y)
    Z = np.where((X + Y) != 0, (2 * X * Y) / (X + Y), 0)  # Avoid division by zero
    levels = np.arange(0.1, 1.1, 0.1)
    contours = plt.contour(X, Y, Z, levels=levels, colors='#333333', linestyles='dashed')

    # Annotate contour lines with values
    plt.clabel(contours, inline=True, fontsize=8, fmt='%1.1f')

    # draw the chart
    plt.savefig(f"{'_'.join(sv_type)}-{repeat_type}.pdf")
    plt.show()


# main function
def main():
    data = pd.read_excel("../../merge.xlsx", sheet_name="merge")

    sv_types = [["snp"], ["smallIndel"], ["largeIndel"], ["ins"], ["del"], ["dup"], ["inv"]]
    repeat_types = ["Normal", "Repeat"]

    for sv_type in sv_types:
        for repeat_type in repeat_types:
            draw(data, sv_type, repeat_type)


# function entrance
if __name__ == "__main__":
    main()
