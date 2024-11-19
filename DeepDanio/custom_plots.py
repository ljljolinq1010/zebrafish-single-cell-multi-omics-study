import numpy
import pandas
import matplotlib
from matplotlib import pyplot

import logomaker

import seq_utils

NT_COLOR_DICT = {
    'A': (15/255, 148/255, 71/255),
    'C': (35/255, 63/255, 153/255),
    'G': (245/255, 179/255, 40/255),
    'T': (228/255, 38/255, 56/255),
}

def plot_seq_logo(nt_height=None, pwm=None, seq=None, ax=None, title=None):
    """
    Plot a sequence logo
    
    Input can be specified as a sequence string, pwm matrix, or nucleotide height matrix.

    Parameters
    ----------
    nt_height : numpy.ndarray or None
        Nucleotide height matrix.
    pwm : numpy.ndarray or None
        PWM matrix.
    seq : str or None
        Sequence string.
    ax : matplotlib.Axes or None
        Axes to plot on.
    title : str or None
        Title for the plot.

    Returns
    -------
    matplotlib.Axes
        Axes containing the sequence logo.

    """

    if nt_height is None and seq is None and pwm is None:
        raise ValueError("At least one of nt_height, seq, or pwm must be provided")
    
    # Preference is given to nt_height, then pwm, then seq
    if nt_height is None:
        if pwm is not None:
            # Infer nucleotide heights using information content / entropy
            entropy = numpy.zeros_like(pwm)
            entropy[pwm > 0] = pwm[pwm > 0] * -numpy.log2(pwm[pwm > 0])
            entropy = numpy.sum(entropy, axis=1)
            conservation = 2 - entropy
            # Nucleotide height
            nt_height = numpy.tile(numpy.reshape(conservation, (-1, 1)), (1, 4))
            nt_height = pwm * nt_height
        elif seq is not None:
            # Nucleotide heights from one hot-encoding of sequence
            nt_to_onehot = {'A': [1, 0, 0, 0], 'C': [0, 1, 0, 0], 'G': [0, 0, 1, 0], 'T': [0, 0, 0, 1]}
            nt_height = [nt_to_onehot[c] for c in seq.upper()]
            nt_height = numpy.array(nt_height)

    nt_height_df = pandas.DataFrame(
        nt_height,
        columns=['A', 'C', 'G', 'T'],
    )

    if ax is None:
        fig, ax = pyplot.subplots(figsize=(len(nt_height_df)/20, 0.5))
    
    logo = logomaker.Logo(
        nt_height_df,
        # color_scheme='classic',
        color_scheme=NT_COLOR_DICT,
        ax=ax,
        font_name='Consolas',
    )
    logo.style_spines(visible=False)
    logo.style_spines(spines=['bottom'], visible=True, linewidth=2)
    ax.set_xticks([])
    ax.set_yticks([])
    if title is not None:
        ax.set_title(title)

    return ax


def plot_seq_and_contributions(
        seq,
        contributions_seq,
        cell_states_to_interpret,
        xlim=None,
    ):
    """
    Plot a sequence logo and logos of contributions for each specified cell state.

    Parameters
    ----------
    seq : str
        Sequence string.
    contributions_seq : dict
        Dictionary of contributions (values, 500x4 array) for each cell state (key).
    cell_states_to_interpret : list
        List of cell states whose interpretations to plot.
    xlim : tuple or None
        X-axis limits.

    """
    seq_onehot = seq_utils.one_hot_encode([seq])[0]

    fig, axes = pyplot.subplots(
        1 + len(cell_states_to_interpret), 1,
        sharex=True,
        num=1,
        clear=True,
    )
    if xlim is not None:
        width = (xlim[1] - xlim[0]) / 20
    else:
        width = len(seq_onehot) / 20
    fig.set_size_inches((width, 0.5 + 0.5*len(cell_states_to_interpret)))

    ax = axes[0]
    plot_seq_logo(nt_height=seq_onehot, ax=ax)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    for cell_state_idx, cell_state_to_interpret in enumerate(cell_states_to_interpret):
        ax = axes[cell_state_idx + 1]
        plot_seq_logo(
            nt_height=contributions_seq[cell_state_to_interpret]*seq_onehot,
            ax=ax,
        )
        ax.spines['left'].set_visible(True)
        ax.set_ylabel(cell_state_to_interpret, rotation=0, ha='right')

    # Adjust ylims
    ylim = [numpy.inf, -numpy.inf]
    for ax in axes[1:]:
        ylim[0] = min(ylim[0], ax.get_ylim()[0])
        ylim[1] = max(ylim[1], ax.get_ylim()[1])
    for ax in axes[1:]:
        ax.set_ylim(ylim)
        ax.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
    axes[-1].set_xticks(range(0, len(seq_onehot), 20));

    # Adjust xlim
    if xlim is not None:
        for ax in axes:
            ax.set_xlim(xlim)

    return fig
