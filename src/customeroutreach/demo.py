from customeroutreach.crew import CustomerOutreach, set_educational_mode
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.syntax import Syntax
from rich.live import Live
import argparse
import os
import time
from datetime import datetime

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Run CustomerOutreach Demo")
    parser.add_argument("--company", default="Manpower Group Poland", help="Target company name")
    parser.add_argument("--industry", default="HR and Recruitment", help="Company industry")
    parser.add_argument("--decision-maker", default="Tomasz Walenczak", help="Key decision maker")
    parser.add_argument("--position", default="Country Manager", help="Decision maker position")
    parser.add_argument("--verbose", action="store_true", help="Display more verbose output")
    parser.add_argument("--educational", action="store_true", help="Show educational explanations")
    args = parser.parse_args()
    
    # Configure educational mode
    set_educational_mode(args.educational)
    
    # Display intro banner for the demo with improved styling
    console.print(Panel.fit(
        "[bold cyan]Customer Outreach Multi-Agent System Demo[/bold cyan]\n\n"
        "[yellow]This demo showcases a multi-agent system working together to:[/yellow]\n"
        "1. [green]Research and profile[/green] a target company\n"
        "2. [blue]Create[/blue] a personalized outreach message\n"
        "3. [magenta]Evaluate and improve[/magenta] the message quality\n"
        "4. [cyan]Finalize[/cyan] the perfect outreach\n\n"
        "[dim]Each agent has specialized expertise and responsibilities in the workflow[/dim]",
        title="🤖 [bold]Multi-Agent System Demo[/bold] 🤖",
        border_style="cyan"
    ))
    
    if args.educational:
        console.print(Panel.fit(
            "[bold yellow]Educational Mode Enabled[/bold yellow]\n\n"
            "You'll see explanations about:\n"
            "• [green]Agent roles and specializations[/green]\n"
            "• [blue]Task delegation and coordination[/blue]\n"
            "• [magenta]Multi-agent system architecture[/magenta]\n"
            "• [cyan]Agent communication patterns[/cyan]\n"
            "• [yellow]Output after each phase completion[/yellow]",
            border_style="yellow"
        ))
        
        console.print(Panel.fit(
            "[bold yellow]Tool Outputs Hidden[/bold yellow]\n\n"
            "When running with --educational flag, you'll see only agent progress, phase transitions, and outputs without the detailed tool inputs/outputs.\n"
            "Each phase of the process will be clearly explained, and you'll see the output from each agent after they complete their task.\n"
            "This provides a cleaner and more educational view of the agent workflow.",
            border_style="yellow"
        ))
    
    # Show the demo configuration
    table = Table(title="Demo Configuration")
    table.add_column("Parameter", style="cyan", justify="right")
    table.add_column("Value", style="green")
    
    table.add_row("Target Company", args.company)
    table.add_row("Industry", args.industry)
    table.add_row("Decision Maker", args.decision_maker)
    table.add_row("Position", args.position)
    table.add_row("Verbose Output", "✅" if args.verbose else "❌")
    table.add_row("Educational Mode", "✅" if args.educational else "❌")
    
    console.print(table)
    
    # Configure environment based on args
    if args.verbose and not args.educational:
        os.environ["CREWAI_VERBOSE"] = "true"
    elif args.educational:
        # Make sure CREWAI_VERBOSE is not set in educational mode
        if "CREWAI_VERBOSE" in os.environ:
            del os.environ["CREWAI_VERBOSE"]
    
    # Educational explanation of the architecture if enabled
    if args.educational:
        console.print("\n[bold yellow]Multi-Agent System Architecture:[/bold yellow]")
        architecture = """
        ┌────────────────────┐      ┌────────────────────┐      ┌────────────────────┐
        │                    │      │                    │      │                    │
        │  Sales Rep Agent   │──→───│ Lead Sales Rep     │──→───│ Quality Control    │
        │  [Research]        │      │ [Content Creation] │      │ [Evaluation]       │
        │                    │      │                    │      │                    │
        └────────────────────┘      └────────────────────┘      └────────────────────┘
                                            │                            │
                                            │                            │
                                            ▼                            │
                                    ┌────────────────────┐              │
                                    │                    │              │
                                    │ Lead Sales Rep     │◀─────────────┘
                                    │ [Refinement]       │
                                    │                    │
                                    └────────────────────┘
        """
        console.print(Syntax(architecture, "text", theme="monokai", background_color="default"))
        
        console.print("\n[bold yellow]Agent Roles & Specializations:[/bold yellow]")
        roles_table = Table(show_header=True, header_style="bold")
        roles_table.add_column("Agent", style="cyan")
        roles_table.add_column("Role", style="green")
        roles_table.add_column("Expertise", style="yellow")
        
        roles_table.add_row(
            "Sales Representative", 
            "Research & Analysis", 
            "Finding company information, analyzing needs, identifying opportunities"
        )
        roles_table.add_row(
            "Lead Sales Rep", 
            "Content Creation & Refinement", 
            "Crafting persuasive messages, personalizing outreach"
        )
        roles_table.add_row(
            "Quality Control", 
            "Evaluation & Feedback", 
            "Assessing effectiveness, suggesting improvements"
        )
        
        console.print(roles_table)
    
    # Setup inputs
    inputs = {
        "lead_name": args.company,
        "industry": args.industry,
        "key_decision_maker": args.decision_maker,
        "position": args.position
    }
    
    # Ask user to confirm before starting the demo
    console.print("\n[yellow]This demo will run multiple AI agents and may take several minutes to complete.[/yellow]")
    if input("\nPress Enter to start the demo or Ctrl+C to cancel..."):
        pass  # This just waits for the user to press Enter
    
    # Initialize crew
    crew = CustomerOutreach()
    
    # Create output directory for all files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"outputs_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Record start time
    start_time = time.time()
    
    console.print("\n[bold cyan]━━━━━━━━━━━━━━━━━━━ STARTING MULTI-AGENT WORKFLOW ━━━━━━━━━━━━━━━━━━━[/bold cyan]\n")
    
    # Run the crew
    result = crew.run(inputs)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Display completion summary with improved formatting
    console.print("\n[bold green]━━━━━━━━━━━━━━━━━━━ WORKFLOW RESULTS ━━━━━━━━━━━━━━━━━━━[/bold green]\n")
    
    console.print(Panel.fit(
        f"[bold green]Multi-Agent System Execution Complete[/bold green]\n\n"
        f"• [cyan]Total agents involved:[/cyan] 3\n"
        f"• [cyan]Execution time:[/cyan] {duration:.2f} seconds\n"
        f"• [cyan]Output files saved to:[/cyan] {output_dir}/\n\n"
        f"[dim]The final outreach message represents the collective intelligence\n"
        f"of multiple specialized agents working together.[/dim]",
        title="🎉 [bold]Workflow Results[/bold] 🎉",
        border_style="green"
    ))
    
    # Offer to view the final output file with better formatting
    if os.path.exists(f"{output_dir}/final_outreach.md"):
        console.print("\n[yellow]Would you like to view the final outreach message? (y/n)[/yellow]")
        if input().lower() == 'y':
            with open(f"{output_dir}/final_outreach.md", 'r') as f:
                content = f.read()
                console.print(Panel(
                    content, 
                    title="[bold]Final Outreach Message - Created by Multi-Agent System[/bold]", 
                    border_style="blue",
                    width=100
                ))
    
    if args.educational:
        console.print("\n[bold yellow]Key Learning Points:[/bold yellow]")
        learning_table = Table(show_header=False, box=None)
        learning_table.add_column("", style="cyan")
        
        learning_table.add_row("• Each agent has a specialized role and expertise")
        learning_table.add_row("• Agents exchange information through shared task outputs")
        learning_table.add_row("• The system follows a sequential workflow with feedback loops")
        learning_table.add_row("• Quality control provides an independent evaluation")
        learning_table.add_row("• The final output benefits from multiple perspectives and expertise")
        
        console.print(learning_table)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Demo cancelled by user.[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red]Error during demo execution: {str(e)}[/bold red]")