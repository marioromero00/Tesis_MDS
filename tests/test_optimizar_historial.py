import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from optimizar_historial import histories, represent, smooth, FEATURES, select


class OptimizationTests(unittest.TestCase):
    def frame(self):
        f=pd.DataFrame(dict(participant=['P1']*5+['P2']*2,recording=['R']*7,
            segment_id=['a','a','b','b','b','a','a'],stimulus=['x','x','y','y','y','x','x'],
            window_start_utc=pd.to_datetime(['2026-01-01T00:00:00Z','2026-01-01T00:00:01Z',
                '2026-01-01T00:00:02Z','2026-01-01T00:00:03Z','2026-01-01T00:00:08Z',
                '2026-01-01T00:00:00Z','2026-01-01T00:00:01Z'])))
        for c in FEATURES: f[c]=np.arange(7,dtype=float)
        return f

    def test_context_crosses_segments_only_when_declared_and_resets_gap_person(self):
        f=self.frame()
        segment=dict(histories(f,4,'segment')); recording=dict(histories(f,4,'recording'))
        self.assertEqual(segment[2],[2]); self.assertEqual(recording[2],[0,1,2])
        self.assertEqual(recording[4],[4]); self.assertEqual(recording[5],[5])

    def test_representation_and_smoothing_cannot_see_future(self):
        f=self.frame(); changed=f.copy(); changed.loc[3:,FEATURES]=999
        np.testing.assert_array_equal(represent(f,'recording_4')[:3],represent(changed,'recording_4')[:3])
        p=np.arange(21,dtype=float).reshape(7,3); altered=p.copy(); altered[3:]=999
        np.testing.assert_array_equal(smooth(f,p,4)[:3],smooth(f,altered,4)[:3])
        np.testing.assert_array_equal(smooth(f,p,4)[2],p[:3].mean(axis=0))

    def test_current_selection_excludes_smoothed_current(self):
        s=pd.DataFrame(dict(representation=['current','current','segment_4'],estimator=['a']*3,
                            smoothing=[1,4,1],score=[.3,.5,.4]))
        self.assertEqual(select(s,'current').score,.3)
        self.assertEqual(select(s,'temporal').score,.5)

    def test_multimodal_inputs_exclude_teacher_and_future_values(self):
        from fusion_modalidades import inputs
        from baselines_estaticos import EYE,EEG,GSR
        f=self.frame()
        for c in EYE+EEG+GSR: f[c]=np.arange(len(f),dtype=float)
        changed=f.copy(); changed[GSR]=-999; changed['arousal_label_6s']='alto'
        np.testing.assert_array_equal(inputs(f,'full__recording_8'),inputs(changed,'full__recording_8'))
        changed.loc[3:,EYE+EEG+FEATURES]=999
        np.testing.assert_array_equal(inputs(f,'full__recording_8')[:3],inputs(changed,'full__recording_8')[:3])


if __name__=='__main__': unittest.main()
