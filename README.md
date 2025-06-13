# Random-Movie-Generator

Choose filters and get a list of matching movies.  
Or Hit *Random* and the app serves a single surprise title.

---

## ✨ Features
| | |
|-|-|
| **Filter-driven search** – Year, genre, critic score and more; returns results in < 200 ms. |
| **“I’m Feeling Lucky” button** – One click fetches a random hidden gem. |
| **Live critic data** – Scrapes Rotten Tomatoes / Metacritic (2 × daily) for up-to-date ratings. |
| **Responsive UI** – Plain HTML/CSS enhanced with Tailwind utility classes; mobile-first layout. |
| **Python back-end** – Flask handles API endpoints; Django templating (Jinja2) renders pages. |

---

## 🚀 Quick Start

### Prereqs
- Python 3.9+  
- `virtualenv` *(optional but recommended)*

### 1 · Clone & install
```bash
git clone https://github.com/your-handle/movie-discovery.git
cd movie-discovery
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Project Structure

```
├── app.py                    ← Flask entry-point (routes + logic)
├── README.md
├── .gitignore                ← keeps __pycache__ and scrape cache out of Git
├── templates/                ← HTML (Jinja2) files
│   ├── metacritic_results.html
│   ├── index.html
│   └── random_results.html
|   └── rotten_results.html
```

No affiliation with Rotten Tomatoes or metacritic.
