#!/usr/bin/env python
"""
Run Visualizer Tool

This script finds the most recent execution data file and runs the visualization tool.
It's a convenience wrapper around visualize_interactions.py.

Usage:
    python -m src.customeroutreach.tools.run_visualizer [--latest|--file=PATH]
"""

import os
import sys
import glob
import subprocess
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def find_latest_execution_data():
    """Find the most recent execution data file"""
    # Check multiple possible locations for the execution data
    search_dirs = [
        "agent_visualizations/",
        "./agent_visualizations/",
        "../agent_visualizations/",
        "../../agent_visualizations/",
        "./",
        "../",
        "outputs_*/"
    ]
    
    all_files = []
    
    for directory in search_dirs:
        pattern = f"{directory}execution_data_*.json"
        files = glob.glob(pattern)
        if files:
            all_files.extend(files)
    
    if not all_files:
        console.print("[yellow]No execution data files found in any of the expected directories[/yellow]")
        return None
    
    # Sort by modification time (newest first)
    latest_file = max(all_files, key=os.path.getmtime)
    return latest_file

def list_available_execution_data():
    """List all available execution data files"""
    # Check multiple possible locations for the execution data
    search_dirs = [
        "agent_visualizations/",
        "./agent_visualizations/",
        "../agent_visualizations/",
        "../../agent_visualizations/",
        "./",
        "../",
        "outputs_*/"
    ]
    
    all_files = []
    
    for directory in search_dirs:
        pattern = f"{directory}execution_data_*.json"
        files = glob.glob(pattern)
        if files:
            all_files.extend(files)
    
    if not all_files:
        console.print("[yellow]No execution data files found in any of the expected directories[/yellow]")
        return None
    
    # Create a table of files
    table = Table(title="Available Execution Data Files")
    table.add_column("Index", style="cyan")
    table.add_column("Timestamp", style="green")
    table.add_column("File", style="blue")
    table.add_column("Size", style="magenta")
    
    # Sort by modification time (newest first)
    all_files.sort(key=os.path.getmtime, reverse=True)
    
    for i, file in enumerate(all_files):
        # Extract timestamp from filename
        try:
            timestamp_str = file.split("execution_data_")[1].split(".json")[0]
            timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            timestamp_display = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, IndexError):
            timestamp_display = "Unknown"
        
        # Get file size
        try:
            size = os.path.getsize(file)
            if size < 1024:
                size_str = f"{size} bytes"
            elif size < 1024 * 1024:
                size_str = f"{size/1024:.1f} KB"
            else:
                size_str = f"{size/(1024*1024):.1f} MB"
        except (OSError, IOError):
            size_str = "Unknown"
        
        table.add_row(str(i+1), timestamp_display, file, size_str)
    
    console.print(table)
    return all_files

def run_visualization_tool(data_file):
    """Run the visualization tool on the specified data file"""
    console.print(Panel(f"[bold]Running visualization tool on:[/bold]\n{data_file}", border_style="green"))
    
    # Run the visualization tool as a subprocess
    try:
        result = subprocess.run(
            [sys.executable, "-m", "src.customeroutreach.tools.visualize_interactions", data_file],
            check=True,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error running visualization tool: {str(e)}[/bold red]")
        return False

def show_help_when_no_data():
    """Show helpful information when no data is found"""
    console.print(Panel(
        "[bold red]No execution data files found![/bold red]\n\n"
        "To generate visualization data, you need to run the demo first:\n\n"
        "1. Run the demo with visualization enabled:\n"
        "   [cyan]python -m src.customeroutreach.demo --show-steps --save-logs[/cyan]\n\n"
        "2. After the demo completes, execution data will be saved to:\n"
        "   [cyan]agent_visualizations/execution_data_*.json[/cyan]\n\n"
        "3. Then run this visualization tool again to generate interactive visualizations.",
        title="[bold]Help - No Data Found[/bold]",
        border_style="yellow"
    ))

def main():
    console.print(Panel("[bold cyan]CrewAI Visualization Tool[/bold cyan]", border_style="cyan"))
    
    # Check if a specific file was requested
    if len(sys.argv) > 1:
        if sys.argv[1] == "--latest":
            # Use the latest file
            data_file = find_latest_execution_data()
            if data_file:
                run_visualization_tool(data_file)
            else:
                show_help_when_no_data()
        elif sys.argv[1].startswith("--file="):
            # Use the specified file
            file_path = sys.argv[1][7:]  # Remove the --file= prefix
            if os.path.exists(file_path):
                run_visualization_tool(file_path)
            else:
                console.print(f"[bold red]File not found: {file_path}[/bold red]")
                show_help_when_no_data()
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            console.print(Panel(
                "Usage:\n"
                "  [cyan]python -m src.customeroutreach.tools.run_visualizer --latest[/cyan]\n"
                "     - Run with the most recent execution data file\n\n"
                "  [cyan]python -m src.customeroutreach.tools.run_visualizer[/cyan]\n"
                "     - Interactive mode: list available files and select one\n\n"
                "  [cyan]python -m src.customeroutreach.tools.run_visualizer --file=PATH[/cyan]\n"
                "     - Run with a specific execution data file",
                title="[bold]Visualization Tool Help[/bold]",
                border_style="blue"
            ))
        else:
            console.print("[yellow]Unknown option. Use --latest, --file=PATH, or --help[/yellow]")
    else:
        # Interactive mode
        console.print("[bold]Select an execution data file to visualize:[/bold]")
        files = list_available_execution_data()
        
        if not files:
            show_help_when_no_data()
            return
        
        console.print("\nEnter the index of the file to visualize, or 'l' for latest:")
        choice = input("> ")
        
        if choice.lower() == 'l':
            # Use the latest file
            run_visualization_tool(files[0])
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(files):
                    run_visualization_tool(files[index])
                else:
                    console.print(f"[bold red]Invalid index. Choose between 1 and {len(files)}[/bold red]")
            except ValueError:
                console.print("[bold red]Invalid input. Enter a number or 'l'[/bold red]")

if __name__ == "__main__":
    main() 