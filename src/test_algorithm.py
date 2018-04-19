import unittest
from algorithm import maxim_peaks_above_min_height, maxim_remove_close_peaks


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