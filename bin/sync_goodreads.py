#!/usr/bin/env python3
"""
Sync Goodreads shelves → _books/ Jekyll collection.

Usage:
  python3 bin/sync_goodreads.py            # dry run (print what would change)
  python3 bin/sync_goodreads.py --write    # create/update _books/ files

Books are identified by their Goodreads book_id so filenames are stable.
Existing files are never overwritten (manual edits are preserved).
"""

import argparse
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

GOODREADS_USER_ID = "165621971"
SHELVES = ["currently-reading", "to-read", "books-2023", "books-2024", "books-2025", "books-2026"]
BOOKS_DIR = os.path.join(os.path.dirname(__file__), "..", "_books")


def fetch_shelf(shelf):
    url = f"https://www.goodreads.com/review/list_rss/{GOODREADS_USER_ID}?shelf={shelf}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read()


def text(el, tag):
    node = el.find(tag)
    return node.text.strip() if node is not None and node.text else ""


def slugify(s):
    s = s.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "_", s)
    return s.strip("_")[:60]


def determine_status(user_shelves_str, read_at):
    shelves = [s.strip() for s in user_shelves_str.split(",")]
    if "currently-reading" in shelves:
        return "Reading"
    if "not-finishing" in shelves:
        return "Abandoned"
    if "to-read" in shelves:
        return "Queued"
    if read_at:
        return "Finished"
    return "Finished"


def parse_date(date_str):
    """Return YYYY-MM-DD or empty string."""
    if not date_str:
        return ""
    # Format: "Sun, 09 Aug 2026 13:07:07 -0700" or "Sun, 9 Aug 2026 00:00:00 +0000"
    try:
        from email.utils import parsedate
        t = parsedate(date_str)
        if t:
            return f"{t[0]:04d}-{t[1]:02d}-{t[2]:02d}"
    except Exception:
        pass
    return ""


def year_from_shelves(user_shelves_str, shelf_fetched_from):
    """Determine which year shelf this book belongs to."""
    for yr in ["2026", "2025", "2024", "2023"]:
        if f"books-{yr}" in user_shelves_str:
            return yr
    # Fall back to the shelf we fetched it from
    for yr in ["2026", "2025", "2024"]:
        if yr in shelf_fetched_from:
            return yr
    return ""


def book_to_markdown(book):
    title = book["title"]
    author = book["author"]
    isbn = book["isbn"]
    cover_url = book.get("cover_url", "")
    rating = book.get("rating", "")
    read_at = book.get("read_at_iso", "")
    date_added = book.get("date_added_iso", "")
    published = book.get("published", "")
    status = book.get("status", "Finished")
    review = book.get("review", "")
    goodreads_id = book.get("book_id", "")
    year = book.get("year", "")

    # Date used for Jekyll sorting (started = date added or read date)
    sort_date = read_at or date_added or (f"{year}-06-01" if year else "")

    lines = ["---"]
    lines.append("layout: book-review")
    lines.append(f"title: {repr(title)}")
    lines.append(f"author: {repr(author)}")
    if isbn:
        lines.append(f"isbn: {isbn}")
    if cover_url:
        lines.append(f"cover_goodreads: {cover_url}")
    if published:
        lines.append(f"released: {published}")
    if sort_date:
        lines.append(f"date: {sort_date}")
        lines.append(f"started: {sort_date}")
    if read_at:
        lines.append(f"finished: {read_at}")
    if rating and rating != "0":
        lines.append(f"stars: {rating}")
    lines.append(f"status: {status}")
    if goodreads_id:
        lines.append(f"goodreads_id: {goodreads_id}")
    lines.append("---")
    lines.append("")
    if review:
        lines.append(review)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write files (default: dry run)")
    args = parser.parse_args()

    os.makedirs(BOOKS_DIR, exist_ok=True)

    # Find existing GR book IDs to avoid overwriting
    existing_ids = set()
    for fname in os.listdir(BOOKS_DIR):
        if fname.startswith("gr_") and fname.endswith(".md"):
            parts = fname[3:].split("_", 1)
            if parts[0].isdigit():
                existing_ids.add(parts[0])

    seen_ids = set()
    new_books = []
    skipped = []

    for shelf in SHELVES:
        print(f"Fetching shelf: {shelf} ...", flush=True)
        try:
            xml_bytes = fetch_shelf(shelf)
            root = ET.fromstring(xml_bytes)
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)
            continue

        for item in root.findall(".//item"):
            book_id = text(item, "book_id")
            if not book_id or book_id in seen_ids:
                continue
            seen_ids.add(book_id)

            user_shelves_str = text(item, "user_shelves")
            read_at_raw = text(item, "user_read_at")
            date_added_raw = text(item, "user_date_added")

            book = {
                "book_id": book_id,
                "title": text(item, "title"),
                "author": text(item, "author_name"),
                "isbn": text(item, "isbn"),
                "cover_url": text(item, "book_large_image_url") or text(item, "book_medium_image_url"),
                "rating": text(item, "user_rating"),
                "read_at_iso": parse_date(read_at_raw),
                "date_added_iso": parse_date(date_added_raw),
                "review": text(item, "user_review"),
                "published": text(item, "book_published"),
                "status": determine_status(user_shelves_str, read_at_raw),
                "year": year_from_shelves(user_shelves_str, shelf),
            }

            slug = slugify(book["title"])
            filename = f"gr_{book_id}_{slug}.md"
            filepath = os.path.join(BOOKS_DIR, filename)

            if book_id in existing_ids:
                skipped.append(book["title"])
                continue

            new_books.append((filepath, filename, book))

    print(f"\nNew books to add:  {len(new_books)}")
    print(f"Already exist:     {len(skipped)}")
    print()

    for filepath, filename, book in new_books:
        yr = book.get("year", "?")
        print(f"  [{yr}] {book['title']} by {book['author']}  →  {filename}")
        if args.write:
            content = book_to_markdown(book)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

    if not args.write:
        print("\nDry run — pass --write to create files.")
    else:
        print(f"\nWrote {len(new_books)} book files to {BOOKS_DIR}/")


if __name__ == "__main__":
    main()
