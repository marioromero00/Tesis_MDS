import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
from estabilidad_variables import PRIORITY, compact_columns, candidates, folds_for_train, summarize_subjects
from baselines_estaticos import EEG, GSR, EYE, PUPIL


class TestEstabilidad(unittest.TestCase):
    def test_folds_hold_out_each_participant_once(self):
        frame = pd.DataFrame({'participant': np.repeat([f'P{i}' for i in range(25)], 3), 'split': 'train'})
        seen = []
        for fit, evaluation in folds_for_train(frame):
            self.assertTrue(set(frame.iloc[fit].participant).isdisjoint(frame.iloc[evaluation].participant))
            self.assertEqual(frame.iloc[evaluation].participant.nunique(), 5)
            seen.extend(evaluation)
        self.assertEqual(sorted(seen), list(range(len(frame))))
        frame.loc[0, 'split'] = 'test'
        with self.assertRaises(ValueError):
            folds_for_train(frame)

    def test_compact_removes_duplicate_and_constant_without_quality(self):
        frame = pd.DataFrame(np.random.default_rng(1).normal(size=(100, len(PRIORITY))), columns=PRIORITY)
        frame['eeg_std_uv'] = frame.eeg_rms_uv * 2
        frame['gsr_mean_z'] = frame.gsr_tonic_mean_z * -3
        frame['gsr_scr_count'] = 0
        selected, removed = compact_columns(frame)
        self.assertIn('eeg_rms_uv', selected)
        self.assertIn('gsr_tonic_mean_z', selected)
        for name in ['eeg_std_uv', 'gsr_mean_z', 'gsr_scr_count', 'eeg_line_noise_ratio']:
            self.assertNotIn(name, selected)
        self.assertEqual({r['feature'] for r in removed}, {'eeg_std_uv', 'gsr_mean_z', 'gsr_scr_count'})
        # Modificar otros datos no cambia la seleccion ajustada en frame.
        external = frame.copy()
        external['eeg_std_uv'] = np.random.default_rng(2).normal(size=100)
        self.assertEqual(selected, compact_columns(frame)[0])
        self.assertIn('eeg_std_uv', compact_columns(external)[0])

    def test_no_teacher_modality_reused(self):
        frame = pd.DataFrame(np.random.default_rng(3).normal(size=(100, len(PRIORITY))), columns=PRIORITY)
        for columns in candidates('attention_primary', frame)[0].values():
            self.assertTrue(set(columns).isdisjoint(EYE + PUPIL))
        sets = candidates('arousal_primary_6s', frame)[0]
        for columns in sets.values():
            self.assertTrue(set(columns).isdisjoint(GSR))
        self.assertEqual(len(sets['Pupil_no_quality']), 5)
        self.assertNotIn('pupil_both_valid_fraction', sets['Eye_Pupil_no_quality'])

    def test_paired_summary_aligns_participants(self):
        rows = []
        for name, subset, values in [('dummy', 'full', [.3, .3, .3]),
                                      ('logistic', 'full', [.4, .5, .6]),
                                      ('logistic', 'small', [.41, .51, .61])]:
            for i, value in enumerate(values):
                rows.append(dict(task='a', kind='classification', model=name, subset=subset,
                                 participant=f'P{i}', score=value, n_features=2))
        result = summarize_subjects(pd.DataFrame(rows).sample(frac=1, random_state=7))
        small = result.loc[result.subset.eq('small')].iloc[0]
        self.assertAlmostEqual(small.delta_full, .01)
        self.assertAlmostEqual(small.low_full, .01)
        self.assertAlmostEqual(small.high_full, .01)
        self.assertEqual(small.positive_full, 3)


if __name__ == '__main__':
    unittest.main()
