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


class TestPeakMethods(unittest.TestCase):

    def test_peaks_above_min_height_three_peaks(self):
        """Should find three peaks above 4."""
        peaks = [1,2,3,4,5,4,3,2,1,2,3,4,5,4,3,2,1,2,3,4,5,3,2,1]
        min_height = 4
        
        peaks_found = maxim_peaks_above_min_height(peaks, min_height)

        expected = [(4, 5), (12, 5), (20, 5)]
        self.assertEqual(expected, peaks_found)

    def test_peaks_above_min_height_no_peaks(self):
        """Should not find peaks above 6."""
        peaks = [1,2,3,4,5,4,3,2,1,2,3,4,5,4,3,2,1,2,3,4,5,3,2,1]
        min_height = 6

        peaks_found = maxim_peaks_above_min_height(peaks, min_height)

        expected = []
        self.assertEqual(expected, peaks_found)

    def test_peaks_above_min_height_one_peak(self):
        """Should find only one peak above 7."""
        peaks = [1,2,3,4,5,4,3,2,1,2,3,4,8,4,3,2,1,2,3,4,5,3,2,1]
        min_height = 7
        
        peaks_found = maxim_peaks_above_min_height(peaks, min_height)

        expected = [(12, 8)]
        self.assertEqual(expected, peaks_found)

    # Moving on to remove close peaks()
    def test_remove_close_peaks_one(self):
        """Should remove one peak."""
        peaks = [(5, 8), (10, 9), (12, 7), (20, 8), (25, 10)]
        min_distance = 3

        peaks_found = maxim_remove_close_peaks(peaks, min_distance)

        expected = [(5, 8), (10, 9), (20, 8), (25, 10)]
        self.assertEqual(expected, peaks_found)

    def test_remove_every_second_peak(self):
        """Should remove the minimal amount of peaks."""
        peaks = [(5, 10), (7, 10), (9, 10), (11, 10), (13, 10), (15, 10), (17, 10)]
        min_distance = 3

        peaks_found = maxim_remove_close_peaks(peaks, min_distance)

        expected = [(5, 10), (9, 10), (13, 10), (17, 10)]
        self.assertEqual(expected, peaks_found)

    def test_remove_every_second_but_not_second_to_last(self):
        """Should remove the minimal amount of peaks, but not all."""
        peaks = [(5, 10), (7, 10), (9, 10), (11, 10), (13, 10), (17, 10)]
        min_distance = 3

        peaks_found = maxim_remove_close_peaks(peaks, min_distance)

        expected = [(5, 10), (9, 10), (13, 10), (17, 10)]
        self.assertEqual(expected, peaks_found)

    def test_remove_all_but_first(self):
        """Should remove the minimal amount of peaks."""
        peaks = [(5, 10), (6, 10), (7, 10), (8, 10)]
        min_distance = 4

        peaks_found = maxim_remove_close_peaks(peaks, min_distance)

        expected = [(5, 10)]
        self.assertEqual(expected, peaks_found)

    def test_remove_none(self):
        """Should not remove one."""
        peaks = [(5, 10)]
        min_distance = 3

        peaks_found = maxim_remove_close_peaks(peaks, min_distance)

        expected = [(5, 10)]
        self.assertEqual(expected, peaks_found)

    def test_remove_none_of_many(self):
        """Should not remove any of two."""
        peaks = [(5, 10), (20, 10)]
        min_distance = 3

        peaks_found = maxim_remove_close_peaks(peaks, min_distance)

        expected = [(5, 10), (20, 10)]
        self.assertEqual(expected, peaks_found)

    def test_remove_nothing_from_a_lot(self):
        """Should not remove any from a loooot"""
        peaks = [(5, 10), (15, 10), (20, 10), (24, 10), (27, 10)]
        min_distance = 3

        peaks_found = maxim_remove_close_peaks(peaks, min_distance)

        expected = [(5, 10), (15, 10), (20, 10), (24, 10), (27, 10)]
        self.assertEqual(expected, peaks_found)

    def test_remove_last_from_a_lot(self):
        """Should remove last from a lot"""
        peaks = [(5, 10), (15, 10), (20, 10), (24, 10), (27, 10), (28, 45)]
        min_distance = 3

        peaks_found = maxim_remove_close_peaks(peaks, min_distance)

        expected = [(5, 10), (15, 10), (20, 10), (24, 10), (27, 10)]
        self.assertEqual(expected, peaks_found)
    
    def test_should_remove_nothing_from_empty(self):
        """Should return empty list if no peaks are given"""
        peaks = []
        min_distance = 3

        peaks_found = maxim_remove_close_peaks(peaks, min_distance)

        expected = []
        self.assertEqual(expected, peaks_found)

if __name__ == '__main__':
    unittest.main()