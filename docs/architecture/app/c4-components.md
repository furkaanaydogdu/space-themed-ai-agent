# App repo: C4 component view (level 3)

Part of the [main architecture document](../space-agent-architecture.md). Decisions are in [adr/](adr/).

## Inside the app container

```mermaid
flowchart TB
    visitor(["Visitor's browser<br/>(behind IAP)"])
    subgraph app["App service (one container, Cloud Run)"]
        subgraph fe["frontend/ (React + TypeScript, static files)"]
            ui["Conversation, landing, About"]
            overlay["Answer overlay + history entries"]
            illus["Illustrations<br/>pure layout functions"]
            store[("sessionStorage<br/>conversation, draft, open view")]
            client["API client<br/>generated types, expiry handling"]
        end
        subgraph be["backend/ (Python, FastAPI)"]
            api["API routes: ask, show-more, warm, health<br/>+ static file serving"]
            subgraph agent["Agent (LangGraph)"]
                decide["decide<br/>small model"]
                act["act<br/>parallel MCP calls"]
                compose["compose<br/>mid-tier model"]
                validate["validate<br/>levels 1-3"]
                finish["finish<br/>audit log line"]
            end
            mcpc["MCP client<br/>one connection per question"]
        end
    end
    mcp["MCP service<br/>(private)"]
    llm(["Model providers"])
    logs[("Platform logging")]

    visitor --> ui
    ui --> overlay
    overlay --> illus
    ui <--> store
    ui --> client
    client -- "/api, same origin" --> api
    api --> decide
    decide --> act
    act --> mcpc
    mcpc --> mcp
    act --> decide
    decide --> compose
    compose --> validate
    validate --> compose
    validate --> finish
    decide -. "model call" .-> llm
    compose -. "model call" .-> llm
    finish --> logs
```

## Notes
- The deadline is created in `api` when the request arrives and travels in the agent state ([ADR 0012](adr/0012-bounded-loops-deadline-and-cost-guards.md)).
- The backend returns facts and words; `illus` draws from raw data ([ADR 0009](adr/0009-react-and-python-api-in-one-container.md), [ADR 0011](adr/0011-one-api-contract-with-generated-types.md)).
- A decline with no tool calls goes from `decide` straight to `finish` (not drawn).
- The eval job (command line, not part of the service) runs the same agent code with fake or real tools ([ADR 0005](adr/0005-evals-on-demand-with-an-independent-judge.md)).
