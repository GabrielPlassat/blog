---
layout: page
title: MétaNotes
permalink: /metanotes/
---
Les MétaNotes prennent du recul sur un sujet — les énergies, la surveillance, l'avenir du vélo, du camion, de l'automobile, du voyage… — pour en dégager les tendances de fond. La première, la MétaNote N°0 (2009), posait déjà le passage de l'objet véhicule aux services de mobilité.

{% assign notes = site.posts | where: "categorie", "metanote" | sort: "date" %}
<p class="note">{{ notes.size }} MétaNotes, de la plus ancienne à la plus récente.</p>
<ul class="plist">
{% for post in notes %}<li><span class="pd">{{ post.date | date: "%m/%Y" }}</span><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></li>
{% endfor %}
</ul>
