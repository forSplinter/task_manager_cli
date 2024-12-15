import typer
from rich.console import Console
from typing import Optional
from model_task import Todo
from rich.table import Table
import database

console = Console()

app = typer.Typer()


@app.command(short_help="Adds an item")
def add(task: str, category: str):
    typer.echo(f"Adding {task}, {category}")
    todo = Todo(task, category)
    database.insert_todo(todo)
    show()


@app.command(short_help="Deletes an item")
def delete(position: int):
    typer.echo(f"Deleting task at position {position}")
    database.delete_task(position - 1)
    show()


@app.command(short_help="Updates an item")
def update(position: int, task: Optional[str] = None, category: Optional[str] = None):
    typer.echo(f"Updating task at position {position}")
    database.update_task(position - 1, task, category)
    show()


@app.command(short_help="Marks an item as complete")
def complete(position: int):
    typer.echo(f"Completing task at position {position}")
    database.complete_task(position - 1)
    show()


@app.command(short_help="Shows the current tasks")
def show():
    # Simulated list of tasks for demonstration purposes
    tasks = [
        Todo("Todo1", "Study"),
        Todo("Todo2", "Sport"),
    ]

    console.print("[bold magenta]Todos[/bold magenta]!", "🖥️")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category):
        COLORS = {
            "Learn": "cyan",
            "Coding": "orange",
            "Sport": "green",
            "Jisep": "purple",
        }
        return COLORS.get(category, "white")

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = "✅" if task.status == 2 else "❌"
        table.add_row(
            str(idx),
            task.task,
            f"[{c}]{task.category}[/{c}]",
            is_done_str,
        )
    console.print(table)


if __name__ == "__main__":
    app()

