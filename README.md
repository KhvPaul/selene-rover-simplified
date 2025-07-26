# Selene Rover

A simplified API for controlling a rover on the surface of the Moon.

## Overview

This project provides a FastAPI application that allows you to:
- Retrieve the current state of the rover (position and direction)
- Send commands to move and rotate the rover

The rover can move forward and backward, and rotate left and right. It also detects obstacles and stops when it encounters one.

## API Endpoints

### GET "/"

Retrieves the current state of the rover.

**Response:**
```json
{
  "id": 1,
  "longitude": 0,
  "latitude": 0,
  "direction": "NORTH"
}
```

### POST "/command"

Sends commands to the rover.

**Request:**
```json
{
  "command_input": "FFRFFLB"
}
```

Where:
- F: Move forward
- B: Move backward
- L: Rotate left
- R: Rotate right

**Response:**
```json
{
  "id": 1,
  "longitude": 2,
  "latitude": 3,
  "direction": "EAST"
}
```

## Running the Application

1. Set up the environment variables in `.env` file
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Testing

The project includes a comprehensive test suite for the API endpoints.

### Running Tests

You can run the tests using the provided script:

```bash
./run_tests.sh
```

Or manually:

```bash
pip install -r test-requirements.txt
pytest
```

### Test Coverage

The tests cover:
- Retrieving the rover state
- Basic movement commands (forward, backward)
- Rotation commands (left, right)
- Complex movement sequences
- Obstacle detection
- Error handling for invalid commands

For more details about the tests, see the [tests/README.md](tests/README.md) file.

## Project Structure

- `main.py` - FastAPI application and API endpoints
- `models.py` - SQLModel database models
- `schemas.py` - Pydantic schemas for API requests/responses
- `config.py` - Application settings
- `logger.py` - Logging configuration
- `tests/` - Test suite
  - `conftest.py` - Test fixtures
  - `test_get_rover_state.py` - Tests for GET endpoint
  - `test_command_endpoint.py` - Tests for POST endpoint

## Dependencies

- FastAPI - Web framework
- SQLModel - ORM (combines SQLAlchemy and Pydantic)
- Pydantic - Data validation
- Pytest - Testing framework