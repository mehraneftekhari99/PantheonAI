# PantheonAI

PantheonAI is a multi-user long-term history language learning model (LLM) chat application. It uses OpenAI's GPT-3.5-turbo model to generate responses to user prompts and maintains a history of the conversation.

## Features

- Generate responses to user prompts using GPT-3.5-turbo.
- Maintain a history of the conversation.
- Support for multiple prompts.
- A client interface for interacting with the chat application.

## Installation

This project uses Poetry for dependency management. To install the project, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/mehraneftekhari99/PantheonAI.git
```

2. Navigate to the project directory:

```bash
cd PantheonAI
```

3. Install the dependencies:

```bash
poetry install
```

## Usage

To run the project, use the following command:

```bash
python main.py
```

The application will start on localhost port 5000.

To interact with the chat application, run the client script:

```bash
python client.py
```

The client will connect to the server running on localhost port 5000 by default. You can change the server IP and port by setting the `PANTHEON_SERVER_IP` and `PANTHEON_SERVER_PORT` environment variables, respectively.

## Dependencies

This project depends on the following Python packages:

- zep-python
- flask
- openai
- colorama
- gnureadline
- fastapi
- uvicorn
- gunicorn
- pydantic

> **Note:** Zep should be running on localhost. You can use the [official docker compose](https://github.com/getzep/zep#quick-start).

## Contributing

Contributions are welcome. Please open an issue to discuss your ideas before making changes.

## License

This project is licensed under the [GPL-3.0 License](https://www.tldrlegal.com/license/gnu-general-public-license-v3-gpl-3).
