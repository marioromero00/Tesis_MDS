import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from scripts.comparar_tipos_fusion import geometric_mean


class TestTiposFusion(unittest.TestCase):
    def test_media_geometrica_conserva_probabilidades_validas(self):
        expert_a = np.array([[0.8, 0.1, 0.1], [0.2, 0.3, 0.5]])
        expert_b = np.array([[0.2, 0.2, 0.6], [0.1, 0.4, 0.5]])
        fused = geometric_mean([expert_a, expert_b])
        np.testing.assert_allclose(fused.sum(axis=1), 1.0)
        expected = np.sqrt(expert_a * expert_b)
        expected /= expected.sum(axis=1, keepdims=True)
        np.testing.assert_allclose(fused, expected)


if __name__ == "__main__":
    unittest.main()
