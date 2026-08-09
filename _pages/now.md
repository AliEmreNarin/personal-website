---
layout: page
title: now
permalink: /now/
description: What I'm currently reading and want to read next.
nav: true
nav_order: 5
---

<style>
  .now-section-title {
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--global-text-color-light, #6c757d);
    margin: 0 0 1.25rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--global-divider-color, #dee2e6);
  }
  .now-section-title:not(:first-child) { margin-top: 3rem; }
  .now-grid {
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
  .badge-reading  { background: rgba(30,80,180,0.85); }
  .badge-queued   { background: rgba(100,100,100,0.75); }
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
  }
</style>

{% assign reading_books = site.books | where: "status", "Reading" %}
{% assign queued_books  = site.books | where: "status", "Queued" %}

<h2 class="now-section-title">Reading</h2>

{% if reading_books.size > 0 %}

<div class="now-grid">
  {% for book in reading_books %}
  <div class="book-card">
    <a href="{{ book.url | relative_url }}">
      <div class="book-cover-wrap">
        {% if book.cover %}<img src="{{ book.cover | relative_url }}" alt="{{ book.title }}" loading="lazy">
        {% elsif book.olid %}<img src="https://covers.openlibrary.org/b/olid/{{ book.olid }}-M.jpg" alt="{{ book.title }}" loading="lazy">
        {% elsif book.isbn %}<img src="https://covers.openlibrary.org/b/isbn/{{ book.isbn }}-M.jpg" alt="{{ book.title }}" loading="lazy">
        {% elsif book.cover_goodreads %}<img src="{{ book.cover_goodreads }}" alt="{{ book.title }}" loading="lazy">
        {% endif %}
        <span class="book-status-badge badge-reading">Reading</span>
      </div>
      <div class="book-info">
        <div class="book-title">{{ book.title }}</div>
        <div class="book-author">{{ book.author }}</div>
      </div>
    </a>
  </div>
  {% endfor %}
</div>
{% else %}
<p class="now-empty">Nothing in progress right now.</p>
{% endif %}

<h2 class="now-section-title">Want to Read</h2>

{% if queued_books.size > 0 %}

<div class="now-grid">
  {% for book in queued_books %}
  <div class="book-card">
    <a href="{{ book.url | relative_url }}">
      <div class="book-cover-wrap">
        {% if book.cover %}<img src="{{ book.cover | relative_url }}" alt="{{ book.title }}" loading="lazy">
        {% elsif book.olid %}<img src="https://covers.openlibrary.org/b/olid/{{ book.olid }}-M.jpg" alt="{{ book.title }}" loading="lazy">
        {% elsif book.isbn %}<img src="https://covers.openlibrary.org/b/isbn/{{ book.isbn }}-M.jpg" alt="{{ book.title }}" loading="lazy">
        {% elsif book.cover_goodreads %}<img src="{{ book.cover_goodreads }}" alt="{{ book.title }}" loading="lazy">
        {% endif %}
        <span class="book-status-badge badge-queued">Queued</span>
      </div>
      <div class="book-info">
        <div class="book-title">{{ book.title }}</div>
        <div class="book-author">{{ book.author }}</div>
      </div>
    </a>
  </div>
  {% endfor %}
</div>
{% else %}
<p class="now-empty">Nothing queued yet.</p>
{% endif %}
