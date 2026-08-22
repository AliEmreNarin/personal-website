---
layout: page
title: Blog
permalink: /blog/
description: Notes on research, tools, books, and whatever else I can't stop thinking about. Favorites are marked with a ⭐.
---

{% assign known = site.data.blog_categories | map: "slug" %}

{% for cat in site.data.blog_categories %}
{% assign cat_posts = site.posts | where_exp: "p", "p.categories contains cat.slug" %}
{% if cat_posts.size > 0 %}

<section class="post-group">
  <h2>{{ cat.name }}</h2>
  {% if cat.blurb %}<p class="blurb">{{ cat.blurb }}</p>{% endif %}
  <ul class="post-list">
    {% for post in cat_posts %}
    <li>
      <span class="emoji" aria-hidden="true">{{ post.emoji | default: "✏️" }}</span>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <span class="when">({{ post.date | date: "%b '%y" }})</span>
      {% if post.featured %}<span class="star" title="A favorite">⭐</span>{% endif %}
    </li>
    {% endfor %}
  </ul>
</section>
{% endif %}
{% endfor %}

{% assign other_posts = "" | split: "" %}
{% for post in site.posts %}
{% assign first_cat = post.categories | first %}
{% unless known contains first_cat %}
{% assign other_posts = other_posts | push: post %}
{% endunless %}
{% endfor %}
{% if other_posts.size > 0 %}

<section class="post-group">
  <h2>Other</h2>
  <ul class="post-list">
    {% for post in other_posts %}
    <li>
      <span class="emoji" aria-hidden="true">{{ post.emoji | default: "✏️" }}</span>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <span class="when">({{ post.date | date: "%b '%y" }})</span>
      {% if post.featured %}<span class="star" title="A favorite">⭐</span>{% endif %}
    </li>
    {% endfor %}
  </ul>
</section>
{% endif %}

<section class="post-group">
  <h2>All posts, chronologically</h2>
  <ul class="post-list post-list--dated">
    {% for post in site.posts %}
    <li>
      <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y · %b %-d" }}</time>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </li>
    {% endfor %}
  </ul>
</section>
