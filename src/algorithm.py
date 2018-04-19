"""Algorithm module to calculate heartrate from
pulse sensor - RD117."""

# Constants

# Sample frequency
FS = 25

def max_heart_rate_and_oxygen_sat(ir_buffer, red_buffer):
    """Calculate heart rate and Sp02 level. Keeping close to the original
    horror of 'algorithm.cpp' until we know what it does...
    ir_buffer - list()
    red_buffer - list()
    """
    # calculate DC mean and subtract DC from ir
    ir_mean = sum(ir_buffer) / len(ir_buffer)

    # remove DC and invert signal so that we can
    # use peak detector as valley detector
    an_x = [ir_mean - num for num in ir_buffer]

    # Calculate 4 point moving average
    # OSB! This ignores the last three values!?
    moving = []
    for nums in zip(an_x, an_x[1:], an_x[2:], an_x[3:]):
        moving.append(sum(nums) / 4)

    # Calculate threshold based on the moving average
    n_th1 = sum(moving) / len(ir_buffer)

    # Clamp threshold between 30 and 60 because...?!
    n_th1 = max(min(n_th1, 60), 30)

    # Use peak detector as valley-detector
    peaks = maxim_find_peaks(an_x, n_th1, 4, 15)

    peak_interval_sum = 0
    if len(peaks) >= 2:
        for i in range(1, len(peaks)):
            peak_interval_sum += peaks[i][0] - peaks[i - 1][0]
        peak_interval_sum = peak_interval_sum / len(peaks)
        heart_rate = (FS * 60) / peak_interval_sum
        heart_rate_valid = True
    else:
        # Unable to calculate due to lack of peaks
        heart_rate = -999
        heart_rate_valid = False
    
    # Testing heart rate
    return heart_rate
    # -------------
    # Moving on to SPO2 calculation
    # RED = y   IR = x
    an_x = ir_buffer
    an_y = red_buffer



def maxim_find_peaks(an_x, min_height, min_distance, max_peaks):
    """Find peaks.
    Find at most max_peaks peaks above min_height aka 'n_th1'
    separated by at least min_distance.
    """

    all_peaks = maxim_peaks_above_min_height(an_x, min_height)
    real_peaks = maxim_remove_close_peaks(all_peaks, min_distance)
    return real_peaks


def maxim_peaks_above_min_height(an_x, min_height):
    """Find all peaks above min_height.
    Return a list of tuples containing the index and the value.
    """
    peaks = []
    i = 1
    while i < len(an_x):
        # This STARTS a peak
        if an_x[i] > min_height and an_x[i] > an_x[i-1]:
            width = 1
            # Flat area
            while i + width < len(an_x) and an_x[i] == an_x[i+width]:
                width += 1
            # The peak continues to rise
            if an_x[i] < an_x[i+width]:
                i += 1
            # The peak has ended
            else:
                peaks.append((i, an_x[i]))
                i += width
        i += 1

    return peaks


def maxim_remove_close_peaks(peaks, min_distance):
    """Remove peaks separated by at least min_distance."""
    if not peaks:
        return []

    result = [peaks[0]]
    prev = None
    while peaks:
        curr = peaks.pop(0)
        if prev:
            if curr[0] - prev[0] >= min_distance:
                result.append(curr)
            elif peaks:
                curr = peaks.pop(0)
                if curr[0] - prev[0] >= min_distance:
                    result.append(curr)

        prev = curr

    return result
