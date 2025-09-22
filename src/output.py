from rich.prompt import Prompt
from rich.console import Console

console = Console()

def error(message: str):
	console.print(f"❌[bold red] Error: {message} [/bold red]")

def warn(message: str):
	console.print(f"⚠️ [bold yellow] {message} [/bold yellow]")

def success(message: str):
	console.print(f"✅[bold green] {message} [/bold green]")

def info(message: str):
	# Extra space due to crappy emoji width
	console.print(f"ℹ️[bold blue]  {message} [/bold blue]")

def prompt(message: str, default: str) -> str:
	return Prompt.get_input(prompt=f"💬 {message} [bold blue][Default: {default}][/bold blue]: ", password=False, console=console).strip() or default