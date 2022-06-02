import io

import doctest

import pytest

from . import failure_cases as module, finder_cases as finder_module
from .. import DTFinder, DTRunner, DebugDTRunner


### Smoke test DTRunner methods. Mainly to check that they are runnable.

def test_single_failure():
    finder = DTFinder()
    tests = finder.find(module.func9)
    runner = DTRunner(verbose=False)
    stream = io.StringIO()
    for test in tests:
        runner.run(test, out=stream.write)

    stream.seek(0)
    output = stream.read()
    assert output.startswith('\n func9\n -----\n')


def test_exception():
    finder = DTFinder()
    tests = finder.find(module.func10)
    runner = DTRunner(verbose=False)
    stream = io.StringIO()
    for test in tests:
        runner.run(test, out=stream.write)

    stream.seek(0)
    output = stream.read()
    assert output.startswith('\n func10\n ------\n')


def test_get_history():
    finder = DTFinder()
    tests = finder.find(finder_module)
    runner = DTRunner(verbose=False)
    for test in tests:
        runner.run(test)

    dct = runner.get_history()
    assert len(dct) == 6


def test_debug_runner():
    finder = DTFinder()
    tests = finder.find(module.func9)
    runner = DebugDTRunner(verbose=False)

    with pytest.raises(doctest.DocTestFailure) as failure:
        for t in tests:
            runner.run(t)
