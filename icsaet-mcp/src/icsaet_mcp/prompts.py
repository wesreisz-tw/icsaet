"""MCP prompts for authentication and query workflows."""

from .server import mcp


def _get_icaet_overview() -> str:
    """Get the ICAET overview content."""
    return """# ICAET Overview

**What is ICAET?**

ICAET is a knowledge base containing content from the International Conference on Agile and Extreme Programming Topics. It provides searchable access to conference talks, presentations, and discussions from industry experts and practitioners.

**What information does it contain?**

ICAET contains:
- Speaker presentations and talks
- Topics covering agile methodologies, extreme programming, and software development practices
- Insights from industry leaders and practitioners
- Detailed information about specific topics, stories, and examples shared during presentations

**Who would use this?**

Developers, team leads, and software practitioners who want to:
- Learn from conference content
- Reference specific talks or topics
- Explore agile and XP best practices
- Find answers to software development questions based on real-world experiences

**How do I ask questions?**

Simply use the `query` tool with your question in natural language. The system will search the ICAET knowledge base and return relevant information. For best results, see the question formatting guidance prompt.
"""


@mcp.prompt()
def icaet_overview() -> str:
    """Provide an overview of ICAET and how to use it."""
    return _get_icaet_overview()


def _get_example_questions() -> str:
    """Get example questions content."""
    return """# Example Questions for ICAET

Here are example questions demonstrating different query types and specificity levels:

**Broad Topic Queries:**
1. "What did Leslie Miley talk about?"
2. "What topics were covered related to agile methodologies?"
3. "What are the main themes discussed at ICAET?"

**Specific Detail Queries:**
4. "What specific stories did Leslie Miley share during his presentation?"
5. "What recommendations were made about pair programming?"
6. "What metrics were discussed for measuring team velocity?"

**Multi-Part Queries:**
7. "What did speakers say about code review practices and their impact on quality?"
8. "How do different speakers approach technical debt and what strategies do they recommend?"

**Comparison Queries:**
9. "What are the different perspectives on test-driven development presented at the conference?"
10. "How do various speakers compare Scrum and Kanban methodologies?"

**Tip:** Start broad to explore topics, then ask more specific follow-up questions based on the results.
"""


@mcp.prompt()
def example_questions() -> str:
    """Provide example questions demonstrating ICAET capabilities."""
    return _get_example_questions()


def _get_question_formatting() -> str:
    """Get question formatting guidance content."""
    return """# Question Formatting Best Practices

**For Better Results:**

✓ **Be specific** - Include names, topics, or concepts when you know them
  - Good: "What did Leslie Miley say about engineering culture?"
  - Poor: "What was said about culture?"

✓ **Use complete sentences** - Frame questions clearly and naturally
  - Good: "What recommendations were made for improving code quality?"
  - Poor: "code quality tips"

✓ **Ask one thing at a time** - Focus each question on a single topic for clarity
  - Good: "What are the benefits of pair programming?"
  - Less effective: "What are the benefits and drawbacks and costs and ROI of pair programming?"

✓ **Reference specific topics or speakers** - When you know what you're looking for
  - Good: "What testing strategies were discussed?"
  - Better: "What testing strategies did the speakers recommend for microservices?"

**What to Avoid:**

✗ Overly vague questions without context
✗ Multiple unrelated questions in one query
✗ Keyword searches without question structure
✗ Assuming content that may not exist in the knowledge base

**Specificity Guidelines:**

- **Too broad:** "Tell me everything about agile"
- **Well-scoped:** "What agile practices were recommended for distributed teams?"
- **Very specific:** "What did Leslie Miley say about incident response processes?"

All specificity levels work, but more specific questions typically yield more focused and actionable results.
"""


@mcp.prompt()
def question_formatting() -> str:
    """Provide guidance on formatting questions for best results."""
    return _get_question_formatting()

