Enough with the rigid pre-defined cluttered UIs. User and the LLM should play an active role in UI component design for the app. The purpose of this demo is to explore mechanisms allowed by the MCP protocol (MCP-app extensions)[https://modelcontextprotocol.io/extensions/apps/overview].

## Technology
Python (using uv) and FastMCP. Will need a rudimentary sql database for later scenarios (will use in-memory and local storage for the data to keep the app deployable with minimal infrastructure).
We sill use MCP versioning to keep tool surface constrained for each scenario.

# Scenario 1: UI direct tool calling.
This first scenario isn't really about truly dynamically generated UIs. It is "dynamic' in that it explores interactive tool calls from UI to the MCP server and htmx component updates to the UI. We will implement a book reader, with next and previous page functionality.

# Scenario 2: LLM passes template in the same tool call
Given a schema for the book reader published by the MCP tool, LLM can decide how to present the display to the user. We add ToC into the UI picture.

# Scenario 3: is it possible for the LLM to know about the state of the UI?
Just a small feature - when regenerating the layout, stay on the page the user was.

# Scenario 4: displaying dynamically generated queries
There is a schema given for the table, but LLM is supposed to write a query to retrieve it. Since the schema can be inferred from the query, the LLM passes a template. This is a building block for the final scenario.

# Scenario 5: Sampling from  the UI
Can UI make a sampling call to the client (LLM)? We will write a simple little tool to explore that possibility. Need that for everything to come together. 

# Scenario 6: Cached templates and sampling
This scenario puts everything together. Templates are optionally passed to tool calls. MCP server caches a template given the shape of the returned data. If a template is passed during the tool call, that template overrides the one inf the template cache (if it exists there). If template is not passed, and one is not in the template cache, a sampling call is made to query client (LLM) for the template. This is most likely to happen when user performs some action in the UI, so previous scenario results are important here.

# Scenario 7: Saved application state
Can we have some fun here with session memory? Persist app experience for the user. Add a memory tool. Set up a learning system with material to be covered, and recurring quizzes and tests. Memory used to keep track of progress and decide which material needs refreshing / reinforcing. UI used to administer quizzes and conduct lessons.
