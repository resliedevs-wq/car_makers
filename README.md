# Who Builds the World's Cars

2025 light-vehicle production shown as 1,000 mini cars: an inner ring for the country of assembly, an outer ring for the brands built there, and click-to-zoom into each country's brands and models. Brands that would not fill half a mini car are dropped.

## Layout

- `data/build_data.py`: the dataset (country × brand × model) and the counting rules. Writes `data/cars2025.json` and `data/cars2025.csv`.
- `web/template.html`: the interactive page (no dependencies besides Google Fonts).
- `data/build_page.py`: injects the JSON into the template, producing `web/index.html`.

## Rebuild

```sh
python3 data/build_data.py
python3 data/build_page.py
```

Open `web/index.html` in a browser.

## Data notes

Units are thousands of light vehicles (cars, SUVs, pickups, vans) assembled in each country in calendar 2025. Each brand row is marked `r` (reported by an official body or the maker) or `e` (estimated: split from a group total or rebuilt from plant output). Model splits are always estimates. Country totals come from the [OICA 2025 table](https://oica.net/wp-content/uploads/2025/11/prod-total-2025.pdf) minus medium and heavy trucks and buses. Mexico uses official INEGI figures by manufacturer. The page's methodology section lists the other sources.
