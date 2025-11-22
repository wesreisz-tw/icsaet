# Task 05: MCP Prompts Implementation

## Story Reference
- **Parent Story:** SCRUM-5 - Cursor MCP Server for ICAET Query Access
- **Task Sequence:** 5 of 8

## Task Objective
Implement MCP prompts that provide users with guidance on ICAET usage, example questions, and formatting tips to improve their query experience in Cursor IDE.

## Scope
- Implement prompt templates in prompts.py
- Register prompts with MCP server
- Create ICAET overview prompt
- Create example questions prompt
- Create question formatting guidance prompt
- Make prompts discoverable in Cursor IDE

## Acceptance Criteria
1. prompts.py implements three prompt templates:
   - **icaet_overview**: Explains what ICAET is and how to use it
   - **example_questions**: Provides example questions demonstrating capabilities
   - **question_formatting**: Offers guidance on formatting questions for best results

2. ICAET overview prompt includes:
   - What ICAET is (knowledge base for ICAET content)
   - What type of information it contains
   - How to ask questions
   - Basic usage instructions

3. Example questions prompt includes:
   - At least 5 example questions
   - Examples demonstrate different query types
   - Examples are realistic and helpful
   - Examples show specificity levels (broad to specific)

4. Question formatting guidance includes:
   - Best practices for question structure
   - Tips for getting better results
   - What to avoid
   - Specificity guidelines

5. Prompts registered with MCP server:
   - All prompts discoverable via MCP protocol
   - Prompts accessible from Cursor IDE
   - Prompts formatted for readability

6. Prompt content quality:
   - Clear and concise language
   - Helpful for first-time users
   - Accurate information about ICAET
   - Professional tone

## Dependencies
- **Task 02:** Working MCP server with prompt registration capability
- **Task 04:** Logging system (to log prompt access if needed)

## Required Inputs
- Functional server.py with MCP server instance from Task 02
- SCRUM-5 specification sections on prompts (currently marked as STUBs)
- Understanding of ICAET's capabilities and content

## Expected Outputs and Handoff Criteria

### Outputs
1. Implemented prompts.py with three prompt templates
2. Prompts registered with MCP server
3. All prompts accessible from Cursor IDE
4. Clear, helpful prompt content

### Handoff Criteria
- All three prompts implemented and registered
- Prompts display correctly in Cursor IDE
- Prompt content is clear and helpful
- No Lorem Ipsum or placeholder content
- Prompts follow MCP protocol format
- Users can discover and read prompts from Cursor

### Handoff to Task 06
- Task 06 will implement mock server and testing infrastructure
- Task 06 requires: complete working server with tools and prompts to test against

## Task-Specific Constraints
1. Prompts must follow MCP protocol format
2. Keep prompts concise (users will read in IDE)
3. No external dependencies for prompts
4. Prompts should be static (no dynamic content)
5. Professional, helpful tone
6. Accurate information only (no speculation)

## Prompt Content Guidelines

### ICAET Overview Prompt
Should answer:
- What is ICAET?
- What kind of information does it contain?
- Who would use this?
- How do I ask questions?

### Example Questions Prompt
Should include questions like:
- "What did Leslie Miley talk about?"
- Broad topic queries
- Specific detail queries
- Multi-part queries
- Comparison queries

### Question Formatting Guidance
Should include tips like:
- Be specific in your questions
- Use complete sentences
- Ask one thing at a time for clarity
- Reference specific topics or speakers when known
- What makes a good vs poor question

## Implementation Notes
- Use fastmcp prompt decorator/registration
- Keep prompt text in prompts.py (not external files)
- Format prompts for terminal/IDE display
- Consider markdown formatting if supported
- Test prompts in actual Cursor IDE if possible

## Validation Checklist
- [ ] prompts.py created with three prompts
- [ ] ICAET overview prompt implemented
- [ ] Example questions prompt implemented
- [ ] Question formatting prompt implemented
- [ ] All prompts registered with server
- [ ] Prompts discoverable in Cursor
- [ ] Prompt content clear and helpful
- [ ] No placeholder/stub content
- [ ] Professional tone throughout
