from log_sources.file_source import FileLogSource

def test_read_lines(tmp_path):
    # Create temporary file with known content
    log_path = tmp_path / "test.log"
    log_path.write_text("Line 1\nLine 2\nLine 3\n")

    source = FileLogSource(str(log_path))
    lines = list(source.read_lines())

    assert lines == ["Line 1", "Line 2", "Line 3"]

def test_empty_file(tmp_path):
    log_path = tmp_path / "empty.log"
    log_path.write_text("")

    source = FileLogSource(str(log_path))
    lines = list(source.read_lines())

    assert lines == []