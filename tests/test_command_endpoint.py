"""
Tests for the POST "/command" endpoint that controls the rover.
"""
import pytest
from fastapi import status
from unittest.mock import patch

from schemas import Direction
from config import settings


def test_move_forward(client):
    """
    Test that the rover moves forward correctly.
    """
    command_data = {"command_input": "F"}
    response = client.post("/command", json=command_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["longitude"] == 0
    assert data["latitude"] == 1  # Moved north by 1
    assert data["direction"] == Direction.NORTH


def test_move_backward(client):
    """
    Test that the rover moves backward correctly.
    """
    command_data = {"command_input": "B"}
    response = client.post("/command", json=command_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["longitude"] == 0
    assert data["latitude"] == -1  # Moved south by 1
    assert data["direction"] == Direction.NORTH


def test_rotate_left(client):
    """
    Test that the rover rotates left correctly.
    """
    command_data = {"command_input": "L"}
    response = client.post("/command", json=command_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["longitude"] == 0
    assert data["latitude"] == 0
    assert data["direction"] == Direction.WEST


def test_rotate_right(client):
    """
    Test that the rover rotates right correctly.
    """
    command_data = {"command_input": "R"}
    response = client.post("/command", json=command_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["longitude"] == 0
    assert data["latitude"] == 0
    assert data["direction"] == Direction.EAST


def test_complex_movement(client):
    """
    Test a complex sequence of movements and rotations.
    """
    # Move forward, rotate right, move forward, rotate left, move backward
    command_data = {"command_input": "FRFLB"}
    response = client.post("/command", json=command_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["longitude"] == 1
    assert data["latitude"] == 0
    assert data["direction"] == Direction.NORTH


def test_obstacle_detection(client, monkeypatch):
    """
    Test that the rover stops when it encounters an obstacle.
    """
    # Patch the settings to include an obstacle at (0, 1)
    monkeypatch.setattr(settings, "INITIAL_OBSTACLES", [(0, 1)])
    
    # Try to move forward (north) into the obstacle
    command_data = {"command_input": "F"}
    response = client.post("/command", json=command_data)
    
    # The rover should not move
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["longitude"] == 0
    assert data["latitude"] == 0  # Still at the original position
    assert data["direction"] == Direction.NORTH


def test_invalid_command(client):
    """
    Test that invalid commands are rejected.
    """
    command_data = {"command_input": "X"}  # Invalid command
    response = client.post("/command", json=command_data)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data


@pytest.mark.parametrize(
    "command_input,expected_longitude,expected_latitude,expected_direction",
    [
        ("F", 0, 1, Direction.NORTH),  # Move forward
        ("B", 0, -1, Direction.NORTH),  # Move backward
        ("L", 0, 0, Direction.WEST),   # Rotate left
        ("R", 0, 0, Direction.EAST),   # Rotate right
        ("FF", 0, 2, Direction.NORTH),  # Move forward twice
        ("FB", 0, 0, Direction.NORTH),  # Move forward then backward
        ("FRFL", 1, 1, Direction.NORTH),  # Complex movement
    ],
)
def test_parameterized_commands(
    client, command_input, expected_longitude, expected_latitude, expected_direction
):
    """
    Parameterized test for various command sequences.
    """
    command_data = {"command_input": command_input}
    response = client.post("/command", json=command_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["longitude"] == expected_longitude
    assert data["latitude"] == expected_latitude
    assert data["direction"] == expected_direction