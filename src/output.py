from rich import print as rprint
from rich.prompt import Prompt

def error(message: str):
	rprint(f"❌ [bold red]Error: {message} [/bold red]")

def warn(message: str):
	rprint(f"⚠️ [bold yellow] {message} [/bold yellow]")

def success(message: str):
	rprint(f"✅ [bold green] {message} [/bold green]")

def info(message: str):
	rprint(f"ℹ️ [bold blue] {message} [/bold blue]")

def prompt(message: str, default: str) -> str:
	rprint(f"💬 {message} [bold blue][Default: {default}][/bold blue]: ")
	return input().strip() or default