# Portfolio Summarizer

A web application that summarizes portfolio content using a Language Learning Model (LLM), hosted on Vercel. This tool extracts content from provided portfolio URLs and delivers concise, professional summaries to the frontend.

## Features

- **Portfolio Summarization**: Takes a portfolio URL, extracts its content, and generates a professional summary using an LLM.
- **FastAPI Backend**: Built as a FastAPI-based API for quick and efficient processing.
- **Frontend Integration**: Consumed by our portfolio page for seamless user experience.
- **Real-time Logging**: Application logs are stored and monitored on Grafana Loki Cloud in real-time.
- **Health Monitoring**: Uses UptimeRobot to ping the healthcheck API, ensuring timely alerts if the service goes down.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Hosting**: Vercel
- **LLM**: Language Learning Model (specific model details TBD)
- **Logging**: Grafana Loki Cloud
- **Monitoring**: UptimeRobot
- **Frontend**: Integrated with our portfolio page (framework TBD)

## Getting Started

### Prerequisites

- Python 3.9+
- Vercel account for deployment
- Grafana Loki Cloud account for logging
- UptimeRobot account for health monitoring
- API keys for LLM integration (if applicable)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/portfolio-summarizer.git
   cd portfolio-summarizer
   Install dependencies:
   pip install -r requirements.txt
   Set up environment variables:
    - Create a .env file in the root directory.
    - Add necessary keys (e.g., LLM API key, Grafana Loki credentials, etc.)

    LLM_API_KEY=your-llm-api-key
    GRAFANA_LOKI_URL=your-loki-url
    GRAFANA_LOKI_USER=your-loki-user
    GRAFANA_LOKI_PASSWORD=your-loki-password

2. Run the FastAPI server locally:
    ```bash 
    uvicorn main:app --reload

## API Endpoints
- POST /summarize
  - Description: Accepts a portfolio URL and returns a summarized version.
  - Request Body:
        {
  "url": "https://example.com/portfolio"
}

  - Response: {
  "summary": "A concise, professional summary of the portfolio content."
}

- GET /healthcheck
  - Description: Health check endpoint monitored by UptimeRobot.
  - Response {
  "status": "Portfolio Summarizer API is running"
}

## Monitoring
- Logs: Real-time logs are pushed to Grafana Loki Cloud for debugging and performance tracking.
- Uptime: UptimeRobot pings the /healthcheck endpoint every 5 minutes. Alerts are sent via email if the service is down.


## Contributing

This is a personal portfolio project, but I’m open to suggestions! Feel free to open an issue or submit a pull request if you have ideas for improvement.

## License

This project is licensed under the [[Apache LICENSE 2.0](https://www.apache.org/licenses/LICENSE-2.0)].

## Contact

For questions, suggestions, or support, reach out at 
- **sk0551460@gmail.com** 
- **shivam.hireme@gmail.com**.

## Support the Project

Help support continued development and improvements:

- **Follow on LinkedIn**: Stay connected for updates – [LinkedIn Profile](https://www.linkedin.com/in/shivam-hireme/)
- **Buy Me a Coffee**: Appreciate the project? [Buy Me a Coffee](https://buymeacoffee.com/shivamshane)
- **Visit my Portfolio**: [Shivam's Portfolio](https://shivam-portfoliio.vercel.app/)

