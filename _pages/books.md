---
layout: page
title: library
permalink: /books/
nav: true
nav_order: 4
---

<style>
  .library-intro {
    margin-bottom: 2.5rem;
    max-width: 600px;
  }
  .library-intro p {
    color: var(--global-text-color-light, #6c757d);
    line-height: 1.7;
  }
  .library-filters {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 2.5rem;
  }
  .filter-btn {
    padding: 0.3rem 0.85rem;
    border: 1px solid var(--global-divider-color, #dee2e6);
    border-radius: 999px;
    background: transparent;
    color: var(--global-text-color, #212529);
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.15s;
  }
  .filter-btn:hover {
    border-color: var(--global-theme-color, #212529);
  }
  .filter-btn.active {
    background: var(--global-theme-color, #212529);
    border-color: var(--global-theme-color, #212529);
    color: #fff;
  }
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
  .library-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 1.5rem 1.25rem;
    margin-bottom: 1rem;
  }
  .book-card {
    display: flex;
    flex-direction: column;
    transition: opacity 0.2s;
  }
  .book-card.hidden {
    display: none;
  }
  .book-card a {
    text-decoration: none;
    color: inherit;
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  .book-cover-wrap {
    position: relative;
    width: 100%;
    padding-top: 150%;
    overflow: hidden;
    border-radius: 4px;
    background: var(--global-divider-color, #dee2e6);
    box-shadow: 2px 3px 10px rgba(0,0,0,0.12);
    transition: box-shadow 0.2s, transform 0.2s;
  }
  .book-card:hover .book-cover-wrap {
    box-shadow: 4px 6px 18px rgba(0,0,0,0.2);
    transform: translateY(-2px);
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
  .badge-finished   { background: rgba(30,120,60,0.85); }
  .badge-reading    { background: rgba(30,80,180,0.85); }
  .badge-queued     { background: rgba(100,100,100,0.75); }
  .badge-paused     { background: rgba(180,100,20,0.82); }
  .badge-abandoned  { background: rgba(160,30,30,0.8); }
  .book-info {
    margin-top: 0.6rem;
    flex: 1;
  }
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
  .book-stars {
    font-size: 0.7rem;
    color: #e8a020;
    letter-spacing: 0.05em;
  }
  .book-stars .empty { color: var(--global-divider-color, #dee2e6); }
</style>

<div class="library-intro">
  <p>Books I've read, am reading, or plan to read — roughly in reverse order. Click any cover to read my notes.</p>
</div>

<div class="library-filters">
  <button class="filter-btn active" data-filter="all">All</button>
  <button class="filter-btn" data-filter="finished">Finished</button>
  <button class="filter-btn" data-filter="reading">Reading</button>
  <button class="filter-btn" data-filter="queued">Want to Read</button>
  <button class="filter-btn" data-filter="paused">Paused</button>
</div>

{% assign all_books = site.books | sort: "started" | reverse %}
{% assign displayed_years = "" %}

{% for book in all_books %}
  {% assign yr = book.started | date: '%Y' %}
  {% unless displayed_years contains yr %}
    {% if displayed_years != "" %}
      </div><!-- /library-grid -->
    {% endif %}
    <h2 class="library-year">{{ yr }}</h2>
    <div class="library-grid">
    {% assign displayed_years = displayed_years | append: yr | append: "," %}
  {% endunless %}

  {% assign status_lower = book.status | downcase | strip | default: "uncategorized" %}
  <div class="book-card" data-status="{{ status_lower }}">
    <a href="{{ book.url | relative_url }}">
      <div class="book-cover-wrap">
        {% if book.cover %}
          <img src="{{ book.cover | relative_url }}" alt="{{ book.title }}" loading="lazy">
        {% elsif book.olid %}
          <img src="https://covers.openlibrary.org/b/olid/{{ book.olid }}-M.jpg" alt="{{ book.title }}" loading="lazy">
        {% elsif book.isbn %}
          <img src="https://covers.openlibrary.org/b/isbn/{{ book.isbn }}-M.jpg" alt="{{ book.title }}" loading="lazy">
        {% elsif book.cover_goodreads %}
          <img src="{{ book.cover_goodreads }}" alt="{{ book.title }}" loading="lazy">
        {% endif %}
        {% if book.status %}
          <span class="book-status-badge badge-{{ status_lower }}">{{ book.status }}</span>
        {% endif %}
      </div>
      <div class="book-info">
        <div class="book-title">{{ book.title }}</div>
        <div class="book-author">{{ book.author }}</div>
        {% if book.stars %}
          <div class="book-stars">
            {% assign full  = book.stars | floor %}
            {% assign empty = 5 | minus: full %}
            {% for i in (1..full)  %}★{% endfor %}{% for i in (1..empty) %}<span class="empty">★</span>{% endfor %}
          </div>
        {% endif %}
      </div>
    </a>
  </div>
{% endfor %}

{% if all_books.size > 0 %}
  </div><!-- /library-grid -->
{% endif %}

<script>
  (function () {
    var btns  = document.querySelectorAll('.filter-btn');
    var cards = document.querySelectorAll('.book-card');
    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        btns.forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        var f = btn.dataset.filter;
        cards.forEach(function (card) {
          if (f === 'all' || card.dataset.status === f) {
            card.classList.remove('hidden');
          } else {
            card.classList.add('hidden');
          }
        });
      });
    });
  })();
</script>
