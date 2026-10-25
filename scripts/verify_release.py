#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def parse_sum_file(path: Path):
    out={}
    for line in path.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#'): continue
        digest, name=line.split(None,1)
        out[name.strip()] = digest
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--archive-dir', type=Path, help='Optional directory containing the large archival artifacts.')
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'RELEASE_MANIFEST.json').read_text(encoding='utf-8'))
    failures=[]
    for rel, meta in manifest['files'].items():
        p=root/rel
        if not p.exists():
            failures.append(f'MISSING::{rel}'); continue
        actual=sha256(p)
        if actual != meta['sha256']:
            failures.append(f'SHA_MISMATCH::{rel}::{actual}')
    if args.archive_dir:
        expected=parse_sum_file(root/'evidence'/'SHA256_ARCHIVAL_ARTIFACTS.txt')
        for name,digest in expected.items():
            p=args.archive_dir/name
            if p.exists():
                actual=sha256(p)
                if actual != digest:
                    failures.append(f'ARCHIVE_SHA_MISMATCH::{name}::{actual}')
            else:
                print(f'ARCHIVE_OPTIONAL_MISSING::{name}')
    if failures:
        for x in failures: print(x)
        raise SystemExit(1)
    print('REPOSITORY_RELEASE_INTEGRITY=PASS')
    print(f'VERSION={manifest["version"]}')
    print(f'FILES_VERIFIED={len(manifest["files"])}')

if __name__=='__main__':
    main()
