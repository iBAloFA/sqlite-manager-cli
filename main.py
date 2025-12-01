import typer, sqlite3, pandas as pd, os
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="SQLite Manager CLI – beautiful terminal database browser")
console = Console()

def get_conn(db_path: str):
    if not os.path.exists(db_path):
        console.print(f"[red]Database {db_path} not found![/]")
        raise typer.Exit(1)
    return sqlite3.connect(db_path)

@app.command()
def tables(db: str):
    """List all tables"""
    conn = get_conn(db)
    df = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    console.print(df)

@app.command()
def query(db: str, sql: str):
    """Run any SQL query with pretty output"""
    conn = get_conn(db)
    df = pd.read_sql(sql, conn)
    table = Table(*df.columns, show_header=True, header_style="bold magenta")
    for _, row in df.iterrows():
        table.add_row(*[str(x) for x in row])
    console.print(table)

@app.command()
def export(db: str, table_name: str):
    """Export table to CSV and JSON"""
    conn = get_conn(db)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    df.to_csv(f"{table_name}.csv", index=False)
    df.to_json(f"{table_name}.json", orient="records", indent=2)
    console.print(f"[green]Exported {table_name} → {table_name}.csv & {table_name}.json[/]")

if __name__ == "__main__":
    app()
