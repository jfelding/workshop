import subprocess

from workshop.tools.check_pictures import problems


def project(tmp_path, readme, parts=("bracket",), pictures=("bracket",)):
    (tmp_path / "exports").mkdir()
    for p in parts:
        (tmp_path / "exports" / f"{p}.stl").write_text("solid x\nendsolid x\n")
    for p in pictures:
        (tmp_path / "exports" / f"{p}.png").write_bytes(b"png")
    (tmp_path / "README.md").write_text(readme)
    return tmp_path


def test_every_part_shown(tmp_path):
    assert problems(project(tmp_path, "# B\n\n![Bracket](exports/bracket.png)\n")) == []


def test_missing_picture_and_unshown_part(tmp_path):
    out = problems(project(tmp_path, "# B\n\n![Bracket](exports/bracket.png)\n",
                           parts=("bracket", "lid"), pictures=("bracket",)))
    assert any("exports/lid.png missing" in o for o in out)
    assert any("does not show exports/lid.png" in o for o in out)


def test_readme_without_any_picture(tmp_path):
    out = problems(project(tmp_path, "# B\n", parts=(), pictures=()))
    assert any("shows no picture" in o for o in out)


def test_img_tag_counts_and_committed(tmp_path):
    p = project(tmp_path, '# B\n\n<img src="exports/bracket.png" width="200">\n')
    assert problems(p) == []
    subprocess.run(["git", "init", "-q"], cwd=p, check=True)
    assert any("not committed" in o for o in problems(p, committed=True))
    subprocess.run(["git", "add", "exports/bracket.png"], cwd=p, check=True)
    assert problems(p, committed=True) == []
