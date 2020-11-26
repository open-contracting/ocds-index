import json
import os.path

from click.testing import CliRunner

from ocdsindex.cli.__main__ import main
from tests import expected


def test_sphinx():
    runner = CliRunner()
    base_url = "https://standard.open-contracting.org/dev/"
    result = runner.invoke(main, ["sphinx", os.path.join("tests", "fixtures"), base_url])

    actual = json.loads(result.output)

    assert result.exit_code == 0
    assert len(actual) == 2
    assert actual["base_url"] == "https://standard.open-contracting.org/dev/"
    assert set(actual["documents"]) == set(expected)
