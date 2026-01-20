"""Integration tests that run .pmd files through the parser and renderer.

This module tests the complete pipeline: parsing .pmd template files,
render them with test data, and verifying the output matches expected results.
"""

import pathlib

import pytest

from pmd.parser import PMDParser
from pmd.render.renderer import PMDRenderer


class TestPmdIntegration:
    """Integration tests for parsing and render .pmd templates."""

    @pytest.fixture
    def parser(self):
        """Create a fresh parser instance."""
        return PMDParser()

    @pytest.fixture
    def files_dir(self):
        """Get the files directory path."""
        return pathlib.Path(__file__).parent / "files"

    def test_simple_template(self, parser, files_dir):
        """Test simple.pmd with basic variable substitution."""
        template_file = files_dir / "simple.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Render with context
        renderer = PMDRenderer(context={"name": "Alice"})
        result = renderer.render(nodes)

        # Expected output
        expected = "Hello, Alice!\nWelcome to Pmd templating.\n\n"

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_metadata_template(self, parser, files_dir):
        """Test metadata.pmd with metadata and variable substitution."""
        template_file = files_dir / "metadata.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Verify metadata
        assert metadata["task"] == "summarization"
        assert metadata["owner"] == "search-team"
        assert metadata["version"] == "2.0"

        # Render with context
        renderer = PMDRenderer(context={"document": "This is a sample document to summarize."})
        result = renderer.render(nodes)

        # Expected output
        expected = (
            "\n"
            "# Instruction\n"
            "You are a helpful assistant specialized in summarization.\n\n"
            "# Input\n"
            "This is a sample document to summarize.\n"
            "\n"
        )

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_conditional_template_authenticated(self, parser, files_dir):
        """Test conditional.pmd with authenticated user (true branch)."""
        template_file = files_dir / "conditional.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Render with authenticated context
        renderer = PMDRenderer(
            context={"is_authenticated": True, "username": "Bob", "status": "Premium"}
        )
        result = renderer.render(nodes)

        # Expected output
        expected = (
            "\n"
            "# Greeting\n\n"
            "Welcome back, Bob!\n\n"
            "Your account status: Premium\n"
            "\n"
            "# Footer\n"
            "Thank you for using our service.\n"
            "\n"
        )

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_conditional_template_unauthenticated(self, parser, files_dir):
        """Test conditional.pmd with unauthenticated user (false branch)."""
        template_file = files_dir / "conditional.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Render with unauthenticated context
        renderer = PMDRenderer(context={"is_authenticated": False})
        result = renderer.render(nodes)

        # Expected output
        expected = (
            "\n"
            "# Greeting\n\n"
            "Please sign in to continue.\n"
            "\n# Footer\n"
            "Thank you for using our service.\n"
            "\n"
        )

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_loop_template(self, parser, files_dir):
        """Test loop.pmd with for loop iteration."""
        template_file = files_dir / "loop.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Render with items
        renderer = PMDRenderer(context={"items": ["Apple", "Banana", "Cherry"]})
        result = renderer.render(nodes)

        # Expected output
        expected = (
            "\n"
            "# Items List\n\n"
            "- Item: Apple\n"
            "- Item: Banana\n"
            "- Item: Cherry\n"
            "\n# Summary\n"
            "Total items listed above.\n"
            "\n"
        )

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_loop_template_empty(self, parser, files_dir):
        """Test loop.pmd with empty items list."""
        template_file = files_dir / "loop.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Render with empty items
        renderer = PMDRenderer(context={"items": []})
        result = renderer.render(nodes)

        # Expected output (loop body should not appear)
        expected = "\n# Items List\n\n\n# Summary\nTotal items listed above.\n\n"

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_complex_template_with_context(self, parser, files_dir):
        """Test complex.pmd with nested if/for statements."""
        template_file = files_dir / "complex.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Verify metadata
        assert metadata["task"] == "complex-template"
        assert metadata["owner"] == "ai-team"

        # Render with context (has_context=True, format_json=False)
        renderer = PMDRenderer(
            context={
                "task_type": "question answering",
                "has_context": True,
                "documents": ["Doc1", "Doc2"],
                "query": "What is the capital of France?",
                "format_json": False,
            }
        )
        result = renderer.render(nodes)

        # Expected output
        expected = (
            "\n"
            "# System Prompt\n"
            "You are an AI assistant helping with question answering.\n\n"
            "# Instructions\n"
            "Use the following context to answer:\n\n"
            "Document Doc1:\n"
            "- Title: Doc1\n"
            "- Content: Available\n"
            "Document Doc2:\n"
            "- Title: Doc2\n"
            "- Content: Available\n"
            "\n"
            "# User Query\n"
            "What is the capital of France?\n\n"
            "# Output Format\n"
            "Provide your response in plain text.\n"
            "\n\n"
            "# Additional Notes\n"
            "- Be concise\n"
            "- Be accurate\n"
            "- Be helpful\n"
            "\n"
        )

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_complex_template_no_context(self, parser, files_dir):
        """Test complex.pmd with has_context=False."""
        template_file = files_dir / "complex.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Render with context (has_context=False, format_json=True)
        renderer = PMDRenderer(
            context={
                "task_type": "general inquiry",
                "has_context": False,
                "query": "Tell me about AI",
                "format_json": True,
            }
        )
        result = renderer.render(nodes)

        # Expected output
        expected = (
            "\n"
            "# System Prompt\n"
            "You are an AI assistant helping with general inquiry.\n\n"
            "# Instructions\n"
            "Answer based on your general knowledge.\n"
            "\n"
            "# User Query\n"
            "Tell me about AI\n\n"
            "# Output Format\n"
            "Provide your response in JSON format.\n"
            "\n"
            "\n"
            "# Additional Notes\n"
            "- Be concise\n"
            "- Be accurate\n"
            "- Be helpful\n"
            "\n"
        )

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_nested_template(self, parser, files_dir):
        """Test nested.pmd with deeply nested structures."""
        template_file = files_dir / "nested.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Render with show_categories=True, show_items=True
        renderer = PMDRenderer(
            context={
                "show_categories": True,
                "categories": ["Electronics", "Books"],
                "show_items": True,
                "items": ["Item1", "Item2"],
            }
        )
        result = renderer.render(nodes)

        # Expected output
        expected = (
            "\n"
            "# Nested Conditionals and Loops\n\n"
            "# Categories\n\n"
            "## Category: Electronics\n\n"
            "Items in this category:\n"
            "  - Item1\n"
            "  - Item2\n"
            "\n"
            "## Category: Books\n\n"
            "Items in this category:\n"
            "  - Item1\n"
            "  - Item2\n"
            "\n"
            "\n# End\n"
            "\n"
        )

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_nested_template_no_items(self, parser, files_dir):
        """Test nested.pmd with show_items=False."""
        template_file = files_dir / "nested.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Render with show_categories=True, show_items=False
        renderer = PMDRenderer(
            context={"show_categories": True, "categories": ["Electronics"], "show_items": False}
        )
        result = renderer.render(nodes)

        # Expected output
        expected = (
            "\n"
            "# Nested Conditionals and Loops\n\n"
            "# Categories\n\n"
            "## Category: Electronics\n\n"
            "No items to display.\n"
            "\n"
            "\n# End\n"
            "\n"
        )

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_include_template(self, parser, files_dir):
        """Test include.pmd with include directives."""
        template_file = files_dir / "include.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Render
        renderer = PMDRenderer(context={"content": "This is the main content section."})
        result = renderer.render(nodes)

        # Expected output (includes are rendered as placeholders)
        expected = (
            "\n"
            "[INCLUDE: header.pmd]\n"
            "# Main Content\n"
            "This is the main content section.\n\n"
            "[INCLUDE: footer.pmd]\n"
        )

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_unicode_template_happy(self, parser, files_dir):
        """Test unicode.pmd with unicode characters and emojis (happy=True)."""
        template_file = files_dir / "unicode.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Verify metadata
        assert metadata["task"] == "multilingual"
        assert metadata["language"] == "mixed"

        # Render with happy=True
        renderer = PMDRenderer(context={"name": "World", "happy": True})
        result = renderer.render(nodes)

        # Expected output
        expected = (
            "\n"
            "# Multilingual Template\n\n"
            "Hello, World! 👋\n"
            "Bonjour, World! 🇫🇷\n"
            "こんにちは, World! 🇯🇵\n"
            "你好, World! 🇨🇳\n"
            "Привет, World! 🇷🇺\n\n"
            "# Emoji Support\n"
            "😊 You seem happy!\n"
            "\n"
        )

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_unicode_template_not_happy(self, parser, files_dir):
        """Test unicode.pmd with unicode characters and emojis (happy=False)."""
        template_file = files_dir / "unicode.pmd"
        with open(template_file, encoding="utf-8") as f:
            content = f.read()

        # Parse
        metadata, nodes = parser.parse(content)

        # Render with happy=False
        renderer = PMDRenderer(context={"name": "世界", "happy": False})
        result = renderer.render(nodes)

        # Expected output
        expected = (
            "\n"
            "# Multilingual Template\n\n"
            "Hello, 世界! 👋\n"
            "Bonjour, 世界! 🇫🇷\n"
            "こんにちは, 世界! 🇯🇵\n"
            "你好, 世界! 🇨🇳\n"
            "Привет, 世界! 🇷🇺\n\n"
            "# Emoji Support\n"
            "😐 Hope you're doing well!\n"
            "\n"
        )

        assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

    def test_all_templates_parse_without_error(self, parser, files_dir):
        """Smoke test: ensure all .pmd files can be parsed without errors."""
        pmd_files = sorted(files_dir.glob("*.pmd"))

        assert len(pmd_files) > 0, "No .pmd files found"

        results = {}
        for template_file in pmd_files:
            with open(template_file, encoding="utf-8") as f:
                content = f.read()

            # Parse should not raise an exception
            metadata, nodes = parser.parse(content)
            results[template_file.name] = {
                "metadata_count": len(metadata),
                "node_count": len(nodes),
            }

        # Print summary
        print("\n" + "=" * 60)
        print("All templates parsed successfully:")
        print("=" * 60)
        for filename, info in results.items():
            print(
                f"{filename:20} -> {info['node_count']:2} nodes, {info['metadata_count']:2} metadata"
            )

        # Verify we tested all expected files
        assert "simple.pmd" in results
        assert "metadata.pmd" in results
        assert "conditional.pmd" in results
        assert "loop.pmd" in results
        assert "complex.pmd" in results
        assert "nested.pmd" in results
        assert "include.pmd" in results
        assert "unicode.pmd" in results
