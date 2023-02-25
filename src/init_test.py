import pytest
import proj

g_init_succ = False
checkinit = pytest.mark.skipif(not g_init_succ, reason='初始化失败')

def test_init(env):
    '''
    初始化
    '''
    global g_init_succ
    print("in test_init")
    if proj.init(env):
        g_init_succ = True
    else:
        assert False
    print("init_succ", g_init_succ)

def test_succ():
    '''
    测试通过
    '''
    print("succ")
    pass

def test_failed(env):
    '''
    测试失败
    '''
    print("failed")
    assert False
    pass

@checkinit
def test_need_init():
    '''
    测试依赖初始化
    '''
    print("g_init_succ:", g_init_succ)
    print("succ")
    pass
