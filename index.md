---
layout: default
title: Home
---

<h2>Latest Posts</h2>

{%- if site.posts.size > 0 -%}
  <ul class="post-list">
    {%- for post in site.posts -%}
    <li>
      <span class="post-meta">{{ post.date | date: "%B %d, %Y" }}</span>
      <h3>
        <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
      </h3>
      {%- if site.show_excerpts -%}
        <p>{{ post.excerpt }}</p>
      {%- endif -%}
    </li>
    {%- endfor -%}
  </ul>
  
  <p class="rss-subscribe">Subscribe <a href="{{ "/feed.xml" | relative_url }}">via RSS</a></p>
{%- else -%}
  <p>No posts yet. Check back soon!</p>
{%- endif -%}
