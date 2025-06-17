import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# draw the picture
def draw(data, sv_type):
    data = data[(data["sv_type"] == sv_type)].copy()
    print(data)

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

    colors_type = {"Biallelic": "#e48463", "Multiallelic": "#75a2d1"}

    # set X axis
    plt.xlabel("Software", fontsize="x-large")

    # set Y axis
    plt.ylabel("Precision", fontsize="x-large")

    # set figure information
    plt.title(f"{sv_type}", fontsize="x-large")

    # Draw the bar plot
    ax = sns.barplot(
        x="software",
        y="F-measure (F)_genotype",
        data=data,
        hue="Biallelic/Multiallelic",
        palette=colors_type,
        edgecolor="#333333"
    )

    plt.xticks(rotation=45)  # Rotate x labels for better readability

    # Add Y values on top of each bar
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=10)

    # Draw grid lines behind the scatter plot points
    plt.grid(True, linestyle='--', zorder=0)

    # Save the plot
    plt.savefig(f"{sv_type}.pdf")
    plt.show()


# main function
def main():
    data = pd.read_excel("../../merge.xlsx", sheet_name="Bia-Mul")

    sv_types = ["SNPs", "1-19", "20-49", "Deletion", "Insertion"]

    for sv_type in sv_types:
        draw(data, sv_type)


# function entrance
if __name__ == "__main__":
    main()
