"""
Backfill the product / warehouse / billing links on document_lines.

Why this exists
---------------
The original importer wrote each quotation line's description text but left
`variant_id` and `catalog_item_id` null on 606 of 719 lines. Everything
downstream depends on that link:

  * no variant  -> no inventory row  -> the split engine finds zero stock and
                   every order silently becomes a backorder
  * no category -> no discount ceiling -> the blended risk score falls back to a
                   flat rate for every line, so tier and category governance
                   never actually applies

How the match is made
---------------------
NOT by the CSV's `line_id -> product_variant_id` column. The database was
seeded from a different generation of the data than the current CSVs, so that
mapping is stale: it attaches a "Dell USB-C Dock" line to an HPE ProLiant
server. Only 19 of 392 such links survived a description check.

Instead each line is matched on its own description text against variant and
catalog item names, using Jaccard token overlap. A link is written only at
CONFIDENCE_THRESHOLD or above; anything weaker is left NULL on purpose. A null
link is a visible gap, a wrong link is a silent corruption.

    python scripts/backfill_line_links.py            # write links
    python scripts/backfill_line_links.py --dry-run  # report only

If the database sits on a mounted or synced folder and SQLite raises
"disk I/O error", copy it to a local disk, run this, and copy it back.
"""

import argparse
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.environ.get("DEALFLOW_DB") or os.path.join(ROOT, "dealflow360.db")

# Token overlap required before a link is trusted. 0.75 keeps the confident
# matches and discards the ambiguous middle band.
CONFIDENCE_THRESHOLD = 0.75


def normalise(s: str) -> str:
    """Lowercase, drop the '(Fulfillment: ...)' suffix, reduce to word tokens."""
    s = (s or "").lower()
    s = re.sub(r"\(fulfillment:[^)]*\)", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def overlap(a: str, b: str) -> float:
    A, B = set(a.split()), set(b.split())
    if not A or not B:
        return 0.0
    return len(A & B) / max(len(A), len(B))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report without writing")
    args = ap.parse_args()

    if not os.path.exists(DB):
        sys.exit(f"database not found: {DB}")

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    variants = [
        (r["id"], normalise(r["name"]), r["catalog_item_id"])
        for r in cur.execute("SELECT id, name, catalog_item_id FROM variants")
    ]
    items = [
        (r["id"], normalise(r["name"]))
        for r in cur.execute("SELECT id, name FROM catalog_items")
    ]
    exact_variant = {v[1]: v for v in variants}
    exact_item = {i[1]: i for i in items}

    stats = {"exact": 0, "fuzzy": 0, "unmatched": 0}
    updates = []

    for row in cur.execute("SELECT id, description FROM document_lines"):
        d = normalise(row["description"])
        if not d:
            stats["unmatched"] += 1
            continue

        variant_id = item_id = None

        if d in exact_variant:
            variant_id, _, item_id = exact_variant[d]
            stats["exact"] += 1
        elif d in exact_item:
            item_id = exact_item[d][0]
            stats["exact"] += 1
        else:
            best_v = max(((overlap(d, v[1]), v) for v in variants), default=(0.0, None))
            best_i = max(((overlap(d, i[1]), i) for i in items), default=(0.0, None))
            if best_v[0] >= best_i[0] and best_v[0] >= CONFIDENCE_THRESHOLD:
                variant_id, _, item_id = best_v[1]
                stats["fuzzy"] += 1
            elif best_i[0] >= CONFIDENCE_THRESHOLD:
                item_id = best_i[1][0]
                stats["fuzzy"] += 1
            else:
                stats["unmatched"] += 1
                continue

        updates.append((variant_id, item_id, row["id"]))

    if args.dry_run:
        print(f"  exact name matches   : {stats['exact']}")
        print(f"  fuzzy >= {CONFIDENCE_THRESHOLD}      : {stats['fuzzy']}")
        print(f"  left unlinked        : {stats['unmatched']}")
        print("  (dry run, nothing written)")
        conn.close()
        return

    cur.executemany(
        """
        UPDATE document_lines
           SET variant_id      = COALESCE(?, variant_id),
               catalog_item_id = COALESCE(?, catalog_item_id)
         WHERE id = ?
        """,
        updates,
    )

    # A variant line inherits its category through its parent catalog item.
    cur.execute(
        """
        UPDATE document_lines
           SET catalog_item_id = (
               SELECT v.catalog_item_id FROM variants v WHERE v.id = document_lines.variant_id
           )
         WHERE catalog_item_id IS NULL
           AND variant_id IS NOT NULL
        """
    )

    # A recurring line is one whose catalog item is flagged is_recurring.
    cur.execute(
        """
        UPDATE document_lines
           SET billing_type = CASE
                 WHEN (SELECT ci.is_recurring FROM catalog_items ci
                        WHERE ci.id = document_lines.catalog_item_id) = 1
                 THEN 'RECURRING' ELSE 'ONE_TIME' END
         WHERE catalog_item_id IS NOT NULL
        """
    )

    conn.commit()

    total = cur.execute("SELECT COUNT(*) FROM document_lines").fetchone()[0]
    linked = cur.execute(
        "SELECT COUNT(*) FROM document_lines WHERE variant_id IS NOT NULL OR catalog_item_id IS NOT NULL"
    ).fetchone()[0]
    categorised = cur.execute(
        """
        SELECT COUNT(*) FROM document_lines dl
          JOIN catalog_items ci ON ci.id = dl.catalog_item_id
         WHERE ci.category_id IS NOT NULL
        """
    ).fetchone()[0]
    recurring = cur.execute(
        "SELECT COUNT(*) FROM document_lines WHERE billing_type = 'RECURRING'"
    ).fetchone()[0]
    conn.close()

    print(f"  exact name matches   : {stats['exact']}")
    print(f"  fuzzy >= {CONFIDENCE_THRESHOLD}      : {stats['fuzzy']}")
    print(f"  left unlinked        : {stats['unmatched']}")
    print(f"  lines linked         : {linked} / {total}")
    print(f"  resolving to category: {categorised}")
    print(f"  recurring lines      : {recurring}")


if __name__ == "__main__":
    main()
