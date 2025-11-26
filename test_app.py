#!/usr/bin/env python3
"""
Unit tests for the app list CLI application.

This module contains test cases similar to JUnit tests for testing
the core functionality of the app.py application.
"""

import os
import tempfile
import unittest

import app


class TestappApp(unittest.TestCase):
    """Test cases for the app list application."""

    def setUp(self):
        """Set up a temporary file for each test."""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        )
        self.temp_file.close()
        self.original_app_file = app.app_FILE
        app.app_FILE = self.temp_file.name

    def tearDown(self):
        """Clean up the temporary file after each test."""
        app.app_FILE = self.original_app_file
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_add_task(self):
        """Test adding a new task to the list."""
        # Add a task
        task_id = app.add_task("Buy groceries")

        # Verify the task was added
        tasks = app.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], task_id)
        self.assertEqual(tasks[0]["description"], "Buy groceries")
        self.assertFalse(tasks[0]["completed"])

    def test_complete_task(self):
        """Test marking a task as complete."""
        # Add a task first
        task_id = app.add_task("Walk the dog")

        # Complete the task
        result = app.complete_task(task_id)

        # Verify the task was marked as complete
        self.assertTrue(result)
        tasks = app.load_tasks()
        self.assertTrue(tasks[0]["completed"])

    def test_delete_task(self):
        """Test deleting a task from the list."""
        # Add a task first
        task_id = app.add_task("Read a book")

        # Verify task was added
        tasks = app.load_tasks()
        self.assertEqual(len(tasks), 1)

        # Delete the task
        result = app.delete_task(task_id)

        # Verify the task was deleted
        self.assertTrue(result)
        tasks = app.load_tasks()
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()