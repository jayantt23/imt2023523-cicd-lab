#!/usr/bin/env python3
"""
Unit tests for the TODO list CLI application.

This module contains test cases similar to JUnit tests for testing
the core functionality of the todo.py application.
"""

import os
import tempfile
import unittest

import todo


class TestTodoApp(unittest.TestCase):
    """Test cases for the TODO list application."""

    def setUp(self):
        """Set up a temporary file for each test."""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        )
        self.temp_file.close()
        self.original_todo_file = todo.TODO_FILE
        todo.TODO_FILE = self.temp_file.name

    def tearDown(self):
        """Clean up the temporary file after each test."""
        todo.TODO_FILE = self.original_todo_file
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_add_task(self):
        """Test adding a new task to the list."""
        # Add a task
        task_id = todo.add_task("Buy groceries")

        # Verify the task was added
        tasks = todo.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], task_id)
        self.assertEqual(tasks[0]["description"], "Buy groceries")
        self.assertFalse(tasks[0]["completed"])

    def test_complete_task(self):
        """Test marking a task as complete."""
        # Add a task first
        task_id = todo.add_task("Walk the dog")

        # Complete the task
        result = todo.complete_task(task_id)

        # Verify the task was marked as complete
        self.assertTrue(result)
        tasks = todo.load_tasks()
        self.assertTrue(tasks[0]["completed"])

    def test_delete_task(self):
        """Test deleting a task from the list."""
        # Add a task first
        task_id = todo.add_task("Read a book")

        # Verify task was added
        tasks = todo.load_tasks()
        self.assertEqual(len(tasks), 1)

        # Delete the task
        result = todo.delete_task(task_id)

        # Verify the task was deleted
        self.assertTrue(result)
        tasks = todo.load_tasks()
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()