import json
from pathlib import Path


def test_qa_dataset() -> None:
    data_path = Path(__file__).parent / "data" / "qa_pairs.json"
    pairs = json.loads(data_path.read_text())
    assert 30 <= len(pairs) <= 50
    for item in pairs:
        context = item["context"]
        answer = item["answer"]
        span = item["citation"]
        assert context[span["start"] : span["end"]] == answer
