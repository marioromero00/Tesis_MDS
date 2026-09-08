"""Controles de informacion y particion del contraste pupilar anidado."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from control_historial import current_control, nested_folds, fixed_fit
from temporales_core import raw_predict


class HistoryControlTests(unittest.TestCase):
    def test_repeat_erases_past_preserves_current_length_padding(self):
        x = np.arange(48, dtype=np.float32).reshape(3, 4, 4)
        lengths = np.array([1, 3, 4])
        z = current_control(x, lengths, 'repeat_current')
        for row, n in enumerate(lengths):
            np.testing.assert_array_equal(z[row, :n], np.tile(x[row, n-1], (n, 1)))
            self.assertTrue((z[row, n:] == 0).all())
        altered = x.copy()
        for row, n in enumerate(lengths):
            altered[row, :n-1] = -999
            altered[row, n:] = 999
        np.testing.assert_array_equal(z, current_control(altered, lengths, 'repeat_current'))
        np.testing.assert_array_equal(x, np.arange(48, dtype=np.float32).reshape(3, 4, 4))

    def test_nested_people_isolation_and_complete_oof_coverage(self):
        frame = pd.DataFrame({'participant':np.repeat([f'P{i}' for i in range(25)], 3), 'split':'train'})
        folds = nested_folds(frame)
        evaluated = []
        for fold in folds:
            self.assertEqual([len(fold[k]) for k in ['fit', 'evaluation', 'inner_fit', 'inner_validation']], [20, 5, 16, 4])
            self.assertTrue(set(fold['fit']).isdisjoint(fold['evaluation']))
            self.assertTrue(set(fold['inner_fit']).isdisjoint(fold['inner_validation']))
            self.assertEqual(set(fold['fit']), set(fold['inner_fit']) | set(fold['inner_validation']))
            evaluated.extend(fold['evaluation'])
        self.assertEqual(sorted(evaluated), sorted(frame.participant.unique()))
        frame.loc[0, 'split'] = 'test'
        with self.assertRaises(ValueError):
            nested_folds(frame)

    def test_fixed_refit_reproducible_for_prescribed_epochs(self):
        x = np.random.default_rng(7).normal(size=(12, 3, 5)).astype(np.float32)
        lengths = np.full(12, 3, dtype=np.int64)
        y = np.tile(np.arange(3), 4)
        config = dict(hidden=4, dropout=.2, learning_rate=.001, weight_decay=.0001, batch_size=6)
        first, history = fixed_fit(x, lengths, y, 'classification', 'BiLSTM', 7, 2, config)
        second, _ = fixed_fit(x, lengths, y, 'classification', 'BiLSTM', 7, 2, config)
        self.assertEqual(len(history), 2)
        self.assertNotIn('validation_macro_score', history[-1])
        np.testing.assert_array_equal(raw_predict(first, x, lengths), raw_predict(second, x, lengths))


if __name__ == '__main__':
    unittest.main()
