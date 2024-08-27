# Tennis Score Board

Tennis Score Board is a web application for tracking scores in tennis matches.

## Features

- Create and manage tennis matches
- Real-time score tracking
- View match history
- Support for tennis scoring rules

## Technologies

- Python 3.11
- SQLAlchemy
- Alembic (for database migrations)
- uWSGI
- Jinja2
- MySQL
- Docker and Docker Compose

## Installation and Setup

### Prerequisites

- Docker
- Docker Compose
- Make 

### Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/your-username/tennis-score-board.git
cd tennis-score-board
```

2. Create a `.env` file in the project root directory and fill it with the necessary environment variables (see `.env.dist` for reference).

3. Build, make migrations and run the containers:

```bash
make init
make up
```

4. The application should now be accessible at `http://localhost:8000`.

## Usage

- To create a new match, navigate to `/new-match`
- To view the current score of a match, use `/match-score?uuid={match_uuid}`
- The list of all matches is available at `/matches`

## Development

### Creating Migrations

To create a new database migration, use:

```bash
make makemigrations
```

### Running Tests

```bash
make test
```

## Project Structure

```bash
tennis_score_board/
├── src/
│   ├── tennis_score_board/
│   │   ├── adapters/
│   │   ├── application/
│   │   ├── domain/
│   │   └── ...
│   └── mini_framework/
├── tests/
├── alembic/
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── pyproject.toml
```



