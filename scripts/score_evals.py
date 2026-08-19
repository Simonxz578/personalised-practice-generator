#!/usr/bin/env python3
import argparse,json
from pathlib import Path
def main():
    p=argparse.ArgumentParser();p.add_argument("results");a=p.parse_args();data=json.loads(Path(a.results).read_text());scores=[x.get("scores",{}) for x in data];keys=sorted({k for s in scores for k in s});print(json.dumps({k:sum(s.get(k,0) for s in scores)/len(scores) for k in keys},indent=2))
if __name__=="__main__":main()
