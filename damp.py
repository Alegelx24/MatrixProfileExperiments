import numpy as np
from scipy.signal import correlate
from scipy.fftpack import fft, ifft

def DAMP_2_0(T, SubsequenceLength, location_to_start_processing, lookahead=None, enable_output=True):
    # Set default values for parameters
    if lookahead is None:
        lookahead = 2**int(np.log2(16 * SubsequenceLength))

    if enable_output:
        print("------------------------------------------")
        print("Thank you for using DAMP.")
        print("This is version 2.0 of DAMP, please email Eamonn Keogh (eamonn@cs.ucr.edu) or Yue Lu (ylu175@ucr.edu) "
              "to make sure you have the latest version.")
        print(f"This time series is of length {len(T)}, and the subsequence length you chose is {SubsequenceLength}.")

        if lookahead != 0 and lookahead != 2**int(np.log2(lookahead)):
            lookahead = 2**int(np.log2(lookahead))
            print(f"The lookahead is {lookahead} (we use the nearest power of two to your input).")
        else:
            print(f"The lookahead is {lookahead}.")

        print("Hints:")
        print("In most cases, the subsequence length you should use is between about 50 to 90% of a typical period.")
        print("A good initial value of lookahead is about 2^nearest_power_of_two(16 times S). "
              "The range of lookahead should be 0 to length(T)-location_to_start_processing.")
        print("If speed is important, you can tune lookahead to get greater speed-up in your domain. A simple search, "
              "doubling and halving the current value should let you quickly converge on a good value.")
        print("------------------------------------------\n")

    # Handle invalid inputs
    # 1. Constant Regions
    if contains_constant_regions(T, SubsequenceLength):
        raise ValueError("ERROR: This dataset contains constant and/or near constant regions. "
                         "Such regions can cause both false positives and false negatives depending on how you define anomalies. "
                         "And more importantly, it can also result in imaginary numbers in the calculated Left Matrix Profile, "
                         "from which we cannot get the correct score value and position of the top discord. ** The program has been terminated. **")

    # 2. Location to Start Processing
    if location_to_start_processing / SubsequenceLength < 4:
        print("WARNING:")
        print("location_to_start_processing/SubsequenceLength is less than four. We recommend that you allow DAMP "
              "to see at least four cycles, otherwise you may get false positives early on. If you have training data from the "
              "same domain, you can prepend the training data, like this Data = [trainingdata, testdata], and call DAMP(data, "
              "S, len(trainingdata))")
        if location_to_start_processing < SubsequenceLength:
            print("location_to_start_processing cannot be less than the subsequence length")
            print(f"location_to_start_processing has been set to {SubsequenceLength}")
            location_to_start_processing = SubsequenceLength
        print("------------------------------------------\n")
    elif location_to_start_processing > (len(T) - SubsequenceLength + 1):
        print("WARNING:")
        print("location_to_start_processing cannot be greater than len(T) - S + 1")
        location_to_start_processing = (len(T) - SubsequenceLength + 1)
        print(f"location_to_start_processing has been set to {location_to_start_processing}")
        print("------------------------------------------\n")

    # 3. Subsequence length
    if SubsequenceLength <= 10 or SubsequenceLength > 1000:
        autocor = np.correlate(T, T, mode='full')
        lags = np.arange(-len(T) + 1, len(T))
        autocor = autocor[lags >= 3010]
        ReferenceSubsequenceLength = np.argmax(autocor) + 3010
        ReferenceSubsequenceLength = np.floor(ReferenceSubsequenceLength)

        print("WARNING:")
        print("The subsequence length you set may be too large or too small")
        print(f"For the current input time series, we recommend setting the subsequence length to {ReferenceSubsequenceLength}")
        print("------------------------------------------\n")

    # Initialization
    Left_MP = np.zeros_like(T, dtype=float)
    best_so_far = -np.inf
    bool_vec = np.ones(len(T), dtype=bool)

    # Handle the prefix to get a relatively high best so far discord score
    for i in range(location_to_start_processing, location_to_start_processing + (16 * SubsequenceLength)):
        if not bool_vec[i]:
            Left_MP[i] = Left_MP[i - 1] - 0.00001
            continue

        if i + SubsequenceLength - 1 >= len(T):
            break

        query = T[i:i + SubsequenceLength]
        Left_MP[i] = np.min(MASS_V2(T[:i+SubsequenceLength-1], query))
        best_so_far = max(Left_MP)

        if lookahead != 0:
            start_of_mass = min(i + SubsequenceLength, len(T))
            end_of_mass = min(start_of_mass + lookahead - 1, len(T))
            if (end_of_mass - start_of_mass + 1) > SubsequenceLength:
                distance_profile = MASS_V2(T[start_of_mass:end_of_mass], query)
                dp_index_less_than_BSF = np.where(distance_profile < best_so_far)[0]
                ts_index_less_than_BSF = dp_index_less_than_BSF + start_of_mass - 1
                bool_vec[ts_index_less_than_BSF] = False

    # Remaining test data except for the prefix
    for i in range(location_to_start_processing + (16 * SubsequenceLength) + 1, len(T) - SubsequenceLength + 1):
        if not bool_vec[i]:
            Left_MP[i] = Left_MP[i - 1] - 0.00001
            continue

        approximate_distance = np.inf
        X = 2**int(np.log2(8 * SubsequenceLength))
        flag = 1
        expansion_num = 0

        if i + SubsequenceLength - 1 >= len(T):
            break

        query = T[i:i + SubsequenceLength]

        while approximate_distance >= best_so_far:
            if i - X + 1 + (expansion_num * SubsequenceLength) < 1:
                approximate_distance = np.min(MASS_V2(T[:i], query))
                Left_MP[i] = approximate_distance
                if approximate_distance > best_so_far:
                    best_so_far = approximate_distance
                break
            else:
                if flag == 1:
                    flag = 0
                    approximate_distance = np.min(MASS_V2(T[i - X + 1:i], query))
                else:
                    X_start = i - X + 1 + (expansion_num * SubsequenceLength)
                    X_end = i - (X // 2) + (expansion_num * SubsequenceLength)
                    approximate_distance = np.min(MASS_V2(T[X_start:X_end], query))

                if approximate_distance < best_so_far:
                    Left_MP[i] = approximate_distance
                    break
                else:
                    X *= 2
                    expansion_num += 1

        if lookahead != 0:
            start_of_mass = min(i + SubsequenceLength, len(T))
            end_of_mass = min(start_of_mass + lookahead - 1, len(T))
            if (end_of_mass - start_of_mass + 1) > SubsequenceLength:
                distance_profile = MASS_V2(T[start_of_mass:end_of_mass], query)
                dp_index_less_than_BSF = np.where(distance_profile < best_so_far)[0]
                ts_index_less_than_BSF = dp_index_less_than_BSF + start_of_mass - 1
                bool_vec[ts_index_less_than_BSF] = False

    # Get pruning rate
    PV = bool_vec[location_to_start_processing:(len(T) - SubsequenceLength + 1)]
    PR = (len(PV) - np.sum(PV)) / len(PV)

    # Get top discord
    discord_score = np.max(Left_MP)
    position = np.argmax(Left_MP)

    # Outputs
    if enable_output:
        print("Results:")
        print(f"Pruning Rate: {PR}")
        print(f"Predicted discord score/position: {discord_score}/{position}")
        print("\n* If you want to suppress the outputs, please call DAMP using the following format:")
        print(">> discord_score, position = DAMP_2_0(T, SubsequenceLength, location_to_start_processing, enable_output=False)\n")

    # Create the plot
    import matplotlib.pyplot as plt

    plt.figure(num='UCR DAMP 2.0')
    plt.plot(Left_MP / np.max(Left_MP), 'b')
    plt.plot((T - np.min(T)) / (np.max(T) - np.min(T)) + 1.1, 'r')
    plt.show()

    return discord_score, position

def MASS_V2(x, y):
    # x is the data, y is the query
    m = len(y)
    n = len(x)

    # Compute y stats -- O(n)
    meany = np.mean(y)
    sigmay = np.std(y, ddof=1)  # Use ddof=1 for sample standard deviation

    # Compute x stats -- O(n)
    meanx = np.convolve(x, np.ones(m) / m, mode='valid')
    sigmax = np.sqrt(np.convolve(x**2, np.ones(m) / m, mode='valid') - meanx**2)

    y = y[::-1]  # Reverse the query
    y = np.pad(y, (0, n - m), 'constant')  # Append zeros to match the length of x

    # The main trick of getting dot products in O(n log n) time
    X = np.fft.fft(x)
    Y = np.fft.fft(y)
    Z = X * Y.conjugate()
    z = np.fft.ifft(Z)

    dist = 2 * (m - (z[m - 1:] - m * meanx * meany) / (sigmax * sigmay))
    dist = np.sqrt(dist)
    
    return dist

def contains_constant_regions(T, SubsequenceLength):
    constant_indices = np.where(np.diff(T) == 0)[0]
    constant_length = np.max(np.diff(constant_indices))
    return constant_length >= SubsequenceLength or np.var(T) < 0.2

# Example usage:
# discord_score, position = DAMP_2_0(T, SubsequenceLength, location_to_start_processing, lookahead=YourLookaheadValue)

if __name__ == '__main__':


    # Specifica il percorso del file contenente i dati
    file_path = "/Users/aleg2/Downloads/ydata-labeled-time-series-anomalies-v1_0/A1Benchmark/real_1.csv"  # Sostituisci con il percorso reale del tuo file

    # Load the data from the CSV file, skipping the first row (header)
    T = np.loadtxt(file_path, delimiter=',', skiprows=1)
    SubsequenceLength=200
    location_to_start_processing=0
    lookahead=0
    discord_score, position = DAMP_2_0(T, SubsequenceLength, location_to_start_processing, lookahead)
