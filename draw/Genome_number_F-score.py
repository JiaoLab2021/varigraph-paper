import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns


# draw the picture
def draw(data, sv_type):
    data = data[(data["sv_type"] == sv_type)].copy()

    # sort
    genome_numbers = ["top1", "top32", "top64", "top127", "top252"]
    softwares = ["varigraph", "EVG", "vg-map", "vg-giraffe", "GraphAligner",
                 "Paragraph", "GraphTyper2", "BayesTyper", "PanGenie"]

    df_mapping = pd.DataFrame({'sort': genome_numbers})
    sort_mapping = df_mapping.reset_index().set_index('sort')
    data['sort'] = data['Number'].map(sort_mapping['index'])
    data = data.sort_values(by=['sort'], ascending=True)

    df_mapping1 = pd.DataFrame({'sort1': softwares})
    sort_mapping1 = df_mapping1.reset_index().set_index('sort1')
    data['sort1'] = data['software'].map(sort_mapping1['index'])
    data = data.sort_values(by=['sort', 'sort1'], ascending=True)

    # Define colors for each software
    colors_type = {"varigraph": "#43b494", "EVG": "#75a2d1", "vg-map": "#e7d887",
                   "vg-giraffe": "#e48463", "GraphAligner": "#b3c43a", "Paragraph": "#efa5b6",
                   "GraphTyper2": "#9bd5f1", "BayesTyper": "#ca8eed", "PanGenie": "#525153"}

    sns.lineplot(x="Number", y="F-measure (F)_genotype", data=data, hue="software", style="software",
                 markers=True, dashes=False, palette=colors_type, alpha=1, ci='sd')

    plt.legend(loc="lower center", numpoints=1, bbox_to_anchor=(0.6, 0.01))

    # set X axis
    plt.xlabel("Genome number", fontsize="x-large")

    # set Y axis
    plt.ylabel("F-measure (F)", fontsize="x-large")

    # set figure information
    plt.title(f"{sv_type}", fontsize="x-large")

    # draw the chart
    plt.savefig(f"{sv_type}.pdf")
    plt.show()


# main function
def main():
    data = pd.read_excel("../../merge.xlsx", sheet_name="Number")

    sv_types = ["snp", "smallIndel", "largeIndel", "del", "ins"]

    for sv_type in sv_types:
        draw(data, sv_type)


# function entrance
if __name__ == "__main__":
    main()
