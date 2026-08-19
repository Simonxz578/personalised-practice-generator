#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from jsonschema import Draft202012Validator

def validate(instance_path, schema_path):
    data=json.loads(Path(instance_path).read_text(encoding="utf-8")); schema=json.loads(Path(schema_path).read_text(encoding="utf-8"))
    errors=sorted(Draft202012Validator(schema).iter_errors(data),key=lambda e:list(e.path))
    if errors: raise ValueError("\n".join(f"{'.'.join(map(str,e.path)) or '<root>'}: {e.message}" for e in errors))
    return data
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("instance"); ap.add_argument("schema"); a=ap.parse_args(); validate(a.instance,a.schema); print("schema: passed")
if __name__=="__main__": main()
