---
layout: page
title: Derniers articles
permalink: /recents/
---
<ul class="plist">
{% for post in site.posts limit:80 %}<li><span class="src src-{{ post.source }}">{{ post.source_name }}</span><span class="pd">{{ post.date | date: "%d/%m/%Y" }}</span><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></li>
{% endfor %}
</ul>
<p><a href="{{ site.baseurl }}/archives/">Toutes les archives →</a></p>
