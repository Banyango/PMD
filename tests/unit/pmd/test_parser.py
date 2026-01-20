from pmd.parser import (
    PMDParser,
    ForNode,
    IfNode,
    IncludeNode,
    TextNode,
    VariableNode,
)


class TestPmdParser:
    """Test suite for PmdParser."""

    def setup_method(self):
        """Set up a fresh parser for each test."""
        self.parser = PMDParser()

    def test_parse_simple_text(self):
        """Test parsing plain text without any special tokens."""
        template = "Hello, world!"
        metadata, nodes = self.parser.parse(template)

        assert metadata == {}
        assert len(nodes) == 1
        assert isinstance(nodes[0], TextNode)
        assert nodes[0].content == "Hello, world!"

    def test_parse_metadata(self):
        """Test parsing metadata directives."""
        template = """@task: summarization
@owner: search-team
@version: 1.0

Content here"""
        metadata, nodes = self.parser.parse(template)

        assert metadata == {"task": "summarization", "owner": "search-team", "version": "1.0"}
        assert len(nodes) == 1
        assert isinstance(nodes[0], TextNode)

    def test_parse_variable(self):
        """Test parsing variable placeholders."""
        template = "Hello, {{name}}!"
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 3
        assert isinstance(nodes[0], TextNode)
        assert nodes[0].content == "Hello, "
        assert isinstance(nodes[1], VariableNode)
        assert nodes[1].name == "name"
        assert isinstance(nodes[2], TextNode)
        assert nodes[2].content == "!"

    def test_parse_multiple_variables(self):
        """Test parsing multiple variables."""
        template = "{{greeting}}, {{name}}! Your age is {{age}}."
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 6
        assert isinstance(nodes[0], VariableNode)
        assert nodes[0].name == "greeting"
        assert isinstance(nodes[2], VariableNode)
        assert nodes[2].name == "name"
        assert isinstance(nodes[4], VariableNode)
        assert nodes[4].name == "age"

    def test_parse_if_statement(self):
        """Test parsing if conditionals."""
        template = """{% if show_greeting %}
Hello!
{% endif %}"""
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], IfNode)
        assert nodes[0].condition == "show_greeting"
        assert len(nodes[0].true_block) == 1
        assert isinstance(nodes[0].true_block[0], TextNode)
        assert nodes[0].false_block is None

    def test_parse_if_else_statement(self):
        """Test parsing if-else conditionals."""
        template = """{% if logged_in %}
Welcome back!
{% else %}
Please log in.
{% endif %}"""
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], IfNode)
        assert nodes[0].condition == "logged_in"
        assert len(nodes[0].true_block) == 1
        assert "Welcome back!" in nodes[0].true_block[0].content
        assert nodes[0].false_block is not None
        assert len(nodes[0].false_block) == 1
        assert "Please log in." in nodes[0].false_block[0].content

    def test_parse_if_with_variable(self):
        """Test parsing if statement containing variables."""
        template = """{% if show_name %}
Your name is {{name}}.
{% endif %}"""
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], IfNode)
        assert len(nodes[0].true_block) == 3
        assert isinstance(nodes[0].true_block[1], VariableNode)
        assert nodes[0].true_block[1].name == "name"

    def test_parse_for_loop(self):
        """Test parsing for loops."""
        template = """{% for item in items %}
- {{item}}
{% endfor %}"""
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], ForNode)
        assert nodes[0].iterator == "item"
        assert nodes[0].iterable == "items"
        assert len(nodes[0].block) == 3

    def test_parse_nested_for_loop(self):
        """Test parsing nested for loops."""
        template = """{% for category in categories %}
Category: {{category}}
{% for item in items %}
  - {{item}}
{% endfor %}
{% endfor %}"""
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], ForNode)
        assert nodes[0].iterator == "category"
        inner_nodes = nodes[0].block
        # Find the nested for loop
        nested_for = None
        for node in inner_nodes:
            if isinstance(node, ForNode):
                nested_for = node
                break
        assert nested_for is not None
        assert nested_for.iterator == "item"

    def test_parse_if_with_for_loop(self):
        """Test parsing if statement containing a for loop."""
        template = """{% if has_items %}
Items:
{% for item in items %}
- {{item}}
{% endfor %}
{% endif %}"""
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], IfNode)
        # Find the for loop in the true block
        for_node = None
        for node in nodes[0].true_block:
            if isinstance(node, ForNode):
                for_node = node
                break
        assert for_node is not None
        assert for_node.iterator == "item"

    def test_parse_include(self):
        """Test parsing include directives."""
        template = '{% include "header.pmd" %}'
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], IncludeNode)
        assert nodes[0].template_name == "header.pmd"

    def test_parse_comment(self):
        """Test that comments are ignored."""
        template = """Text before
{# This is a comment #}
Text after"""
        metadata, nodes = self.parser.parse(template)

        # Comments should be completely removed
        assert len(nodes) == 1
        assert isinstance(nodes[0], TextNode)
        assert "comment" not in nodes[0].content.lower()

    def test_parse_multiline_comment(self):
        """Test parsing multiline comments."""
        template = """{# This is a
multiline
comment #}
Content"""
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], TextNode)
        assert "Content" in nodes[0].content

    def test_parse_complex_template(self):
        """Test parsing a complex template with multiple features."""
        template = """@task: summarization
@owner: search-team

# Instruction
You are a helpful assistant.

# Document
Summarize the following document for {{audience}}:

{{doc}}

{% if rules %}
# Rules
{% for rule in rules %}
- {{rule}}
{% endfor %}
{% endif %}"""
        metadata, nodes = self.parser.parse(template)

        assert metadata == {"task": "summarization", "owner": "search-team"}

        # Should have text, variables, if, and for nodes
        has_variable = any(isinstance(node, VariableNode) for node in nodes)
        has_if = any(isinstance(node, IfNode) for node in nodes)
        assert has_variable
        assert has_if

    def test_parse_empty_template(self):
        """Test parsing an empty template."""
        template = ""
        metadata, nodes = self.parser.parse(template)

        assert metadata == {}
        assert len(nodes) == 0

    def test_parse_whitespace_only(self):
        """Test parsing whitespace-only template."""
        template = "   \n  \n  "
        metadata, nodes = self.parser.parse(template)

        assert metadata == {}
        assert len(nodes) == 1
        assert isinstance(nodes[0], TextNode)

    def test_parse_consecutive_variables(self):
        """Test parsing consecutive variables without text between them."""
        template = "{{first}}{{second}}{{third}}"
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 3
        assert all(isinstance(node, VariableNode) for node in nodes)
        assert nodes[0].name == "first"
        assert nodes[1].name == "second"
        assert nodes[2].name == "third"

    def test_parse_variable_in_text(self):
        """Test parsing variables embedded in text."""
        template = "The value is {{value}} and that's final."
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 3
        assert nodes[0].content == "The value is "
        assert nodes[1].name == "value"
        assert nodes[2].content == " and that's final."

    def test_parse_nested_if_statements(self):
        """Test parsing nested if statements."""
        template = """{% if outer %}
Outer true
{% if inner %}
Inner true
{% endif %}
{% endif %}"""
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], IfNode)
        assert nodes[0].condition == "outer"

        # Find nested if in true block
        nested_if = None
        for node in nodes[0].true_block:
            if isinstance(node, IfNode):
                nested_if = node
                break
        assert nested_if is not None
        assert nested_if.condition == "inner"

    def test_parse_for_with_complex_content(self):
        """Test parsing for loop with complex content."""
        template = """{% for user in users %}
Name: {{user}}
{% if active %}
Status: Active
{% endif %}
{% endfor %}"""
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], ForNode)

        # Should have text, variable, and if nodes in the loop body
        has_variable = any(isinstance(node, VariableNode) for node in nodes[0].block)
        has_if = any(isinstance(node, IfNode) for node in nodes[0].block)
        assert has_variable
        assert has_if

    def test_parse_metadata_with_special_chars(self):
        """Test parsing metadata with special characters."""
        template = """@description: This is a test with: colons and - dashes
@email: user@example.com

Content"""
        metadata, nodes = self.parser.parse(template)

        assert "description" in metadata
        assert ":" in metadata["description"]
        assert metadata["email"] == "user@example.com"

    def test_parse_multiple_includes(self):
        """Test parsing multiple include statements."""
        template = """{% include "header.pmd" %}
Content here
{% include "footer.pmd" %}"""
        metadata, nodes = self.parser.parse(template)

        include_nodes = [node for node in nodes if isinstance(node, IncludeNode)]
        assert len(include_nodes) == 2
        assert include_nodes[0].template_name == "header.pmd"
        assert include_nodes[1].template_name == "footer.pmd"

    def test_parser_state_reset(self):
        """Test that parser state is reset between parses."""
        template1 = "@key: value1\nText1"
        template2 = "@key: value2\nText2"

        metadata1, nodes1 = self.parser.parse(template1)
        metadata2, nodes2 = self.parser.parse(template2)

        assert metadata1 == {"key": "value1"}
        assert metadata2 == {"key": "value2"}
        assert "Text1" in nodes1[0].content
        assert "Text2" in nodes2[0].content

    def test_parse_variable_underscore(self):
        """Test parsing variables with underscores."""
        template = "{{my_variable_name}}"
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], VariableNode)
        assert nodes[0].name == "my_variable_name"

    def test_parse_for_with_underscore(self):
        """Test parsing for loop with underscored variable names."""
        template = "{% for list_item in my_list %}{{list_item}}{% endfor %}"
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], ForNode)
        assert nodes[0].iterator == "list_item"
        assert nodes[0].iterable == "my_list"


