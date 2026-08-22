---
layout: page
title: Library
permalink: /library/
wide: true
---

{% assign reading = site.books | where: "status", "Reading" %}
{% assign queued = site.books | where: "status", "Queued" %}
{% assign past = site.books | where_exp: "b", "b.status != 'Reading' and b.status != 'Queued'" | sort: "started" | reverse %}
{% assign by_year = past | group_by: "year" | sort: "name" | reverse %}

<div class="tabs" role="tablist" data-tabs>
  <button class="tab" role="tab" data-tab="present" aria-selected="true">present <span class="count">{{ reading.size | plus: queued.size }}</span></button>
  <button class="tab" role="tab" data-tab="past" aria-selected="false">past <span class="count">{{ past.size }}</span></button>
</div>

<div data-pane="present">
  <section class="shelf">
    <div class="shelf-head"><h2>Reading</h2><span class="count">{{ reading.size }}</span></div>
    {% if reading.size > 0 %}
      {% include book-grid.html books=reading %}
    {% else %}
      <p class="empty">Nothing in progress right now.</p>
    {% endif %}
  </section>

  <section class="shelf">
    <div class="shelf-head"><h2>Want to read</h2><span class="count">{{ queued.size }}</span></div>
    {% if queued.size > 0 %}
      {% include book-grid.html books=queued %}
    {% else %}
      <p class="empty">Nothing queued yet.</p>
    {% endif %}
  </section>
</div>

<div data-pane="past" hidden>
  {% for group in by_year %}
  <section class="shelf">
    <div class="shelf-head"><h2>{{ group.name }}</h2><span class="count">{{ group.items.size }}</span></div>
    {% include book-grid.html books=group.items stars=true %}
  </section>
  {% endfor %}
</div>
