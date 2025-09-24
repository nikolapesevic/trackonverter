from rich.prompt import Prompt
from rich.console import Console
import sys

console = Console()

def error(message: str):
	console.print(f"❌[bold red] Error: {message} [/bold red]")

def warn(message: str):
	console.print(f"⚠️ [bold yellow] {message} [/bold yellow]")

def success(message: str):
	console.print(f"✅[bold green] {message} [/bold green]")

def info(message: str):
	# Extra space due to crappy emoji width
	console.print(f"ℹ️[bold]  {message} [/bold]")

def prompt(message: str, default: str) -> str:
	return Prompt.get_input(prompt=f"💬 {message} [bold blue][Default: {default}][/bold blue]: ", password=False, console=console).strip() or default

def wait_for_key():
	console.print("➡️  [bold gray]Press any key to continue...[/bold gray]")

	try:
		# Try Windows first
		import msvcrt
		msvcrt.getch()
	except ImportError:
		# Unix/Linux/macOS
		import termios
		import tty
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)