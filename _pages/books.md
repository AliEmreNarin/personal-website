---
layout: page
title: library
permalink: /books/
nav: true
nav_order: 4
---

<style>
  /* past / present switch */
  .library-switch {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2.5rem;
    font-size: 1.05rem;
  }
  .switch-btn {
    background: none;
    border: none;
    padding: 0 0 0.25rem;
    cursor: pointer;
    color: var(--global-text-color-light, #6c757d);
    font-size: inherit;
    font-weight: 500;
    letter-spacing: 0.02em;
    border-bottom: 2px solid transparent;
    transition: color 0.15s, border-color 0.15s;
  }
  .switch-btn:hover { color: var(--global-text-color, #212529); }
  .switch-btn.active {
    color: var(--global-text-color, #212529);
    font-weight: 700;
    border-bottom-color: var(--global-theme-color, #212529);
  }

  .library-pane { display: none; }
  .library-pane.active { display: block; }

  .library-year {
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: var(--global-text-color-light, #6c757d);
    text-transform: uppercase;
    margin: 2.5rem 0 1.25rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--global-divider-color, #dee2e6);
  }
  .library-pane .library-year:first-child { margin-top: 0; }
  .library-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 1.5rem 1.25rem;
    margin-bottom: 1rem;
  }
  .now-empty {
    color: var(--global-text-color-light, #6c757d);
    font-size: 0.9rem;
    font-style: italic;
    padding: 1rem 0 2rem;
  }
  .book-card { display: flex; flex-direction: column; }
  .book-cover-wrap {
    position: relative;
    width: 100%;
    padding-top: 150%;
    overflow: hidden;
    border-radius: 4px;
    background: var(--global-divider-color, #dee2e6);
    box-shadow: 2px 3px 10px rgba(0,0,0,0.12);
  }
  .book-cover-wrap img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .book-status-badge {
    position: absolute;
    bottom: 0.4rem;
    left: 0.4rem;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.18rem 0.45rem;
    border-radius: 3px;
    color: #fff;
  }
  .badge-abandoned { background: rgba(160,30,30,0.8); }
  .book-info { margin-top: 0.6rem; flex: 1; }
  .book-title {
    font-size: 0.82rem;
    font-weight: 600;
    line-height: 1.35;
    color: var(--global-text-color, #212529);
    margin-bottom: 0.15rem;
  }
  .book-author {
    font-size: 0.75rem;
    color: var(--global-text-color-light, #6c757d);
    margin-bottom: 0.25rem;
  }
  .book-stars { font-size: 0.7rem; color: #e8a020; letter-spacing: 0.05em; }
  .book-stars .empty { color: var(--global-divider-color, #dee2e6); }
</style>

<div class="library-switch">
  <button class="switch-btn active" data-pane="present">present</button>
  <button class="switch-btn" data-pane="past">past</button>
</div>

{% assign reading_books = site.books | where: "status", "Reading" %}
{% assign queued_books = site.books | where: "status", "Queued" %}
{% assign past_books = site.books | where_exp: "b", "b.status != 'Reading' and b.status != 'Queued'" | sort: "started" | reverse %}

<div class="library-pane active" id="pane-present">
  <h2 class="library-year">Reading</h2>
  {% if reading_books.size > 0 %}
  <div class="library-grid">
    {% for book in reading_books %}
    <div class="book-card">
      <div class="book-cover-wrap">
        {% if book.cover %}<img src="{{ book.cover | relative_url }}" alt="{{ book.title }}" loading="lazy">
        {% elsif book.olid %}<img src="https://covers.openlibrary.org/b/olid/{{ book.olid }}-M.jpg" alt="{{ book.title }}" loading="lazy">
        {% elsif book.isbn %}<img src="https://covers.openlibrary.org/b/isbn/{{ book.isbn }}-M.jpg" alt="{{ book.title }}" loading="lazy">
        {% elsif book.cover_goodreads %}<img src="{{ book.cover_goodreads }}" alt="{{ book.title }}" loading="lazy">
        {% endif %}
      </div>
      <div class="book-info">
        <div class="book-title">{{ book.title }}</div>
        <div class="book-author">{{ book.author }}</div>
      </div>
    </div>
    {% endfor %}
  </div>
  {% else %}
  <p class="now-empty">Nothing in progress right now.</p>
  {% endif %}

  <h2 class="library-year">Want to Read</h2>
  {% if queued_books.size > 0 %}
  <div class="library-grid">
    {% for book in queued_books %}
    <div class="book-card">
      <div class="book-cover-wrap">
        {% if book.cover %}<img src="{{ book.cover | relative_url }}" alt="{{ book.title }}" loading="lazy">
        {% elsif book.olid %}<img src="https://covers.openlibrary.org/b/olid/{{ book.olid }}-M.jpg" alt="{{ book.title }}" loading="lazy">
        {% elsif book.isbn %}<img src="https://covers.openlibrary.org/b/isbn/{{ book.isbn }}-M.jpg" alt="{{ book.title }}" loading="lazy">
        {% elsif book.cover_goodreads %}<img src="{{ book.cover_goodreads }}" alt="{{ book.title }}" loading="lazy">
        {% endif %}
      </div>
      <div class="book-info">
        <div class="book-title">{{ book.title }}</div>
        <div class="book-author">{{ book.author }}</div>
      </div>
    </div>
    {% endfor %}
  </div>
  {% else %}
  <p class="now-empty">Nothing queued yet.</p>
  {% endif %}
</div>

<div class="library-pane" id="pane-past">
  {% assign by_year = past_books | group_by: "year" | sort: "name" | reverse %}
  {% for group in by_year %}
  <h2 class="library-year">{{ group.name }}</h2>
  <div class="library-grid">
    {% for book in group.items %}
    <div class="book-card">
      <div class="book-cover-wrap">
        {% if book.cover %}<img src="{{ book.cover | relative_url }}" alt="{{ book.title }}" loading="lazy">
        {% elsif book.olid %}<img src="https://covers.openlibrary.org/b/olid/{{ book.olid }}-M.jpg" alt="{{ book.title }}" loading="lazy">
        {% elsif book.isbn %}<img src="https://covers.openlibrary.org/b/isbn/{{ book.isbn }}-M.jpg" alt="{{ book.title }}" loading="lazy">
        {% elsif book.cover_goodreads %}<img src="{{ book.cover_goodreads }}" alt="{{ book.title }}" loading="lazy">
        {% endif %}
        {% if book.status == "Abandoned" %}<span class="book-status-badge badge-abandoned">Abandoned</span>{% endif %}
      </div>
      <div class="book-info">
        <div class="book-title">{{ book.title }}</div>
        <div class="book-author">{{ book.author }}</div>
        {% if book.stars %}
          {% assign s = book.stars %}
          <div class="book-stars">
            {% if s >= 1 %}★{% else %}<span class="empty">★</span>{% endif %}{% if s >= 2 %}★{% else %}<span class="empty">★</span>{% endif %}{% if s >= 3 %}★{% else %}<span class="empty">★</span>{% endif %}{% if s >= 4 %}★{% else %}<span class="empty">★</span>{% endif %}{% if s >= 5 %}★{% else %}<span class="empty">★</span>{% endif %}
          </div>
        {% endif %}
      </div>
    </div>
    {% endfor %}
  </div>
  {% endfor %}
</div>

<script>
  (function () {
    var btns = document.querySelectorAll('.switch-btn');
    var panes = document.querySelectorAll('.library-pane');
    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        btns.forEach(function (b) { b.classList.remove('active'); });
        panes.forEach(function (p) { p.classList.remove('active'); });
        btn.classList.add('active');
        document.getElementById('pane-' + btn.dataset.pane).classList.add('active');
      });
    });
  })();
</script>
