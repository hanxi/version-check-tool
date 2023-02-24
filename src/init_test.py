import pytest
import proj

g_init_succ = False
checkinit = pytest.mark.skipif(not g_init_succ, reason='初始化失败')

def test_init(env):
    global g_init_succ
    print("in test_init")
    if proj.init(env):
        g_init_succ = True
    else:
        assert False, "初始化环境失败"
    print("init_succ", g_init_succ)


@checkinit
def test_need_init():
    print("g_init_succ:", g_init_succ)
    print("succ")
    pass
