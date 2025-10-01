import typer

app = typer.Typer(help="Jobcopilot CLI")


@app.command()
def version() -> None:
    """Show version."""
    from jobcopilot import __version__

    typer.echo(__version__)


if __name__ == "__main__":
    app()
