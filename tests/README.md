# API Tests for Selene Rover

This directory contains tests for the Selene Rover API endpoints.

## Test Structure

- `conftest.py` - Contains pytest fixtures for setting up the test environment
- `test_get_rover_state.py` - Tests for the GET "/" endpoint
- `test_command_endpoint.py` - Tests for the POST "/command" endpoint

## Running the Tests

To run the tests, first install the test dependencies:

```bash
pip install -r test-requirements.txt
```

Then run the tests using pytest:

```bash
pytest tests/
```

## Test Coverage

### GET "/" Endpoint

- `test_get_rover_state` - Tests that the endpoint returns the current rover state
- `test_get_rover_state_after_initialization` - Tests that the endpoint returns the correct rover state after it has been modified

### POST "/command" Endpoint

- `test_move_forward` - Tests that the rover moves forward correctly
- `test_move_backward` - Tests that the rover moves backward correctly
- `test_rotate_left` - Tests that the rover rotates left correctly
- `test_rotate_right` - Tests that the rover rotates right correctly
- `test_complex_movement` - Tests a complex sequence of movements and rotations
- `test_obstacle_detection` - Tests that the rover stops when it encounters an obstacle
- `test_invalid_command` - Tests that invalid commands are rejected
- `test_parameterized_commands` - Parameterized test for various command sequences

## Test Environment

The tests use an in-memory SQLite database instead of PostgreSQL to avoid external dependencies and make tests faster and more isolated. The database is initialized with a rover state at position (0, 0) facing NORTH.

## Adding New Tests

When adding new tests, make sure to:

1. Use the fixtures provided in `conftest.py`
2. Reset the rover state between tests if necessary
3. Add documentation for the new tests in this README