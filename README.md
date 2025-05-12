# 🎮 Pokémon Web Scraper

This project is a dynamic web scraper built using **Selenium** that extracts structured data for each Pokémon from [Pokémon Database](https://pokemondb.net). It collects stats, types, forms, abilities, and more, and stores the results both in a **MySQL database** and an **Excel spreadsheet**.

---

## 📌 Features

- 🔍 Scrapes detailed Pokémon data including:
  - Name, Form, Species, Type(s)
  - Height, Weight
  - Abilities (1, 2, Hidden)
  - Stats (HP, Attack, Defence, Special Stats, Speed, Total)
- 🔄 Automatically navigates through all Pokémon pages
- 🧠 Differentiates between multiple forms via smart tab selection
- 💾 Stores data in:
  - `MySQL` using SQLAlchemy ORM
  - `Excel` file (`data/pokemon.xlsx`)
- 🪵 Logging enabled for tracking scraping progress and errors (`logs/pokemon.log`)

---

## 🏗️ Project Structure

```
Pokemon-WebScraper/
│
├── pokemon.py          # Main scraper class and logic
├── model.py            # SQLAlchemy model (PokemonDB)
├── database.py         # DB connection and session setup
├── requirements.txt    # Project dependencies
├── .gitignore
└── credentials.env     # Contains DB password (not committed)
```

---

## 🧰 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

Ensure the following packages are available:

- `selenium==4.8.2`
- `pandas==1.5.3`
- `sqlalchemy==2.0.5.post1`
- `openpyxl==3.1.1`
- `python-dotenv~=1.0.0`
- `mysqlclient==2.1.1`

---

## 🔐 Environment Setup

Create a `.env` file in the root directory with the following content:

```env
PASSWD=your_mysql_password
```

> ⚠️ Make sure MySQL is installed and running. The scraper connects to:
> `mysql://root:<PASSWD>@localhost/pokemon_db`

---

## 🚀 Running the Scraper

```bash
python pokemon.py
```

- A Chrome browser will open in **incognito** mode and start scraping.
- The final output is saved in:
  - MySQL table: `pokemon`
  - Excel file: `data/pokemon.xlsx`
  - Logs: `logs/pokemon.log`

> 📎 The scraper starts from **Bulbasaur** and iteratively navigates using the "Next" button.

---

## 📂 Output Sample (Excel)

| Index | Name     | Form       | Type 1 | Type 2 | HP | Attack | ... |
|-------|----------|------------|--------|--------|----|--------|-----|
| 1     | Bulbasaur| None       | Grass  | Poison | 45 | 49     | ... |
| 2     | Ivysaur  | None       | Grass  | Poison | 60 | 62     | ... |

---

## 🧱 Database Table Structure

Defined in `model.py` using SQLAlchemy ORM:

```python
class PokemonDB(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type_1 = Column(String)
    ...
```

---

## 📝 Notes

- Requires **chromedriver** inside the `driver/` directory (update path if needed).
- Built for local testing; you can extend it with Docker or cloud integration if needed.
- Ensure page structure of [pokemondb.net](https://pokemondb.net) remains unchanged; otherwise, XPath updates may be required.

---

## 📄 License

This project is for educational and personal use only. Data is publicly available on pokemondb.net.

---

## 🙋‍♂️ Author

**Arabind Meher**  
🔗 [LinkedIn](https://www.linkedin.com/in/arabind-meher) • [GitHub](https://github.com/arabind-meher)
