from pathlib import Path

from costume.netcheck import check, load_groups, main

CONFIG = Path(__file__).resolve().parents[1] / "config" / "network.yaml"


def test_config_lists_approved_retailer_image_hosts():
    groups = load_groups(CONFIG)
    assert "i.ebayimg.com" in groups["retailer-images"]
    assert all(hosts for hosts in groups.values())


def test_check_pairs_every_host_with_its_probe_result():
    groups = {"a": ["one.test", "two.test"], "b": ["three.test"]}
    results = check(groups, probe_fn=lambda host: "ok (200)" if host != "two.test" else "blocked")
    assert results == [
        ("a", "one.test", "ok (200)"),
        ("a", "two.test", "blocked"),
        ("b", "three.test", "ok (200)"),
    ]


def test_unknown_group_is_a_usage_error(capsys):
    assert main(["no-such-group", "--config", str(CONFIG)]) == 2
