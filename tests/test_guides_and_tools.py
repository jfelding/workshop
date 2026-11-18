import types

import pytest

from workshop.guides import style
from workshop.guides.book import Chapter, write_book
from workshop.tools import check_file_sizes


def test_book_writes_index_and_linked_chapters(tmp_path):
    def build(title):
        return types.SimpleNamespace(build=lambda nav="": style.page(title, "sub", style.step(1, "Do it.", ""), nav))
    write_book(tmp_path, "Guides", [Chapter("01-a", build("A"), "A", "Done"),
                                    Chapter("02-b", build("B"), "B", "Next")])
    index = (tmp_path / "00-start-here.html").read_text()
    assert "01-a.html" in index and "02-b.html" in index and "Next" in index
    assert "02-b.html" in (tmp_path / "01-a.html").read_text()


def test_file_size_ratchet():
    assert check_file_sizes.check({"a.py": 10}, {}) == []
    assert "over the 800-line limit" in check_file_sizes.check({"a.py": 900}, {})[0]
    assert "grew" in check_file_sizes.check({"a.py": 901}, {"a.py": 900})[0]
