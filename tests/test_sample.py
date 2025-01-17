import pytest



def cal_add(a :int, b :int):
    return a+b

add_test_data = [
    pytest.param(5,10,15,id="5+10 is 15"),
    pytest.param(10,20,30,id="10+20 is 30"),
    pytest.param(1,2,4, marks=pytest.mark.xfail, id="1+2 is 4"),
    pytest.param(1,2,9, marks=pytest.mark.xfail, id="1+2 is 9")
]

@pytest.mark.parametrize("a, b, result", add_test_data)
def test_add(a,b,result):
    assert cal_add(a,b) == result

@pytest.mark.skip(reason="no way of currently testing this")
def test_skip_v1():
    assert 1 == 1

def test_skip_v2():
    if True :
        pytest.skip(reason="no way of currently testing this")
    assert 1 == 1

class TestCalculator:
    value = 0

    def test_add(self):
        self.value += 1
        assert self.value == 1
        
    def test_result(self):
        assert self.value == 0