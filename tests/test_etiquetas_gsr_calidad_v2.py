import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import numpy as np,pandas as pd
from reconstruir_etiquetas_gsr_calidad_v2 import rebuild,COLS
class QualityLabels(unittest.TestCase):
 def data(self):
  n=20;f=pd.DataFrame(dict(participant=['P']*n,recording=['r']*n,segment_id=[1]*n,stimulus=['s']*n,window_start_utc=pd.date_range('2026-01-01',periods=n,freq='s',tz='UTC'),gsr_n=[30]*n,gsr_coverage=[1.]*n,gsr_window_valid=[True]*n))
  for c in COLS:f[c]=np.arange(n,dtype=float)
  return f
 def test_missing_invalidates_and_resets(self):
  f=self.data();f.loc[7,COLS[0]]=np.nan;r,_,_=rebuild(f)
  self.assertFalse(r.loc[7,'gsr_quality_valid']);self.assertTrue(r.loc[7:11,'activation_binary_v2'].isna().all());self.assertEqual(r.loc[12,'history_valid_windows'],5)
 def test_zero_coverage_zero_scr_not_labelled(self):
  f=self.data();f.loc[6,'gsr_coverage']=0;f.loc[6,'gsr_n']=0;f.loc[6,COLS[2:]]=0;r,_,_=rebuild(f)
  self.assertTrue(pd.isna(r.loc[6,'activation_binary_v2']))
 def test_segment_boundary_and_gap(self):
  f=self.data();f.loc[10:,'segment_id']=2;r,_,_=rebuild(f)
  self.assertTrue(r.loc[10:13,'score6s_quality'].isna().all())
  f=self.data();f.loc[10:,'window_start_utc']+=pd.Timedelta(seconds=4);r,_,_=rebuild(f);self.assertTrue(r.loc[10:13,'score6s_quality'].isna().all())
 def test_constant_has_no_labels(self):
  f=self.data();f[COLS]=0;r,_,_=rebuild(f);self.assertTrue(r.activation_binary_v2.isna().all())
 def test_participant_alignment_independent_of_input_order(self):
  first=self.data();first['participant']='P2'
  second=self.data();second['participant']='P10'
  second[COLS]=second[COLS].pow(2)+7
  f=pd.concat([first,second],ignore_index=True);f['source_row']=np.arange(len(f))
  original,_,_=rebuild(f);shuffled,_,_=rebuild(f.sample(frac=1,random_state=42))
  columns=['participant','score2s_quality','score6s_quality','activation_binary_v2']
  pd.testing.assert_frame_equal(original.set_index('source_row')[columns].sort_index(),shuffled.set_index('source_row')[columns].sort_index())
if __name__=='__main__':unittest.main()
