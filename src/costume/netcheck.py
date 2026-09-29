"""Report which hosts in config/network.yaml are reachable from this environment.

Usage:
    uv run costume-netcheck                     # every group
    uv run costume-netcheck retailer-images     # one group

A host counts as reachable when an HTTPS request gets any HTTP response, since even a
404 or 405 means the network path is open. The egress proxy refusing the connection,
or a timeout, counts as blocked. Exit code 0 when every checked host is reachable, 1
otherwise.
"""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from collections.abc import Callable
from pathlib import Path

import yaml

DEFAULT_CONFIG = Path("config/network.yaml")


def load_groups(path: Path) -> dict[str, list[str]]:
    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {name: list(group.get("hosts", [])) for name, group in config.get("groups", {}).items()}


def probe(host: str, timeout: float = 10.0) -> str:
    """Return 'ok (<status>)' or 'blocked (<reason>)' for one host."""
    request = urllib.request.Request(f"https://{host}/", method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return f"ok ({response.status})"
    except urllib.error.HTTPError as exc:
        return f"ok ({exc.code})"
    except (urllib.error.URLError, OSError) as exc:
        reason = getattr(exc, "reason", exc)
        return f"blocked ({reason})"


def check(groups: dict[str, list[str]], probe_fn: Callable[[str], str] = probe) -> list[tuple]:
    return [(group, host, probe_fn(host)) for group, hosts in groups.items() for host in hosts]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("groups", nargs="*", help="group names to check (default: all)")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args(argv)

    groups = load_groups(args.config)
    unknown = [name for name in args.groups if name not in groups]
    if unknown:
        print(f"error: unknown group(s): {', '.join(unknown)}", file=sys.stderr)
        return 2
    if args.groups:
        groups = {name: groups[name] for name in args.groups}

    results = check(groups)
    for group, host, status in results:
        print(f"{group:20} {host:32} {status}")
    return 0 if all(status.startswith("ok") for _, _, status in results) else 1


if __name__ == "__main__":
    sys.exit(main())
