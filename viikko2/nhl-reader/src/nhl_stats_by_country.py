from player import Player, PlayerReader, PlayerStats
from rich.console import Console
from rich.table import Table


def style(players):
    table = Table(title = "NHL-pelaajien tilastoja", border_style="blue")
    table.add_column("Nimi", style="bold")
    table.add_column("Maalit", style="purple")
    table.add_column("Syötöt", style="green")
    table.add_column("Pisteet", style="bold yellow")

    for p in players:
        points = p.goals + p.assists
        table.add_row(p.name, str(p.goals), str(p.assists), str(points))

    return table

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality("SWE")

    console = Console()
    console.print(style(players))

if __name__ == "__main__":
    main()
