# Project Instructions

The goal of this project is to learn and experiment. Remember to take small steps, and set it up so that the user can run things and learn. 

Specific items we are working on are in the README.md. 


## Technology

We will use python, and build everything with uv. Remember that every python command or script is to be run via uv.

For MCP implementation we will use FastMCP. Make extensive use of FastMCP's online documentation, because your training is most likely out of date. Verify patterns and functinality in the documentation. Starting point is: https://gofastmcp.com/llms.txt but you can add additional references as we use specific features in the project. 

For frontend, use FastHtml, with context (note, it is fairly large, we will activate it in a skill in the future): https://www.fastht.ml/docs/llms-ctx.txt 

## How to fulfil user's instructions

Unless it is a single line shell command, you should not emote inline code directly into the shell, even if just to experiment or debug a problem. Instead, try to solve a problem in python and write it as a reusable code. Execute script with uv. Even for a simple example, it is better if you start with barebones and iterate on it in a code - run - check output cycle. You may use "code-scratchpad" directory for such scripts. Name them code-scratchpad/001_<function>.py consecutively, so we can easily pick up the latest work. 

When fulfilling user's request, you should first check to make sure you have latest patterns and documentation in your context. We are working on leading edge technologies here and the documentation changes daily sometimes.

Think through the stated problem and present options to the user (you can emit example code in the chat window), before implementing anything. As you start to implement, take really small steps, and pause to let the user learn and verify what is going on.