#!/usr/bin/env python3
"""
Paper Trail — re-check one archive year for late additions.

enumerate.py caches each view|exam|year subject list in out/subjects.json and
skips any subject that already has rows, so material the SEC publishes AFTER a
crawl (the Junior Cycle marking schemes, which arrive in the autumn; a re-issued
or late scheme) is never seen again. This re-lists the given year for every
view and examination in scope, re-walks each subject, and appends only rows the
manifest does not already hold. Same politeness as enumerate.py.

usage: python3 refresh_year.py 2026
"""

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("pt_enumerate", os.path.join(HERE, "enumerate.py"))
en = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(en)


def main():
    year = sys.argv[1]
    have = set()
    for line in open(en.MANIFEST):
        r = json.loads(line)
        have.add((r["view"], r["exam"], r["year"], r["subjectId"], r["fileid"]))
    subjects_index = json.load(open(en.SUBJECTS))
    added = 0
    with open(en.MANIFEST, "a") as out:
        for view in en.VIEWS:
            for exam, years in en.SCOPE[view].items():
                if year not in years:
                    continue
                key = f"{view}|{exam}|{year}"
                subs = en.parse_subjects(en.post(en.fields(view, year, exam)))
                before = {sid for sid, _ in subjects_index.get(key, [])}
                subjects_index[key] = subs
                en.log(f"{key}: {len(subs)} subjects ({len(set(s for s, _ in subs) - before)} new)")
                for sid, sname in subs:
                    for fileid, label, size_hint in en.parse_files(en.post(en.fields(view, year, exam, sid))):
                        if (view, exam, year, sid, fileid) in have:
                            continue
                        out.write(json.dumps({"view": view, "exam": exam, "year": year, "subjectId": sid,
                                              "subjectName": sname, "fileid": fileid, "label": label,
                                              "sizeHint": size_hint}) + "\n")
                        out.flush()
                        added += 1
                        en.log(f"  + {sname}: {fileid} | {label}")
    with open(en.SUBJECTS, "w") as f:
        json.dump(subjects_index, f, indent=1)
    en.log(f"DONE — {added} new rows for {year}")


if __name__ == "__main__":
    sys.exit(main())
