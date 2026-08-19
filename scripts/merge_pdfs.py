#!/usr/bin/env python3
import argparse
from pypdf import PdfReader,PdfWriter
def main():
    p=argparse.ArgumentParser();p.add_argument("inputs",nargs="+");p.add_argument("--output",required=True);a=p.parse_args();w=PdfWriter()
    for f in a.inputs:
        for page in PdfReader(f).pages:w.add_page(page)
    with open(a.output,"wb") as out:w.write(out)
if __name__=="__main__":main()
