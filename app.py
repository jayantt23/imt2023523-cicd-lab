#!/usr/bin/env python3
"""
A simple TODO list CLI application.

Usage:
    python todo.py add <task>       - Add a new task
    python todo.py list             - List all tasks
    python todo.py complete <id>    - Mark a task as complete
    python todo.py delete <id>      - Delete a task
    python todo.py clear            - Clear all tasks
"""

import argparse
import json
import os
import sys
from datetime import datetime


# Default file to store tasks
TODO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def add_task(description):
    """Add a new task to the list."""
    tasks = load_tasks()
    task_id = max([t["id"] for t in tasks], default=0) + 1
    task = {
        "id": task_id,
        "description": description,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: [{task_id}] {description}")
    return task_id


def list_tasks(show_all=True):
    """List all tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    print("\n📋 TODO List")
    print("-" * 40)

    for task in tasks:
        status = "✅" if task["completed"] else "⬜"
        task_id = task["id"]
        desc = task["description"]
        print(f"  {status} [{task_id}] {desc}")

    pending = sum(1 for t in tasks if not t["completed"])
    completed = sum(1 for t in tasks if t["completed"])
    print("-" * 40)
    print(f"Total: {len(tasks)} | Pending: {pending} | Completed: {completed}\n")


def complete_task(task_id):
    """Mark a task as complete."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print(f"Task [{task_id}] is already completed.")
            else:
                task["completed"] = True
                save_tasks(tasks)
                print(f"Task [{task_id}] marked as complete: {task['description']}")
            return True
    print(f"Task [{task_id}] not found.")
    return False


def delete_task(task_id):
    """Delete a task from the list."""
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            removed = tasks.pop(i)
            save_tasks(tasks)
            print(f"Task [{task_id}] deleted: {removed['description']}")
            return True
    print(f"Task [{task_id}] not found.")
    return False


def clear_tasks():
    """Clear all tasks."""
    save_tasks([])
    print("All tasks cleared.")


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="A simple TODO list CLI application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python todo.py add "Buy groceries"
  python todo.py list
  python todo.py complete 1
  python todo.py delete 1
  python todo.py clear
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task", help="Task description")

    # List command
    subparsers.add_parser("list", help="List all tasks")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("id", type=int, help="Task ID to mark as complete")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID to delete")

    # Clear command
    subparsers.add_parser("clear", help="Clear all tasks")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.task)
    elif args.command == "list":
        list_tasks()
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "clear":
        clear_tasks()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()