class TestPmdParserEdgeCases:
    """Test edge cases and error conditions."""

    def setup_method(self):
        """Set up a fresh parser for each test."""
        self.parser = PMDParser()

    def test_unclosed_if(self):
        """Test parsing template with unclosed if statement."""
        template = "{% if condition %}Text"
        # Should still parse, just won't have proper closing
        metadata, nodes = self.parser.parse(template)
        assert len(nodes) == 1
        assert isinstance(nodes[0], IfNode)

    def test_unclosed_for(self):
        """Test parsing template with unclosed for loop."""
        template = "{% for item in items %}Text"
        metadata, nodes = self.parser.parse(template)
        assert len(nodes) == 1
        assert isinstance(nodes[0], ForNode)

    def test_else_without_if(self):
        """Test else without preceding if (should be ignored)."""
        template = "{% else %}Text{% endif %}"
        metadata, nodes = self.parser.parse(template)
        # Parser should handle this gracefully

    def test_special_characters_in_text(self):
        """Test that special characters in text are preserved."""
        template = "Special chars: !@#$%^&*()[]{}|\\<>?,./;':\"~`"
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 1
        assert isinstance(nodes[0], TextNode)
        # Most special chars should be preserved (except those used in patterns)

    def test_unicode_content(self):
        """Test parsing Unicode content."""
        template = "Hello 世界! {{name}} 🌍"
        metadata, nodes = self.parser.parse(template)

        assert len(nodes) == 3
        assert "世界" in nodes[0].content
        assert isinstance(nodes[1], VariableNode)
        assert "🌍" in nodes[2].content
