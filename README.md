# AgentForge

AgentForge lets you design, configure, and deploy custom AI agents through an interactive wizard. Define agent personality, tools, memory, and goals — then watch your agent come to life. Built with Python Flask and Xiaomi MiMo V2.5 Pro for intelligent agent reasoning.

## Features

- **Agent Personality Builder**
- **Tool Configuration Wizard**
- **Memory Strategy Designer**
- **Goal Hierarchy Planner**
- **Agent Blueprint Export**

## Tech Stack

- **Backend**: Python 3 + Flask
- **AI Model**: Xiaomi MiMo V2.5 Pro
- **Frontend**: Tailwind CSS
- **Deployment**: Vercel

## Local Development

```bash
pip install -r requirements.txt
python api/index.py
```

## API

```
POST /api/generate
Content-Type: application/json

{
  "input": "Your message here"
}
```

## Environment Variables

```
MIMO_API_KEY=your_key
MIMO_BASE_URL=https://llm.tbuglabs.com/v1
MIMO_MODEL=mimo/mimo-v2.5
```

## License

MIT
