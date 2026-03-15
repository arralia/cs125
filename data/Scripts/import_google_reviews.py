"""Import reviews from data/COMPSCIGoogleDocsReviews.json into MongoDB.

Usage:
  python import_google_reviews.py [--file path] [--commit] [--upsert]

By default the script performs a dry-run and only writes when `--commit` is passed.
Use --upsert to avoid creating duplicates by matching on `courseName`+`instructor`.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from datetime import datetime
import sys

from backend.database import Database


def load_reviews(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Import Google Docs course reviews into MongoDB")
    parser.add_argument("--file", type=str, default="data/COMPSCIGoogleDocsReviews.json")
    parser.add_argument("--commit", action="store_true", help="Actually write to the DB (default: dry-run)")
    parser.add_argument("--upsert", action="store_true", help="Upsert documents by courseName+instructor to avoid duplicates")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: file not found: {path}")
        sys.exit(2)

    reviews = load_reviews(path)
    print(f"Loaded {len(reviews)} review objects from {path}")

    db = Database()
    coll = db.get_collection("reviews")

    # Attach metadata timestamp
    for r in reviews:
        r.setdefault("imported_at", datetime.utcnow())

    if not args.commit:
        print("Dry-run mode: no changes written. Use --commit to insert into the database.")
        return

    # Insert or upsert
    inserted = 0
    if args.upsert:
        for r in reviews:
            query = {"courseName": r.get("courseName"), "instructor": r.get("instructor")}
            update = {"$set": r}
            res = coll.update_one(query, update, upsert=True)
            if getattr(res, "upserted_id", None) is not None:
                inserted += 1
    else:
        try:
            res = coll.insert_many(reviews, ordered=False)
            inserted = len(res.inserted_ids)
        except Exception as e:
            print(f"Error during insert_many: {e}")

    print(f"Done. Inserted or upserted {inserted} documents into 'reviews' collection.")


if __name__ == "__main__":
    main()
