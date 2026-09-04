#!/usr/bin/env python3
"""Redirect legado /collections/all → /collections/todos."""

import json
import subprocess
import sys

STORE = "byinbz-0k.myshopify.com"


def gql(query: str, variables: dict) -> dict:
    cmd = [
        "shopify", "store", "execute", "-s", STORE,
        "--allow-mutations", "-j", "-q", query,
    ]
    if variables:
        cmd.extend(["-v", json.dumps(variables)])
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    start = out.find("{")
    if start < 0:
        raise ValueError(out[:300])
    return json.loads(out[start:])


def create_redirect(path: str, target: str) -> bool:
    q = """
    mutation urlRedirectCreate($urlRedirect: UrlRedirectInput!) {
      urlRedirectCreate(urlRedirect: $urlRedirect) {
        urlRedirect { id path target }
        userErrors { field message }
      }
    }
    """
    r = gql(q, {"urlRedirect": {"path": path, "target": target}})
    errs = r.get("urlRedirectCreate", {}).get("userErrors", [])
    if errs:
        msg = errs[0].get("message", "")
        if "already" in msg.lower() or "taken" in msg.lower() or "em uso" in msg.lower():
            print(f"  OK redirect (já existe): {path} → {target}")
            return True
        print(f"  ERRO {path}: {msg}")
        return False
    redir = r["urlRedirectCreate"]["urlRedirect"]
    print(f"  OK redirect {redir['path']} → {redir['target']}")
    return True


def main() -> int:
    print("Redirect /collections/all → /collections/todos\n")
    ok = create_redirect("/collections/all", "/collections/todos")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
