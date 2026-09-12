import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from adaptacion_core import grid,adapt
from test_hiperparametros import frame


class AdaptationTests(unittest.TestCase):
    def test_label_independence_and_person_isolation(self):
        f=frame(); p=np.random.default_rng(4).dirichlet([1,1,1],len(f)); mask=f.participant.eq('P1').to_numpy()
        for choice in grid():
            result=adapt(f,p,choice)
            np.testing.assert_allclose(result.sum(axis=1),1)
            np.testing.assert_array_equal(result,adapt(f.drop(columns=['arousal_label_6s']),p,choice))
            np.testing.assert_array_equal(result[mask],adapt(f.loc[mask].reset_index(drop=True),p[mask],choice))

    def test_offline_future_dependency_is_explicit_and_ties_preserved(self):
        f=frame().iloc[:30]; p=np.tile([.3,.4,.3],(len(f),1))
        d=next(d for d in grid() if d['family']=='rank' and d['window']==1 and d['low']==1/3)
        np.testing.assert_array_equal(adapt(f,p,d).argmax(axis=1),np.ones(len(f),int))
        changed=p.copy(); changed[15:]=[.01,.01,.98]
        self.assertFalse(np.array_equal(adapt(f,p,d)[:15],adapt(f,changed,d)[:15]))


if __name__=='__main__': unittest.main()
