from player import Player, PlayerReader, PlayerStats
from rich.console import Console
from rich.table import Table

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality("SWE")

    console = Console()
    table = Table(title = "[bold italic]NHL-pelaajien tilastoja kansallisuuksittain[/]", border_style="blue")
    table.add_column("Nimi", style="bold")
    table.add_column("Maalit", style="purple")
    table.add_column("Syötöt", style="green")
    table.add_column("Pisteet", style="bold yellow")

    for player in players:
        table.add_row(player.name, str(player.goals), str(player.assists), str(player.goals + player.assists))
    
    console.print(table)

if __name__ == "__main__":
    main()
