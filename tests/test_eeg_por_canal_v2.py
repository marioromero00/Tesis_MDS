import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np
from eeg_por_canal_v2 import extract_window,FEATURES,FS,BANDS
class EEGChannelTests(unittest.TestCase):
    def signal(self):
        t=np.arange(250)/FS;x=np.tile(np.sin(2*np.pi*10*t)[:,None],(1,16))*20
        x[:,1]=20*np.sin(2*np.pi*6*t);return x
    def test_channel_band_information_is_preserved(self):
        d=extract_window(self.signal())
        self.assertGreater(d['eegch00_relative_alpha'],.8)
        self.assertGreater(d['eegch01_relative_theta'],.8)
        self.assertEqual(d['eegsp_usable_channels'],16)
    def test_relative_powers_sum_to_one(self):
        d=extract_window(self.signal())
        self.assertAlmostEqual(sum(d['eegch00_relative_'+b] for b in BANDS),1.,places=10)
        self.assertGreaterEqual(d['eegch00_spectral_entropy'],0);self.assertLessEqual(d['eegch00_spectral_entropy'],1)
    def test_rail_channel_becomes_missing_without_dropping_window(self):
        x=self.signal();x[:,0]=187500;d=extract_window(x)
        self.assertEqual(d['eegch00_usable'],0);self.assertTrue(np.isnan(d['eegch00_relative_alpha']))
        self.assertEqual(d['eegsp_usable_channels'],15);self.assertEqual(d['eegsp_n_samples'],250)
    def test_large_sample_gap_marks_features_missing(self):
        d=extract_window(self.signal(),max_gap_s=.2)
        self.assertEqual(d['eegsp_usable_channels'],0);self.assertEqual(set(d),set(FEATURES))
if __name__=='__main__':unittest.main()
