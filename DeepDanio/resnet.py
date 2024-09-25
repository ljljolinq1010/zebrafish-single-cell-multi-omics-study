import tensorflow
from tensorflow.keras import layers
from tensorflow.keras import models

def resblock(x, filters, kernel_size, dilation_rate=1, first_conv_activation='relu'):
    """
    TODO: add description
    """
    conv_x = x

    conv_x = layers.BatchNormalization()(conv_x)
    conv_x = layers.Activation(first_conv_activation)(conv_x)
    conv_x = layers.Conv1D(
        filters,
        kernel_size=kernel_size,
        padding='same',
        activation='linear',
        dilation_rate=dilation_rate,
        kernel_initializer='glorot_normal',
    )(conv_x) 

    conv_x = layers.BatchNormalization()(conv_x)
    conv_x = layers.ReLU()(conv_x)
    conv_x = layers.Conv1D(
        filters,
        kernel_size=kernel_size,
        padding='same',
        activation='linear',
        dilation_rate=dilation_rate,
        kernel_initializer='glorot_normal',
    )(conv_x)

    x = layers.add([conv_x, x])

    return x

def resgroup(
        x,
        n_blocks_per_group,
        filters,
        kernel_size,
        dilation_rate=1,
        first_conv_activation='relu',
    ):
    """
    TODO: add description
    """
    for i in range(n_blocks_per_group):
        x = resblock(x, filters, kernel_size, dilation_rate, first_conv_activation)

    return x

def make_model(
        input_seq_length,
        groups=4,
        blocks_per_group=3,
        filters=128,
        kernel_size=13,
        dilation_rates=[1, 2, 4, 8],
        first_conv_activation='relu',
        output_activation='linear',
        n_outputs=8,
    ):

    # Input
    model_input = layers.Input(shape=(input_seq_length, 4))

    skip_convs = []

    # 1x1 convolution w/ linear activation to get to "filters" channels
    # (output dim: batch_size x seq_len x filters)
    x = layers.Conv1D(
        filters,
        kernel_size=1,
        padding='same',
        activation='linear',
        kernel_initializer='glorot_normal',
    )(model_input)
    y = layers.Conv1D(
        filters,
        kernel_size=1,
        padding='same',
    )(x)
    skip_convs.append(y)

    # First actual residual group: activation is different
    # (output dim: batch_size x seq_len x n_filters) <- maybe don't do this?
    x = resgroup(
        x,
        blocks_per_group,
        filters,
        kernel_size,
        dilation_rate=dilation_rates[0],
        first_conv_activation=first_conv_activation,
    )
    y = layers.Conv1D(
        filters,
        kernel_size=1,
        padding='same',
        kernel_initializer='glorot_normal',
    )(x)
    skip_convs.append(y)

    # Remaining residual groups
    # (output dim: batch_size x seq_len x n_filters)
    for i in range(1, groups):
        x = resgroup(
            x,
            blocks_per_group,
            filters,
            kernel_size,
            dilation_rate=dilation_rates[i],
            first_conv_activation='relu',
        )
        y = layers.Conv1D(
            filters,
            kernel_size=1,
            padding='same',
            kernel_initializer='glorot_normal',
        )(x)
        skip_convs.append(y)

    # Final convolutional layer, summed with all the skip connections from previous resgroups
    # (output dim: batch_size x seq_len x n_filters)
    x = layers.Conv1D(
        filters,
        kernel_size=1,
        padding='same',
        kernel_initializer='glorot_normal',
    )(x)

    for i in range(len(skip_convs)):
        x = layers.add([x, skip_convs[i]])

    # x is still (batch_size x seq_len x n_filters)
    # Average across sequence dimension
    # output is (batch_size x n_filters)
    x = layers.GlobalAvgPool1D()(x)

    # Final layer
    regression_output_layer = layers.Dense(
        n_outputs,
        name='dense_regression_output',
        activation=output_activation,
    )
    model_regression_output = regression_output_layer(x)

    model = models.Model(
        model_input,
        model_regression_output,
    )

    return model

def load_model(model_path):
    model = tensorflow.keras.models.load_model(model_path)

    return model
