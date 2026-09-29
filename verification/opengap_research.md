# OpenGAP Research

## Repository Inspected
- URL: `https://github.com/open-gitagent/opengap`
- Branch: `main` (latest as of 2026-09-29)

## Version Information
- **gitagent specification version:** `0.1.0`
- **npm package version:** `@open-gitagent/opengap 0.5.0`

## Manifest Requirements (`agent.yaml`)
- **Required fields:** `name`, `version`, `description`.
- **Naming rule:** `name` must match `^[a-z][a-z0-9-]*$`.
- **Tools property:** Array of strings (tool file names without extension).
- No unsupported fields are allowed (strict `additionalProperties: false` except for specific objects like `metadata`).
- Optional fields supported: `spec_version`, `model`, `tools`, `skills`, `metadata`, `compliance`, `agents`, `delegation`, `runtime`, `a2a`, `mcp_servers`, `tags`, etc.

## Tool Requirements (`tool.yaml`)
- **Required fields:** `name`, `description`, `input_schema`.
- **Naming rule:** `name` must match `^[a-z][a-z0-9-]*$`.
- **Input schema:** Must follow JSON schema structure.
- **Optional fields supported:** `output_schema`, `implementation`, `annotations`, `version`.
- `implementation` field specifies script runtime (e.g., `python3`), type (`script`), and `path`.

## Validation Command
- Installed via npm: `@open-gitagent/opengap`
- Command: `opengap validate` (or `npx @open-gitagent/opengap validate`)
- Schema validation enforces `additionalProperties: false` in most places, meaning no made-up fields.

## Official Example Observations
- Examples keep manifests small and rely heavily on Markdown for documentation (`SOUL.md`, `RULES.md`, etc.).
- Agents are meant to be modular and framework-agnostic.
