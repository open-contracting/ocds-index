import json
import os
import time
import traceback

from click.testing import CliRunner

from ocdsindex.cli.__main__ import main

from tests import elasticsearch, search


def test_expire(tmpdir):
    host = os.getenv("ELASTICSEARCH_URL", "localhost:9200")

    runner = CliRunner()

    filename = tmpdir.join("data.json")
    with open(os.path.join("tests", "fixtures", "data.json")) as f:
        data = json.load(f)

    exclude_file = tmpdir.join("exclude.txt")
    exclude_file.write("https://standard.open-contracting.org/keep/\n")

    with elasticsearch(host) as es:

        def index(base_url, offset, total):
            data["base_url"] = base_url
            data["created_at"] = int(time.time() - offset)
            for documents in data["documents"].values():
                for document in documents:
                    document["url"] = f"{base_url}{document['url'][42:]}"

            filename.write(json.dumps(data))
            result = runner.invoke(main, ["index", str(filename), host])

            assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
            assert result.output == ""
            assert search(es, "ocdsindex_en")["total"]["value"] == total

        # Add new data.
        index("https://standard.open-contracting.org/new/", 0, 8)

        # Add old data.
        index("https://standard.open-contracting.org/old/", 20000000, 16)

        # Add old data to keep.
        index("https://standard.open-contracting.org/keep/", 20000000, 24)

        # With --exclude-file.
        result = runner.invoke(main, ["expire", host, "--exclude-file", str(exclude_file)])

        assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
        assert result.output == ""
        assert search(es, "ocdsindex_en")["total"]["value"] == 16

        # Without --exclude-file.
        result = runner.invoke(main, ["expire", host])

        assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
        assert result.output == ""
        assert search(es, "ocdsindex_en")["total"]["value"] == 8
