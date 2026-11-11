---
layout: page
title: Fictions
permalink: /fictions/
---
<img class="illustration-page" src="{{ '/assets/images/illustrations/fictions.svg' | relative_url }}" alt="" width="120" height="120">
Des récits d'anticipation pour rendre tangibles des futurs possibles des mobilités : Google ou Amazon opérateurs de transport, une voiture qui conseille de ne pas l'utiliser, la congestion robotisée… Pourquoi écrire des fictions ? Réponse dans [Et si la fiction facilitait le passage à l'action ?]({{ site.baseurl }}/2013/11/et-si-la-fiction-facilitait-le-passage-a-laction/).

{% assign fx = site.posts | where: "categorie", "fiction" | sort: "date" %}
<p class="note">{{ fx.size }} fictions, de la plus ancienne à la plus récente.</p>
<ul class="plist">
{% for post in fx %}<li><span class="pd">{{ post.date | date: "%m/%Y" }}</span><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></li>
{% endfor %}
</ul>
