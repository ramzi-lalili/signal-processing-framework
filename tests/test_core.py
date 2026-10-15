import numpy as np
from generators.basic import SineGenerator
from operations.basic import Amplify, Differentiate
def test_sine():
    s=SineGenerator().generate(amplitude=2,frequency=10,duration=1,fs=1000)
    assert len(s.values)==1000
    assert np.max(s.values) <= 2.01
def test_amplify():
    s=SineGenerator().generate(amplitude=1,frequency=5,duration=1,fs=100)
    y=Amplify().apply(s,gain=3)
    assert np.isclose(np.max(y.values),3,atol=.1)
def test_derivative():
    s=SineGenerator().generate(amplitude=1,frequency=1,duration=1,fs=1000)
    y=Differentiate().apply(s)
    assert np.max(np.abs(y.values)) > 5
