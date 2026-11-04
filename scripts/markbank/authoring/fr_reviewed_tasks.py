"""Replace one reviewed category while preserving the other French additions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILE = ROOT / 'data/examTopics/french-reviewed-tasks.json'


def write_tasks(category, additions):
    rows = json.loads(FILE.read_text()) if FILE.exists() else []
    category_of = lambda row: row.get('category', row['cardId'].split('-')[3])
    rows = [row for row in rows if category_of(row) != category] + additions
    order = {'writing': 0, 'reading': 1, 'cloze': 2, 'listening': 3}
    rows.sort(key=lambda row: order[category_of(row)])
    assert len({row['cardId'] for row in rows}) == len(rows)
    FILE.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
