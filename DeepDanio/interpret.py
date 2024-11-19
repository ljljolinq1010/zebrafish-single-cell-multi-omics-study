import numpy

import tensorflow

from deeplift.dinuc_shuffle import dinuc_shuffle
import shap

import seq_utils

# The following was adapted from 
# https://github.com/AvantiShri/colab_notebooks/blob/ecf2909528ff47dbc36c87666b44520f07cbaab2/labmeeting/Oct18/DeepSHAP_Unimodal_Input.ipynb

def dinuc_shuffle_several_times(list_containing_input_modes_for_an_example, seed=1234, n_shuffled_seqs=10):
    assert len(list_containing_input_modes_for_an_example)==1
    onehot_seq = list_containing_input_modes_for_an_example[0]
    rng = numpy.random.RandomState(seed)
    to_return = numpy.array([dinuc_shuffle(onehot_seq, rng=rng) for i in range(n_shuffled_seqs)])
    return [to_return] #wrap in list for compatibility with multiple modes
  
def combine_mult_and_diffref(mult, orig_inp, bg_data):
    assert len(orig_inp)==1
    projected_hypothetical_contribs = numpy.zeros_like(bg_data[0]).astype("float")
    assert len(orig_inp[0].shape)==2
    #At each position in the input sequence, we iterate over the one-hot encoding
    # possibilities (eg: for genomic sequence, this is ACGT i.e.
    # 1000, 0100, 0010 and 0001) and compute the hypothetical 
    # difference-from-reference in each case. We then multiply the hypothetical
    # differences-from-reference with the multipliers to get the hypothetical contributions.
    #For each of the one-hot encoding possibilities,
    # the hypothetical contributions are then summed across the ACGT axis to estimate
    # the total hypothetical contribution of each position. This per-position hypothetical
    # contribution is then assigned ("projected") onto whichever base was present in the
    # hypothetical sequence.
    #The reason this is a fast estimate of what the importance scores *would* look
    # like if different bases were present in the underlying sequence is that
    # the multipliers are computed once using the original sequence, and are not
    # computed again for each hypothetical sequence.
    for i in range(orig_inp[0].shape[-1]):
        hypothetical_input = numpy.zeros_like(orig_inp[0]).astype("float")
        hypothetical_input[:,i] = 1.0
        hypothetical_difference_from_reference = (hypothetical_input[None,:,:]-bg_data[0])
        hypothetical_contribs = hypothetical_difference_from_reference*mult[0]
        projected_hypothetical_contribs[:,:,i] = numpy.sum(hypothetical_contribs,axis=-1) 
    return [numpy.mean(projected_hypothetical_contribs,axis=0)]

def compute_contribution_scores(
        seq,
        model,
        cell_state_to_interpret,
        cell_states_all=None,
        ref_seqs=None,
        ref_dinuc_seed=1234,
        ref_dinuc_n_seqs=10,
    ):

    # If ref_seqs not provided, use dinuc shuffled sequences
    if ref_seqs is None:
        ref_data = lambda x: dinuc_shuffle_several_times(
            x, seed=ref_dinuc_seed, n_shuffled_seqs=ref_dinuc_n_seqs,
        )
    else:
        ref_data = seq_utils.one_hot_encode(ref_seqs)

    cell_state_idx = cell_states_all.index(cell_state_to_interpret)

    # One-hot encode sequence
    seqs_onehot = seq_utils.one_hot_encode([seq])

    # Initializing model
    print("Initializing model...")
    model_cell_state = tensorflow.keras.Model(inputs=model.inputs, outputs=model.layers[-1].output[:, cell_state_idx])

    # Initialize shap
    shap.explainers._deep.deep_tf.op_handlers["AddV2"] = shap.explainers._deep.deep_tf.passthrough
    shap.explainers._deep.deep_tf.op_handlers["BatchToSpaceND"] = shap.explainers._deep.deep_tf.linearity_1d(0)
    shap.explainers._deep.deep_tf.op_handlers["SpaceToBatchND"] = shap.explainers._deep.deep_tf.linearity_1d(0)
    explainer = shap.DeepExplainer(
        model=model_cell_state,
        data=ref_data,
        combine_mult_and_diffref=combine_mult_and_diffref,
    )

    # Run shap
    print("Running shap...")
    # raw_contributions has shape (n_samples, seq_len, 4)
    raw_contributions = explainer.shap_values(seqs_onehot, check_additivity=False)

    return raw_contributions[0]
