import unittest

"""Algorithm module to calculate heartrate from
pulse sensor - RD117."""


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
    maxim_find_peaks(an_x, n_th1, 4, 15)


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
    # Order list from large to small
    # [(5, 10), (10, 13), (15, 7), (20, 11)]
    # would be:
    # [(10, 13), (20, 11), (5, 10), (15, 7)]
    #peaks = sorted(peaks, key=lambda x: -x[1])
    filtered_peaks = []
    for i in range(1, len(peaks)):
        # Look at each peaks distance to its previous
        dist_to_previous = peaks[i][0] - peaks[i-1][0]
        if dist_to_previous > min_distance:
            # Keep the previous
            filtered_peaks.append(peaks[i - 1])

    # Also check last peaks distance to previous
    dist_between_last_peaks = peaks[i][0] - peaks[i - 1][0]
    if dist_between_last_peaks > min_distance:
        filtered_peaks.append(peaks[i])

    return filtered_peaks


class TestPeakMethods(unittest.TestCase):

    def test_peaks_above_min_height_three_peaks(self):
        """Should find three peaks above 4."""
        peaks = [1,2,3,4,5,4,3,2,1,2,3,4,5,4,3,2,1,2,3,4,5,3,2,1]
        min_height = 4
        should_find = [(4, 5), (12, 5), (20, 5)]
        peaks_found = maxim_peaks_above_min_height(peaks, min_height)
        self.assertEqual(peaks_found, should_find)

    def test_peaks_above_min_height_no_peaks(self):
        """Should not find peaks above 6."""    
        peaks = [1,2,3,4,5,4,3,2,1,2,3,4,5,4,3,2,1,2,3,4,5,3,2,1]
        min_height = 6
        should_find = []
        peaks_found = maxim_peaks_above_min_height(peaks, min_height)
        self.assertEqual(peaks_found, should_find)

    def test_peaks_above_min_height_one_peak(self):
        """Should find only one peak above 7."""    
        peaks = [1,2,3,4,5,4,3,2,1,2,3,4,8,4,3,2,1,2,3,4,5,3,2,1]
        min_height = 7
        should_find = [(12, 8)]
        peaks_found = maxim_peaks_above_min_height(peaks, min_height)
        self.assertEqual(peaks_found, should_find)

    # Moving on to remove close peaks
    def test_remove_close_peaks(self):
        """Should remove one peak."""    
        peaks = [(5, 8), (10, 9), (12, 7), (20, 8), (25, 10)]
        min_distance = 3
        should_find = [(5, 8), (12, 7), (20, 8), (25, 10)]
        peaks_found = maxim_remove_close_peaks(peaks, min_distance)
        self.assertEqual(peaks_found, should_find)

if __name__ == '__main__':
    unittest.main()