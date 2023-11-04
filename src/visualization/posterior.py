import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import corner

import schemas.visualization
import visualization.base as base


def plot_mass_estimates(df: pd.DataFrame, label: str, output_dir=None, close=True) -> None:
    """
    Plot the distribution of the estimated masses.
    
    Parameters
    ----------
    df : pd.DataFrame
        Posterior.
    label : str
        Posterior label.
    output_dir : str, optional
        Output directory.
    close : bool, optional
        Whether to close the figure.
    
    Returns
    -------
    None
    """
    labels = schemas.visualization.Labels("Distribution of Estimated Masses", "Mass $(M_{\odot})$", "Density")
    _, ax = base.initialize_plot(figsize=(9, 4), labels=labels)
    col_to_labels = {"mf": f"{label}: ", "m_p1": "Heavier Parent: ", "m_p2": "Ligher Parent: "}

    for col, label in col_to_labels.items():
        density, bins = np.histogram(a=df[col], density=True)
        inv_low, med, inv_high = df[col].quantile(0.05), df[col].quantile(0.5), df[col].quantile(0.95)
        ax.stairs(density, bins, label="%s: $%d_{-%d}^{+%d}$ %s" % (label, med, inv_low, inv_high, "($M_{\odot}$)"))
        sns.histplot(df[col], ax=ax, element="step", fill=False, stat="density", label=label))

    plt.ylabel(""), plt.xlabel("")
    plt.legend()
    base.savefig_and_close(f"{label}_mass_estimates.png", output_dir, close)


def plot_corner(
    df: pd.DataFrame,
    label: str,
    levels=[0.68, 0.9],
    nbins=70,
    output_dir=None,
    close=True
) -> None:
    """
    Plot the posterior corner plot.
    
    Parameters
    ----------
    df : pd.DataFrame
        Posterior.
    label : str
        Posterior label.
    levels : list, optional
        The contour levels, by default [0.68, 0.9].
    nbins : int, optional
        The number of bins, by default 70.
    output_dir : str, optional
        Output directory.
    close : bool, optional
        Whether to close the figure.

    Returns
    -------
    None
    """
    corner.corner(
        df,
        nbins,
        var_names=["vf", "m1", "m2", "chif"],
        labels=["$v_f$", "$m_1$", "$m_2$", "$\chi_f$"],
        levels=levels,
        plot_density=True,
        plot_samples=False,
        color="blue",
        fill_contours=False,
        smooth=True,
        plot_datapoints=False,
        hist_kwargs=dict(density=True)
    )
    base.savefig_and_close(f"{label}_corner.png", output_dir, close)