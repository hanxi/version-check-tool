import pytest
from py.xml import html
from py.xml import raw
from ansi2html import Ansi2HTMLConverter
from html import escape

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
    cells.pop(1)  # 删除检查列
    cells.pop(-1) # 删除link列
    cells.insert(1, html.th("描述"))

def pytest_html_results_table_row(report, cells):
    cells.pop(1)  # 删除检查列
    cells.pop(-1) # 删除link列
    description = "未知"
    if hasattr(report, "description"):
        description = report.description
    cells.insert(1, html.td(description))

def pytest_html_results_table_html(report, data):
    del data[:]
    log = html.div(class_="log")
    print(report)
    if report.passed:
        log = html.div(class_="log-passed")
    elif report.skipped:
        log = html.div(class_="log-skipped")
    elif report.failed:
        log = html.div(class_="log-failed")
    if report.skipped and report.longrepr:
        arr = report.longreprtext.strip("()").split(",")
        skip_msg = arr[len(arr)-1]
        log.append(html.span(raw(escape(skip_msg))))
    elif report.failed and report.longrepr:
        pass
    elif report.longrepr:
        text = report.longreprtext or report.full_text
        for line in text.splitlines():
            separator = line.startswith("_ " * 10)
            if separator:
                log.append(line[:80])
            else:
                exception = line.startswith("E   ")
                if exception:
                    log.append(html.span(raw(escape(line)), class_="error"))
                else:
                    log.append(raw(escape(line)))
            log.append(html.br())

    for section in report.sections:
        _, content = map(escape, section)

        converter = Ansi2HTMLConverter(
            inline=False, escaped=False,
        )
        content = converter.convert(content, full=False)

        log.append(raw(content))
        log.append(html.br())
    data.append(log)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
