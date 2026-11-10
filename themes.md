---
layout: page
title: Thèmes
permalink: /themes/
---
Neuf familles de sujets, calculées à partir du vocabulaire des articles (voir `scripts/carte.py`). Chaque article appartient à la famille dont il est le plus proche.

{% assign groups = site.posts | group_by: "theme" | sort: "name" %}
<nav class="theme-index">{% for g in groups %}<a href="#{{ g.name | slugify }}">{{ g.name }} ({{ g.size }})</a>{% endfor %}</nav>

{% for g in groups %}
<section class="theme-section" id="{{ g.name | slugify }}">
<h2>{{ g.name }} <small>{{ g.size }} articles</small></h2>
<details><summary>Voir les articles</summary>
<ul class="plist">{% for post in g.items %}<li><span class="src src-{{ post.source }}" title="{{ post.source_name }}"></span><span class="pd">{{ post.date | date: "%Y" }}</span><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></li>{% endfor %}</ul>
</details>
</section>
{% endfor %}
