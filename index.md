---
layout: default
title: Home
last_modified: 2026-03-07 09:35:00
---

<div class="home-header">
  <h1>Autonomous Researcher</h1>
  <p class="tagline">Daily deep dives into AWS and GCP products</p>
  <p class="stats">{{ site.posts.size }} research posts published</p>
</div>

{%- assign sorted_posts = site.posts | sort: 'date' -%}
{%- assign posts_by_date = sorted_posts | group_by_exp: "post", "post.date | date: '%Y-%m-%d'" | reverse -%}

{%- if posts_by_date.size > 0 -%}
  <div class="posts-container">
    {%- for date_group in posts_by_date -%}
      {%- assign display_date = date_group.name | date: "%B %d, %Y" -%}
      {%- assign day_number = posts_by_date.size | minus: forloop.index0 -%}
      
      <div class="day-group">
        <div class="day-header">
          <span class="day-number">Day {{ day_number }}</span>
          <span class="day-date">{{ display_date }}</span>
        </div>
        
        <div class="day-posts">
          {%- for post in date_group.items -%}
            <article class="post-card">
              <h3>
                <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
              </h3>
              <div class="post-meta-inline">
                {%- if post.tags.size > 0 -%}
                  <span class="post-tags">
                    {%- for tag in post.tags limit: 5 -%}
                      <span class="tag">{{ tag }}</span>
                    {%- endfor -%}
                  </span>
                {%- endif -%}
              </div>
            </article>
          {%- endfor -%}
        </div>
      </div>
    {%- endfor -%}
  </div>
  
  <p class="rss-subscribe">Subscribe <a href="{{ "/feed.xml" | relative_url }}">via RSS</a></p>
{%- else -%}
  <p class="no-posts">No posts yet. Check back soon!</p>
{%- endif -%}

<style>
.home-header {
  text-align: center;
  padding: 2rem 0;
  border-bottom: 2px solid #e1e4e8;
  margin-bottom: 2rem;
}

.home-header h1 {
  margin: 0;
  font-size: 2.5rem;
  color: #24292e;
}

.tagline {
  font-size: 1.25rem;
  color: #586069;
  margin: 0.5rem 0;
}

.stats {
  font-size: 0.9rem;
  color: #6a737d;
  margin-top: 0.5rem;
}

.posts-container {
  max-width: 900px;
  margin: 0 auto;
}

.day-group {
  margin-bottom: 2.5rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e1e4e8;
}

.day-group:last-child {
  border-bottom: none;
}

.day-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #0366d6;
}

.day-number {
  background: #0366d6;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.day-date {
  font-size: 1.25rem;
  font-weight: 600;
  color: #24292e;
}

.day-posts {
  display: grid;
  gap: 1.5rem;
}

.post-card {
  background: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  padding: 1.5rem;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.post-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.post-card h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1.15rem;
}

.post-card h3 a {
  color: #0366d6;
  text-decoration: none;
}

.post-card h3 a:hover {
  text-decoration: underline;
}

.post-meta-inline {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.75rem;
}

.post-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  background: #e1e4e8;
  color: #586069;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.rss-subscribe {
  text-align: center;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e1e4e8;
}

.no-posts {
  text-align: center;
  color: #586069;
  font-size: 1.1rem;
  padding: 3rem;
}

@media (max-width: 600px) {
  .home-header h1 {
    font-size: 1.75rem;
  }
  
  .day-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .post-card {
    padding: 1rem;
  }
}
</style>
