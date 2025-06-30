import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


# draw the picture
def draw(data, variant):
    data = data[(data["Variant type"] == variant)].copy()

    # sort
    softwares = ["varigraph-C88", "varigraph-Otava", "GATK-C88", "GATK-Otava"]
    repeat_types = ["Normal", "Repeat"]
    genotypes = ["AAAa", "AAaa", "Aaaa", "aaaa", "multi-allelic"]

    software_mapping = pd.DataFrame({'sort_software': softwares})
    software_sort_mapping = software_mapping.reset_index().set_index('sort_software')
    data.loc[:, 'sort_software'] = data['Software'].map(software_sort_mapping['index']).values

    repeat_mapping = pd.DataFrame({'sort_repeat': repeat_types})
    repeat_sort_mapping = repeat_mapping.reset_index().set_index('sort_repeat')
    data.loc[:, 'sort_repeat'] = data['Repeat Type'].map(repeat_sort_mapping['index']).values

    genotype_mapping = pd.DataFrame({'sort_genotype': genotypes})
    genotype_sort_mapping = genotype_mapping.reset_index().set_index('sort_genotype')
    data.loc[:, 'sort_genotype'] = data['Genotype'].map(genotype_sort_mapping['index']).values

    # Sort data by depth and sv_type
    data = data.sort_values(by=['sort_software', 'sort_repeat', 'sort_genotype'], ascending=True)

    # Define colors for each software
    colors_type = {
        "varigraph-C88": "#43b494",
        "varigraph-Otava": "#75a2d1",
        "GATK-C88": "#e7d887",
        "GATK-Otava": "#e48463"
    }

    # Define default color for software not in the list
    default_color = "#999999"

    # Map software to colors or use default color if software is not in the list
    data['colors'] = data['Software'].map(colors_type).fillna(default_color)

    sns.scatterplot(x="Genotype", y="F-measure (F)", data=data, hue="Software", palette=colors_type,
                    style="Repeat Type", markers=True, alpha=1, edgecolor="#333333")

    plt.legend(loc="lower center", numpoints=1, bbox_to_anchor=(1.05, 1.0))

    # set X axis
    plt.xlabel("Recall", fontsize="x-large")

    # set Y axis
    plt.ylabel("Precision", fontsize="x-large")

    # set figure information
    plt.title(f"{variant}", fontsize="x-large")

    # draw the chart
    plt.savefig(f"{variant}.pdf")
    plt.show()


# main function
def main():
    data = pd.read_excel("merge.xls", sheet_name="Dot_plot")

    for variant in ["SNP", "Small indel", "Midsize indel", "Deletion", "Insertion"]:
        draw(data, variant)


# function entrance
if __name__ == "__main__":
    main()
