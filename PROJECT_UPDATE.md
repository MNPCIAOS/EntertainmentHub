# Project update — September 2026

This version keeps the existing movie, series, episode, genre, narrator, country, filtering, comments, likes, accounts, dashboard, and Render deployment setup.

Updates:
- Removed Shorts from the application UI, views, URLs, dashboard, model, and media files.
- Added migration 0009_remove_short_add_feedback.py. Running `py manage.py migrate` removes the Short database table/data and creates the Feedback table.
- Added a public Contact & Feedback page. Visitors can submit feedback without registering or logging in.
- Added Feedback management to the content dashboard and Django admin.
- Featured movies now show the selected movie poster in the homepage hero.
- Added homepage rows grouped by each genre, while keeping the existing library/filter area.
