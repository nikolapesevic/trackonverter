from rich import print as rprint
from rich.prompt import Prompt
from rich.console import Console

console = Console()

def error(message: str):
	rprint(f"❌[bold red] Error: {message} [/bold red]")

def warn(message: str):
	rprint(f"⚠️ [bold yellow] {message} [/bold yellow]")

def success(message: str):
	rprint(f"✅[bold green] {message} [/bold green]")

def info(message: str):
	rprint(f"ℹ️[bold blue]  {message} [/bold blue]") # Extra space due to crappy emoji width

def prompt(message: str, default: str) -> str:
	return Prompt.get_input(console, prompt=f"💬 {message} [bold blue][Default: {default}][/bold blue]: ", password=False).strip() or default