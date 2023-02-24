import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--branch", action="store", default="master", help="branch: 分支名"
    )

@pytest.fixture()
def env(request):
    return {
        'branch': request.config.getoption("--branch"),
        'svn_root': "http://test.com",
        'svn_user': "user",
        'svn_passwd': "passwd",
    }

def pytest_configure(config):
    config._metadata.clear()
    config._metadata['分支'] = config.getoption('--branch')

def pytest_html_report_title(report):
    report.title = "版本静态检查报告"

def pytest_html_results_table_header(cells):
    cells.pop(-1)  # 删除link列

def pytest_html_results_table_row(report, cells):
    cells.pop(-1)  # 删除link列
