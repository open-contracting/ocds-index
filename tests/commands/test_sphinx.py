import json
import os.path
import time
import traceback

import pytest
from click.testing import CliRunner

from ocdsindex.cli.__main__ import main
from tests import expected


def test_sphinx():
    runner = CliRunner()

    base_url = "https://standard.open-contracting.org/dev/"
    result = runner.invoke(main, ["sphinx", os.path.join("tests", "fixtures"), base_url])

    actual = json.loads(result.output)

    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
    assert len(actual) == 3
    assert actual["base_url"] == base_url
    assert actual["created_at"] == pytest.approx(time.time())
    assert set(actual["documents"]) == set(expected)
