from libsql_experimental import connect

# ✅ IMPORTANT: use https, NOT libsql://
client = connect(
    "https://reading-progress-dusanzoric6.aws-eu-west-1.turso.io",
    auth_token="eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NzU3MzU3MTcsImlkIjoiMDE5ZDcyMTctZWQwMS03Zjg1LWJmM2YtYjZiNGMyYmJjZWE4IiwicmlkIjoiOTM5N2U2MmEtY2Y2Ni00NGFjLWIxYTYtZmVkZGQwZDVlZDJmIn0.O2G5JsA3cgjR7z12-OJ1Xje4ZBl8HUL0t2lfLs8bl-9CbatbMaSVYfQkC0wFoHgG6uCGADnAsGihZFhC9x4eCA"
)

# ✅ Ensure table exists
client.execute("""
CREATE TABLE IF NOT EXISTS progress (
    book TEXT NOT NULL,
    chapter INTEGER NOT NULL
);
""")

def get_progress(book):
    rows = client.execute(
        "SELECT chapter FROM progress WHERE book = ? ORDER BY chapter;",
        (book,)
    ).fetchall()
    return [r[0] for r in rows]

def save_progress(book, chapters):
    client.execute("DELETE FROM progress WHERE book = ?", (book,))
    for ch in chapters:
        client.execute(
            "INSERT INTO progress (book, chapter) VALUES (?, ?)",
            (book, ch)
        )
    client.commit()