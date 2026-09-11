# EntertainmentHub / FILMS

Django localhost movie/series website with a custom admin dashboard.

## Main features

- Responsive public movie library.
- Fixed/positioned responsive EntertainmentHub header with a replaceable logo asset at `WEBSITE/static/WEBSITE/img/site-logo.png`.
- Footer appears through `base.html` on child pages and includes Email, TikTok, Instagram, X, YouTube and LinkedIn icons/links plus contact information.
- Public search and combined filters: title/description, genre, year, Umusobanuzi and Movie/Series type.
- Umusobanuzi is a separate managed entity. The initial migration seeds names seen in the supplied site reference (Yanga, B-The Great, Rocky Kimomo, Junior Giti, Sankara, Savimbi, PK, Gaheza and Simba); the admin can add more through the custom dashboard.
- Registered users can upload promotional Shorts. User uploads are `pending` until the content administrator approves them; the admin can publish, reject, edit or delete them.
- The admin can create/edit/delete movies, episodes, genres, Abasobanuzi, comments and promotional Shorts entirely through custom webpages.
- No Django `/admin/` URL is exposed; normal content management is done through `/dashboard/`.
- Only the configured content administrator can access `/dashboard/`.
- Visitor appearance controls work without an account: night/day mode, 60 themes and English/Kinyarwanda/French/Kiswahili/Spanish interface translation. Preferences are saved in browser localStorage.
- Likes, comments, local video range streaming, playback speed and ±10 second seeking are retained.
- Google Drive/YouTube/direct media URL support is retained.

## Localhost setup

```powershell
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py setup_content_admin
py manage.py runserver
```

Website: `http://127.0.0.1:8000/`

Login: `http://127.0.0.1:8000/account/login/`

Admin dashboard: `http://127.0.0.1:8000/dashboard/`

Default admin username: `admin` (choose the password during `setup_content_admin`).

## Replace the logo later

Replace:

`WEBSITE/static/WEBSITE/img/site-logo.png`

with the supplied final logo (keeping the same filename/format), then refresh the browser. The header, dashboard header and footer already use that asset.

## Content rights

Only upload, host, advertise or distribute movies/videos for which you have the necessary rights or permission.


## Discovery filters
The public library supports combined filtering/search by title or description, genre, Umusobanuzi, production/filming/cast-origin country, exact release year, Movie/Series type, minimum rating, maximum duration, featured-only, and sorting by newest/oldest/year/rating/title. The Umusobanuzi list is also available as a dedicated dropdown in the public navigation.

## Countries
Movies can be assigned one or more countries from the custom movie publishing webpage. The project seeds a broad country list during migration; the field is intended for production, filming location, or cast-origin information.

## Promotional Shorts
The admin can publish promotional Shorts from the dashboard. Registered users can upload Shorts for admin review before publication.


## Branding and discovery UI
- The supplied logo is used in the public and admin headers as `WEBSITE/static/WEBSITE/img/site-logo.png`.
- The public header contains the normal movie search. The advanced filter panel intentionally does not contain a second search box; it provides Genre, Umusobanuzi, Country, Year, Type, rating, duration, Featured and sorting filters.
- The header search remains independent from the filter panel so visitors have one clear normal-search entry point.

## Movie posters and trailers

- Movie posters work from either the local `poster_image` upload or a public image URL. Google Drive sharing links are converted to an image-display URL automatically.
- The movie details page now shows a **Trailer** button whenever a trailer file or trailer URL is configured. Local trailer files use the project's range-enabled streaming endpoint; YouTube, Google Drive and direct video URLs use the existing URL normalizer.
- The **Watch now** action remains separate, so visitors can preview the trailer before opening the full movie.
- Movie/series publishing remains restricted to the single configured content administrator. Run `py manage.py setup_content_admin` to create/repair that account and set its password.

## Render + Supabase PostgreSQL

Production is configured to use PostgreSQL from the `DATABASE_URL` environment variable. SQLite remains available only for local development when `DJANGO_DEBUG=1` and `DATABASE_URL` is not set.

### Render environment variables

Set these environment variables on the Render Web Service before deploying:

- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY` = a long random secret (Render can generate this automatically when using `render.yaml`)
- `DJANGO_ALLOWED_HOSTS=entertainmenthub-l0yx.onrender.com` (add any custom domain separated by commas)
- `CONTENT_ADMIN_USERNAME=admin`
- `DATABASE_URL` = the PostgreSQL connection string supplied by Supabase

### Supabase connection

In Supabase, create a project and copy its PostgreSQL connection string. For a Render-hosted Django app, the Supabase connection string should be placed in Render as the `DATABASE_URL` secret; do not put the password into source code, `.env.example`, GitHub, or `render.yaml`.

The included `build.sh` installs dependencies, collects static files, and runs all Django migrations automatically on every Render build.

### Important database behavior

Do not use the production `db.sqlite3` as the Render database. Published movies, users, comments, likes and other database records are stored in Supabase PostgreSQL when `DATABASE_URL` is configured. This prevents records from disappearing when the Render web service restarts or redeploys.

Uploaded files under `MEDIA_ROOT` are still stored on the Render filesystem and therefore are not permanent production storage. Use permanent external object storage for uploaded posters/videos if you need those files to survive Render restarts/redeploys. External movie/video URLs stored in PostgreSQL remain as database records, but the external provider itself must keep those URLs/files available.
