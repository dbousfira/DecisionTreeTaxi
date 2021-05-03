import seaborn as sns
import matplotlib.pyplot as plt
from os import path


FIGURE_PATH = "../reports/figures/"


def pairplot(df):

    if path.exists(f"{FIGURE_PATH}pairplot.png"):
        return

    height = 0.375 * df.shape[1]
    sns_plot = sns.pairplot(df, height=height)
    sns_plot.savefig(f"{FIGURE_PATH}pairplot.png")

    plt.clf()  # Clean parirplot figure from sns