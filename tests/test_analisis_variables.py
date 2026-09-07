import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
from analisis_variables import shift_indices, score, subject_scores


class TestAnalisisVariables(unittest.TestCase):
    def test_shift_preserves_segments_and_joint_feature_relationship(self):
        frame = pd.DataFrame({'participant': ['P1'] * 8 + ['P2'] * 5,
                              'recording': ['r'] * 13,
                              'segment_id': [1] * 4 + [2] * 4 + [1] * 5})
        ix = shift_indices(frame, 7)
        np.testing.assert_array_equal(np.sort(ix), np.arange(len(frame)))
        pd.testing.assert_frame_equal(frame, frame.iloc[ix].reset_index(drop=True))
        self.assertTrue(np.all(ix != np.arange(len(frame))))
        x = np.arange(len(frame))
        pair = np.column_stack([x, 2 * x])
        np.testing.assert_array_equal(pair[ix, 1], 2 * pair[ix, 0])
        np.testing.assert_array_equal(ix, shift_indices(frame, 7))

    def test_singleton_and_two_window_segments(self):
        frame = pd.DataFrame({'participant': ['P1'] * 3, 'recording': ['r'] * 3,
                              'segment_id': [1, 2, 2]})
        np.testing.assert_array_equal(shift_indices(frame, 7), [0, 2, 1])

    def test_participant_weighting_does_not_favor_long_recording(self):
        frame = pd.DataFrame({'participant': ['P1'] * 100 + ['P2'] * 2,
                              'target': ['alto', 'bajo'] * 51})
        pred = frame.target.to_numpy().copy()
        pred[-2:] = ['bajo', 'alto']
        np.testing.assert_array_equal(subject_scores(frame, pred, 'target', 'classification'), [1, 0])
        self.assertGreater(score(frame.target, pred, 'classification'), .98)

    def test_known_predictive_feature_loses_score_under_shift(self):
        frame = pd.DataFrame({'participant': ['P1'] * 100, 'recording': ['r'] * 100,
                              'segment_id': [1] * 100})
        signal = np.arange(100, dtype=float)
        shifted = signal[shift_indices(frame, 9)]
        self.assertEqual(score(signal, signal, 'regression'), 0)
        self.assertLess(score(signal, shifted, 'regression'), -100)


if __name__ == '__main__':
    unittest.main()
