import os.path
import json

from click.testing import CliRunner

from ocdsindex.cli.__main__ import main
from tests import expected


def test_sphinx():
    runner = CliRunner()
    base_url = "https://standard.open-contracting.org/dev/"
    result = runner.invoke(main, ["sphinx", os.path.join("tests", "fixtures"), base_url])

    assert result.exit_code == 0
    assert json.loads(result.output) == {
        "base_url": "https://standard.open-contracting.org/dev/",
        "documents": expected,
    }
