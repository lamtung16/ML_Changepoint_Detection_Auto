# ML_Changepoint_Detection_Auto Report  
**Nov 13, 2024**

- **Overview:**  
  Classification model for changepoint detection on a cancer dataset, classifying segments based on changes in mean.

- **Dataset and Labeling:**
  1. **Label 1:** Segment of size 50 with a change in mean (left mean 0, right mean 1 or -1, standard deviation 0.5).
  2. **Label 0:** Segment of size 50 with no change in mean (mean 0, standard deviation 0.5).
  3. **Preprocessing:** Standardize each segment to the range [0, 1].

- **Model Architecture:**
  1. **Type:** Multilayer Perceptron (MLP)
  2. **Layers:** 
     - Input layer: segment (length: 50)
     - 1st hidden layer: 64 neurons
     - 2nd hidden layer: 32 neurons
     - Output layer: 1 neuron with sigmoid activation

- **Classification Approach:**
  1. **Sliding Window:** Window size of 50 slides across the sequence, classifying each segment as changepoint (1) or no changepoint (0).
  2. **Threshold:** Classification threshold set at 0.5.

- **Results:**
  1. Sequence Length 150 to 500: Good performance.
  2. Sequence Length < 50: Not applicable (window size too large).
  3. Long Sequences (>500): Poor performance.
![Sequence Image](model\auto_cpd_scratch\figures_cancer\sequence_1.6.png)
![Sequence Image](model\auto_cpd_scratch\figures_cancer\sequence_12.2.png)
![Sequence Image](model\auto_cpd_scratch\figures_cancer\sequence_106.5.png)
![Sequence Image](model\auto_cpd_scratch\figures_cancer\sequence_106.6.png)
![Sequence Image](model\auto_cpd_scratch\figures_cancer\sequence_189.1.png)
![Sequence Image](model\auto_cpd_scratch\figures_cancer\sequence_20003.2.png)
![Sequence Image](model\auto_cpd_scratch\figures_cancer\sequence_20092.19.png)

- **Conclusion:**  
  Model performs best when the window size matches the sequence length. Longer sequences require larger windows for effective changepoint detection.

- **Next Steps:**
  1. Experiment with varying window sizes for different sequence lengths.
  2. Explore advanced models (e.g., RNNs) for long sequences.