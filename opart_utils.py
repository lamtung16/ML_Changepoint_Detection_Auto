import numpy as np
import matplotlib.pyplot as plt

# Get cumulative sum vectors
def get_cumsum(sequence):
    y = np.cumsum(sequence)
    z = np.cumsum(np.square(sequence))
    return np.append([0], y), np.append([0], z)


# function to create loss value from 'start' to 'end' given cumulative sum vector y (data) and z (square)
def L(start, end, y, z):
    _y = y[end+1] - y[start]
    _z = z[end+1] - z[start]
    return _z - np.square(_y)/(end-start+1)


# function to get the list of changepoint from vector tau_star
def trace_back(tau_star):
    tau = tau_star[-1]
    chpnt = np.array([len(tau_star)], dtype=int)
    while tau > 0:
        chpnt = np.append(tau, chpnt)
        tau = tau_star[tau-1]
    return np.append(0, chpnt)


# solve opart
def opart(sequence, lda):
    sequence = np.append(0, sequence)
    y, z = get_cumsum(sequence)             # cumsum vector
    sequence_length = len(sequence)-1       # length of sequence

    # Set up
    C = np.zeros(sequence_length + 1)
    C[0] = -lda

    # Get tau_star
    tau_star = np.zeros(sequence_length+1, dtype=int)
    for t in range(1, sequence_length+1):
        V = C[:t] + lda + L(1 + np.arange(t), t, y, z)  # calculate set V
        last_chpnt = np.argmin(V)                       # get optimal tau from set V
        C[t] = V[last_chpnt]                            # update C_i
        tau_star[t] = last_chpnt                        # update tau_star

    set_of_chpnt = trace_back(tau_star[1:])             # get set of changepoints
    return set_of_chpnt[1:-1] - 1


# get mean for each segment
def get_mean(sequence, chpnt):
    mean = np.zeros(len(sequence))
    chpnt = np.append(chpnt, len(sequence)-1)
    chpnt = np.append(-1, chpnt)
    chpnt = chpnt + 1
    for i in range(len(chpnt)-1):
        mean[chpnt[i]:chpnt[i+1]] = np.mean(sequence[chpnt[i]:chpnt[i+1]])
    return mean


# visualization
# def plot_chpnt(sequence, chpnt, plot_mean = False):
#     plt.plot(sequence, marker='o')
#     for position in chpnt:
#         plt.axvline(x=position + 0.5, color='red', linestyle='--', label='Changepoint' if position == chpnt[0] else "")
    
#     if plot_mean:
#         mean = get_mean(sequence, chpnt)
#         plt.plot(mean)

#     plt.legend()
#     plt.show()



def plot_chpnt(signal_df, labels_df, seqID, chpnt, title="", plot_mean=False, figsize=(10,1.5)):
    # Filter the data for the specific sequence ID
    seq_df = signal_df[signal_df['sequenceID'] == seqID]
    seq_label_df = labels_df[(labels_df['sequenceID'] == seqID) | (labels_df['sequenceID'] == (seqID[:-3] + ".F2"))]
    sequence_id = seq_df['sequenceID'].unique()[0][:-3]
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot the signal over the position
    ax.plot(seq_df['position'] - 1, seq_df['signal'], color='blue', label=f"{sequence_id}")

    # Plot changepoints with unique label for the first one
    for i, position in enumerate(chpnt):
        ax.axvline(x=position + 0.5, color='red', linestyle='--', label='Changepoint' if i == 0 else "")
    
    # Plot the mean signal if requested
    if plot_mean:
        mean = get_mean(seq_df['signal'].to_numpy(), chpnt)
        x_values = seq_df['position'] - 1
        ax.plot(x_values, mean, color='green', linestyle='-', label='Mean Signal')
    
    # Define the height for the rectangles as the range of signal values
    signal_min = seq_df['signal'].min()
    signal_max = seq_df['signal'].max()

    # Add rectangles for each labeled region in seq_label_df
    for _, row in seq_label_df.iterrows():
        # Set the rectangle color based on 'changes' column
        color = 'pink' if row['changes'] == 0 else 'red'
        
        # Define start and width for the rectangle
        start = row['start'] - 0.7
        width = (row['end'] - 1.3) - start

        # Draw the rectangle
        ax.add_patch(plt.Rectangle((start, signal_min), width, signal_max - signal_min, color=color, alpha=0.3))

    # Label the axes and add legend
    ax.set_title(title)
    ax.set_xlabel('Position')
    ax.set_ylabel('Signal')
    ax.legend()
    
    # Display and close the plot
    plt.show()
    plt.close(fig)