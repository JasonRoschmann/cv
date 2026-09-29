"""Selbsttest des Proof-Feeds mit Events im Format der GitHub-Events-API: py -3 scripts/test_build_proof.py"""
from build_proof import build_ships


def ev(typ: str, tag: str = "2026-09-29T10:00:00Z", **payload) -> dict:
    return {"type": typ, "repo": {"name": "JasonRoschmann/cv"}, "created_at": tag, "payload": payload}


def test_branch_anlage_ist_kein_init():
    assert build_ships([ev("CreateEvent", ref_type="branch")]) == []


def test_repo_anlage_ist_init():
    assert [s["kind"] for s in build_ships([ev("CreateEvent", ref_type="repository")])] == ["init"]


def test_pr_zaehlt_nur_einmal_beim_merge():
    ships = build_ships([ev("PullRequestEvent", action="merged"), ev("PullRequestEvent", action="opened")])
    assert [(s["kind"], s["n"]) for s in ships] == [("merge", 1)]


def test_geschlossen_und_gemergt_zaehlt_als_merge():
    ships = build_ships([ev("PullRequestEvent", action="closed", pull_request={"merged": True}),
                         ev("PullRequestEvent", action="closed", pull_request={"merged": False})])
    assert [(s["kind"], s["n"]) for s in ships] == [("merge", 1)]


def test_push_ohne_size_zaehlt_einmal():
    assert [(s["kind"], s["n"]) for s in build_ships([ev("PushEvent")])] == [("push", 1)]


if __name__ == "__main__":
    rot = 0
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            try:
                f(); print("OK  ", name)
            except AssertionError:
                rot += 1; print("FAIL", name)
    raise SystemExit(1 if rot else 0)
