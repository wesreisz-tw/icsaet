# Task 05 Implementation Plan: MCP Prompts Implementation

## 1. Issue

The prompts.py file currently contains only a stub (just `pass` statement). Need to implement three MCP prompt templates that provide users with guidance on ICAET usage, example questions, and formatting tips to improve their query experience in Cursor IDE.

## 2. Solution

Implement three prompt functions in prompts.py using the fastmcp `@mcp.prompt()` decorator pattern (analogous to `@mcp.tool()` pattern used in tools.py). Each prompt will:
- Be decorated with `@mcp.prompt()` 
- Return a static string containing markdown-formatted guidance
- Be imported in __main__.py to ensure registration with the MCP server
- Provide clear, concise, and actionable content for Cursor IDE users

## 3. Implementation Steps

1. **Update /Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src/icsaet_mcp/prompts.py**:
   - Remove the `pass` statement
   - Import `mcp` from `.server`
   - Create function `icaet_overview()` decorated with `@mcp.prompt()`
     - Return string explaining what ICAET is
     - Include: knowledge base description, content types, usage instructions
     - Format as markdown for readability
   - Create function `example_questions()` decorated with `@mcp.prompt()`
     - Return string with at least 5 example questions
     - Include: broad queries, specific queries, multi-part queries
     - Examples: "What did Leslie Miley talk about?", topic queries, detail queries
     - Format as numbered or bulleted list
   - Create function `question_formatting()` decorated with `@mcp.prompt()`
     - Return string with formatting best practices
     - Include: specificity tips, structure guidance, what to avoid
     - Format as bulleted tips for easy scanning

2. **Update /Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src/icsaet_mcp/__main__.py**:
   - Add import statement: `from . import prompts`
   - This ensures prompts are registered when server starts
   - Import should be after server import, before mcp.run()

3. **Verify prompt content**:
   - ICAET overview prompt includes all required elements from task-05.md lines 24-28
   - Example questions prompt includes at least 5 examples from task-05.md lines 30-34
   - Question formatting prompt includes tips from task-05.md lines 36-40
   - No placeholder text (Lorem Ipsum, STUB, TODO)
   - Professional tone throughout
   - Concise enough for IDE display

## 4. Verification

**Required for completion:**
- [ ] prompts.py contains three prompt functions with @mcp.prompt() decorator
- [ ] Each prompt function returns a non-empty string
- [ ] ICAET overview prompt answers: What is ICAET? What information? How to use?
- [ ] Example questions prompt has at least 5 realistic examples
- [ ] Question formatting prompt has best practices and tips
- [ ] prompts module imported in __main__.py
- [ ] No stub/placeholder content remains
- [ ] All content uses professional tone
- [ ] Content is accurate about ICAET (knowledge base, query capabilities)

**Testing approach:**
- Verify prompts are discoverable via MCP protocol (Task 06 will add comprehensive tests)
- Visual inspection of prompt content for clarity and completeness
- Ensure markdown formatting renders properly in IDE

## IMPLEMENTATION CHECKLIST

1. Edit /Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src/icsaet_mcp/prompts.py - import mcp from server
2. Edit /Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src/icsaet_mcp/prompts.py - create icaet_overview() function with @mcp.prompt() decorator
3. Edit /Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src/icsaet_mcp/prompts.py - create example_questions() function with @mcp.prompt() decorator
4. Edit /Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src/icsaet_mcp/prompts.py - create question_formatting() function with @mcp.prompt() decorator
5. Edit /Users/wesleyreisz/work/mcp/icsaet/icsaet-mcp/src/icsaet_mcp/__main__.py - add import for prompts module
6. Review all prompt content for completeness, accuracy, and professional tone

