import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from persistencia_core import grid,decode,transitions
from test_hiperparametros import frame


class PersistenceTests(unittest.TestCase):
    def test_no_future_or_label_dependency_and_reset(self):
        f=frame(); n=len(f); p=np.random.default_rng(1).dirichlet([1,1,1],size=n)
        transition=transitions(f)
        self.assertTrue((transition>0).all()); np.testing.assert_allclose(transition.sum(axis=1),1)
        changed=p.copy(); changed[n//2:]=[.99,.005,.005]
        for choice in grid():
            actual=decode(f,p,transition,choice)
            np.testing.assert_allclose(actual.sum(axis=1),1)
            np.testing.assert_array_equal(actual[:n//2],decode(f,changed,transition,choice)[:n//2])
            np.testing.assert_array_equal(actual,decode(f.drop(columns=['arousal_label_6s']),p,transition,choice))
            # Separate participant prediction must not inherit previous participant state.
            last=f.participant.eq(f.participant.iloc[-1]).to_numpy()
            np.testing.assert_array_equal(actual[last],decode(f.loc[last].reset_index(drop=True),p[last],transition,choice))


if __name__=='__main__': unittest.main()
