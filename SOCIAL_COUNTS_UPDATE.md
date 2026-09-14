# Movie social-style counters

Added without removing the existing project features:
- Movie `view_count`: increases whenever a visitor opens a published movie detail page.
- Movie `download_count`: increases whenever a movie download is clicked; external/cloud download URLs are routed through Django so they are counted too.
- Existing `MovieLike` remains unchanged and its count is shown alongside views/downloads.
- Counters are displayed on movie posters on the home/library and genre pages.
- Counters are also shown on the movie detail page.
- Admin displays counters as read-only.
- Migration: `0011_movie_engagement_counts.py`.

The counters count actions, not unique users. Refreshing/reopening a movie detail page counts another view.
