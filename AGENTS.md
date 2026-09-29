# Agents Framework Interoperability

This agent is built as a portable, framework-agnostic component conforming to the OpenGAP specification.

## Purpose
To provide reliable, deterministic document processing and intelligence without being tied to a specific execution environment.

## Core Behavior
The agent receives a structured request specifying a tool and input parameters. The internal `AgentCore` dynamically routes the request to the appropriate tool in the `DynamicToolRegistry`, executes it, and returns a structured result.

## Tool Usage
Tools are defined as independent YAML contracts alongside Python implementations. A compatible runtime can read the YAML definitions to understand the agent's capabilities and schema requirements before invoking it.

## Limitations
The agent does not manage its own conversational state. It is a stateless, tool-executing agent. It relies on the host framework (e.g., LangChain, custom CLI, or OpenGAP server) to handle state, memory, and orchestration.

## Error Handling
Errors are returned as structured objects containing a machine-readable `code` and a human-readable `message`, allowing the host framework to make programmatic decisions on how to handle failures.

## Portability
Because the business logic relies entirely on pure Python (and a few dependencies like `pypdf`), it can be wrapped in an adapter for any major AI framework or executed directly from a CLI or REST API.
