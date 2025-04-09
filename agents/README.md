# Agents

A catalog of templates designed to help you get started quickly with examples that can be easily customised, extended and deployed on the watsonx platform.

## Key features

- 🌐 **Framework agnostic**: Build agents with any framework.
- ☁️ **Deployment**: Deploy agents as AI services with one command.

## Get started

1. **Install** the CLI 

```bash
pip install ibm-watsonx-ai-cli
```

2. **Create** the template

```bash
watsonx-ai template new
```

3. **Configure** the template

Go to the [Developer Access](https://dataplatform.cloud.ibm.com/developer-access) to find your environment variables.

```bash
cp config.toml.example config.toml
```

3. **Run** the template

```bash
watsonx-ai template invoke "Hello"
```

3. **Deploy** the template

```bash
watsonx-ai template new
```

## Official Templates

Designed to help you get started quickly with examples that can be easily customized and extended.

| Template                 | 
| ------------------------ |
| [LangGraph](./base/langgraph-react-agent/) |
| [LlamaIndex](./base/llamaindex-websearch-agent/) |
| [CrewAI](./base/crewai-websearch-agent/) |

## Community Templates

Templates published and maintained by the community.

| Template                                            | Framework | Description                                                       |
| --------------------------------------------------- | --------- | ----------------------------------------------------------------- |
| [Agentic RAG](./community/langgraph-agentic-rag/) | Langraph  | Agent to improve how information is retrieved from vector store and used. |
| [arXiv Research Agent](./community/langgraph-arxiv-research/) | Langraph  | Agent to search and summarize research papers published on arXiv. |

## Support

See the [watsonx Developer Hub](https://ibm.com/watsonx/developer) for quickstarts and documentation. Please reach out to us on [Discord](https://ibm.biz/wx-discord) if you have any questions or want to share feedback. We'd love to hear from you!
