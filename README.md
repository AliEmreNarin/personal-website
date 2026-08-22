# alinarin.site

Personal website of Ali Emre Narin. A small custom Jekyll site: dark-first, one accent color, no theme gems.

## Editing

| Want to…            | Do this                                                                                                           |
| ------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Change the bio      | Edit `index.md`                                                                                                   |
| Write a post        | Add `_posts/YYYY-MM-DD-slug.md` with `title`, `categories: technical` (or `non-technical`), `emoji:`, `featured:` |
| Add a blog section  | Add an entry to `_data/blog_categories.yml`                                                                       |
| Add a publication   | Add a BibTeX entry to `_bibliography/papers.bib` (extra fields: `pdf`, `arxiv`, `html`, `code`, `slides`)         |
| Update the CV       | Replace `assets/pdf/cv.pdf` and bump `updated:` in `_pages/cv.md`                                                 |
| Change social links | Edit `_data/socials.yml`                                                                                          |
| Change the photo    | Replace `assets/img/avatar.jpg` (square-ish, ≥ 256 px)                                                            |
| Change nav / title  | Edit `_config.yml`                                                                                                |

The library is synced from Goodreads every morning by `.github/workflows/sync-goodreads.yml` (`bin/sync_goodreads.py`); shelves `books-2023…2026`, `currently-reading`, `to-read`.

## Preview vs. production

- Push to **`dev`** → builds to the unlisted preview at `https://alinarin.site/preview/` (noindex).
- Merge/push to **`main`** → deploys to `https://alinarin.site/`.

## Local

```bash
bundle install
bundle exec jekyll serve --livereload      # http://127.0.0.1:4000
npm run format                             # prettier
```
