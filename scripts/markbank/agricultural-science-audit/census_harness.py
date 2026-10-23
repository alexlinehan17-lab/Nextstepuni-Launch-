"""Run census_subject for one subject with a given paper_census.py, writing its JSON output.
Used to prove a shared-reader change leaves every other subject byte-identical (run before and after, then cmp).
usage: python3 scripts/markbank/agricultural-science-audit/census_harness.py <paper_census.py> <subject> <out.json>
PAPERS_ROOT (env) points at an examiner-reports folder holding <subject>/papers; default: this checkout."""
import importlib.util, json, os, sys
AUTH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'authoring')
MAIN = os.environ.get('PAPERS_ROOT', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(AUTH))), 'examiner-reports'))
sys.path.insert(0, AUTH)
import paper
paper.papers_dir = lambda subject: os.path.join(MAIN, subject, 'papers')
src, subject, out = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('paper_census_under_test', src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.PP.papers_dir = paper.papers_dir
res = mod.census_subject(subject)
json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1, sort_keys=True, default=str)
print(subject, sum(p.get('leafCount', 0) for p in res['papers']))
