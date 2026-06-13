# SuperInstance

<!-- badges -->
<a href="docs/status.html"><img src="https://img.shields.io/badge/API-operational-00E6D6?style=flat-square&labelColor=0a0a0f" alt="API Status"></a>
<a href="https://www.npmjs.com/package/@superinstance/tminus-client"><img src="https://img.shields.io/badge/npm-%40superinstance%2Ftminus--client-0a0a0f?style=flat-square&logo=npm&logoColor=white&labelColor=0a0a0f" alt="npm"></a>
<a href="docs/index.html"><img src="https://img.shields.io/badge/docs-live-00E6D6?style=flat-square&labelColor=0a0a0f" alt="Docs"></a>
<img src="https://img.shields.io/badge/license-MIT-00E6D6?style=flat-square&labelColor=0a0a0f" alt="License">

> Multi-agent AI fleet infrastructure with semantic search, temporal cueing, and conservation-driven orchestration.
> Every instance is a vessel. The fleet emerges from signal overlap.

## 🚀 Quick Start

```bash
# Install the client SDK
npm install @superinstance/tminus-client
```

```js
import { TMinusClient } from '@superinstance/tminus-client';

const client = new TMinusClient('https://fleet-vector-api.casey-digennaro.workers.dev');

// Semantic search across 1,500+ AI crates
const results = await client.search('distributed consensus protocol', 5);
console.log(results);
```

Or just use cURL:

```bash
curl -X POST https://fleet-vector-api.casey-digennaro.workers.dev/search \
  -H "Content-Type: application/json" \
  -d '{"query": "multi-agent orchestration", "topK": 5}'
```

📖 **[Full documentation →](docs/index.html)** | **[API reference →](https://fleet-vector-api.casey-digennaro.workers.dev/docs)** | **[OpenAPI spec →](https://fleet-vector-api.casey-digennaro.workers.dev/openapi.json)**

---

## The Key Idea

Every AI agent obeys a conservation law: **γ + η = C**

- **γ** (generation cost) — tokens, time, API calls
- **η** (innovation value) — new code, tests, discoveries
- **C** — total budget, conserved across all agents

Spend too much on generation (churning tokens without shipping), and η collapses. Ship too fast without thinking, and γ spikes on rework. The sweet spot isn't a setting — it's a **law**.

SuperInstance makes this observable.

## What's Here

| What | Where |
|------|-------|
| **Homepage** | [superinstance.ai](https://superinstance.ai) |
| **Semantic Search API** | [fleet-vector-api](https://fleet-vector-api.casey-digennaro.workers.dev/docs) |
| **npm Client** | [@superinstance/tminus-client](https://www.npmjs.com/package/@superinstance/tminus-client) |
| **npm Dispatcher** | [@superinstance/tminus-dispatcher](https://www.npmjs.com/package/@superinstance/tminus-dispatcher) |
| **Fleet MCP Server** | [fleet-mcp-server](https://github.com/SuperInstance/fleet-mcp-server) |
| **Bottle Protocol** | [fleet-bottle](https://github.com/SuperInstance/fleet-bottle) |
| **Conservation Tracker** | [fleet-conservation](https://github.com/SuperInstance/fleet-conservation) |
| **Docs Hub** | [docs/index.html](docs/index.html) |

## API Endpoints (Live, Free)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/search` | Semantic search across the crate ecosystem |
| `POST` | `/recommend` | Context-aware crate recommendations |
| `POST` | `/similar` | Find crates similar to a given one |
| `GET` | `/stats` | Index stats (model, dimensions, crate count) |
| `GET` | `/clusters` | Crates grouped by domain |
| `GET` | `/docs` | Interactive HTML API documentation |
| `GET` | `/openapi.json` | OpenAPI 3.1 specification |

Base URL: `https://fleet-vector-api.casey-digennaro.workers.dev`

## The Fleet

Four vessels, heterogeneous hardware, one conservation law:

| Vessel | Hardware | Role |
|--------|----------|------|
| **Oracle1** 🔮 | Oracle Cloud ARM64 24GB | The Lighthouse — coordinates fleet, writes research |
| **JetsonClaw1** ⚡ | Jetson Orin Nano | The Scout — edge inference, GPU-native rooms |
| **Forgemaster** ⚒️ | RTX 4050 WSL2 | The Forge — security audits, proofs, LoRA training |
| **CoCapn-claw** 🎭 | Kimi K2.5 / Telegram | The First Mate — frontend, collaboration, play-testing |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [GOOD_FIRST_ISSUES.md](GOOD_FIRST_ISSUES.md).

## License

MIT
