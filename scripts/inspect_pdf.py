#!/usr/bin/env python3
import argparse
from pathlib import Path
from pypdf import PdfReader
def inspect(path):
    r=PdfReader(path); text="\n".join((p.extract_text() or "") for p in r.pages); return {"file":str(path),"pages":len(r.pages),"chars":len(text),"has_disclaimer":"Original examination-style practice material" in text}
def main():
    p=argparse.ArgumentParser();p.add_argument("files",nargs="+");a=p.parse_args()
    for f in a.files: print(inspect(f))
if __name__=="__main__":main()
