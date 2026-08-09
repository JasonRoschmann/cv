#!/usr/bin/env python3
"""Baut proof.json fuer das CV-'Proof of Work'-Panel.

- Heatmap: GitHub GraphQL contributionCalendar (letzte 12 Wochen), wenn GITHUB_TOKEN
  gesetzt ist (in der Action). Ohne Token: Fallback aus public PushEvents.
- Ships: kuratierter Feed aus public Events, nur echte Arbeit (Allowlist), keine
  Kurs-Repos, keine Follower-Zahl.

stdlib only -> laeuft in GitHub Actions ohne pip install.
"""
import json, os, sys, urllib.request, urllib.error, datetime

USER = os.environ.get("GH_USER", "JasonRoschmann")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
WEEKS = 12

# Kuratierung: nur echte Arbeit zeigen. Org 'flowki-club' immer, plus diese Repos.
ALLOW_ORGS = {"flowki-club"}
ALLOW_REPOS = {f"{USER}/cv", f"{USER}/atopicv-preview"}


def _get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "cv-proof"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _graphql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {TOKEN}", "User-Agent": "cv-proof",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def heatmap_from_graphql():
    q = ("query($login:String!){user(login:$login){contributionsCollection{"
         "contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}")
    d = _graphql(q, {"login": USER})
    cal = d["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[day["contributionCount"] for day in w["contributionDays"]]
             for w in cal["weeks"]][-WEEKS:]
    return weeks, cal["totalContributions"]


def heatmap_from_events(events):
    """Fallback ohne Token: Commits pro Tag aus PushEvents der letzten 12 Wochen."""
    today = datetime.date.today()
    start = today - datetime.timedelta(days=WEEKS * 7 - 1)
    counts = {}
    for ev in events:
        if ev.get("type") != "PushEvent":
            continue
        try:
            d = datetime.datetime.strptime(ev["created_at"][:10], "%Y-%m-%d").date()
        except Exception:
            continue
        if d < start:
            continue
        counts[d] = counts.get(d, 0) + int((ev.get("payload") or {}).get("size", 1) or 1)
    # Kalender an einem Sonntag ausrichten (GitHub-Konvention: Woche startet So)
    start -= datetime.timedelta(days=(start.weekday() + 1) % 7)
    weeks, total = [], 0
    for w in range(WEEKS):
        row = []
        for dow in range(7):
            day = start + datetime.timedelta(days=w * 7 + dow)
            c = counts.get(day, 0)
            row.append(c)
            total += c
        weeks.append(row)
    return weeks, total


def build_ships(events):
    """Kuratierter, aggregierter Feed: pro (Repo, Tag) eine Zeile, nur echte Arbeit."""
    def allowed(repo_full):
        owner = repo_full.split("/")[0]
        return owner in ALLOW_ORGS or repo_full in ALLOW_REPOS

    agg = {}
    order = []
    for ev in events:
        repo = (ev.get("repo") or {}).get("name", "")
        if not repo or not allowed(repo):
            continue
        t = ev.get("type")
        day = ev.get("created_at", "")[:10]
        if t == "PushEvent":
            kind, n = "push", int((ev.get("payload") or {}).get("size", 1) or 1)
        elif t == "CreateEvent":
            kind, n = "create", 1
        elif t == "PullRequestEvent":
            kind, n = "pr", 1
        else:
            continue
        key = (repo, day, kind)
        if key not in agg:
            agg[key] = {"repo": repo, "when": day, "kind": kind, "n": 0}
            order.append(key)
        agg[key]["n"] += n
    ships = [agg[k] for k in order][:7]
    # Anzeigename: Org -> nur Org-Name, sonst repo-Name ohne Owner
    for s in ships:
        owner, _, name = s["repo"].partition("/")
        s["label"] = owner if owner in ALLOW_ORGS else name
    return ships


def main():
    events = []
    try:
        events = _get(f"https://api.github.com/users/{USER}/events/public?per_page=100")
        if not isinstance(events, list):
            events = []
    except urllib.error.URLError as e:
        print("events fetch failed:", e, file=sys.stderr)

    source = "events"
    if TOKEN:
        try:
            weeks, total = heatmap_from_graphql()
            source = "graphql"
        except Exception as e:
            print("graphql failed, fallback events:", e, file=sys.stderr)
            weeks, total = heatmap_from_events(events)
    else:
        weeks, total = heatmap_from_events(events)

    out = {
        "updated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "user": USER,
        "weeks": weeks,
        "total": total,
        "ships": build_ships(events),
        "source": source,
    }
    dst = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "proof.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("wrote", dst, "source=%s total=%s ships=%d" % (source, total, len(out["ships"])))


if __name__ == "__main__":
    main()
