"""
Tests for the GET "/" endpoint that retrieves the rover state.
"""
import pytest
from fastapi import status

from schemas import Direction


def test_get_rover_state(client):
    """
    Test that the GET "/" endpoint returns the current rover state.
    """
    response = client.get("/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 1
    assert data["longitude"] == 0
    assert data["latitude"] == 0
    assert data["direction"] == Direction.NORTH


def test_get_rover_state_after_initialization(client, session):
    """
    Test that the GET "/" endpoint returns the correct rover state
    after it has been initialized with different values.
    """
    # Update the rover state in the database
    response = client.get("/")
    rover_state = response.json()
    
    # Modify the rover state using the command endpoint
    command_data = {"command_input": "F"}  # Move forward
    response = client.post("/command", json=command_data)
    
    assert response.status_code == status.HTTP_200_OK
    updated_data = response.json()
    assert updated_data["longitude"] == 0
    assert updated_data["latitude"] == 1  # Moved north by 1
    assert updated_data["direction"] == Direction.NORTH
    
    # Verify the state is persisted
    response = client.get("/")
    persisted_data = response.json()
    assert persisted_data["longitude"] == 0
    assert persisted_data["latitude"] == 1
    assert persisted_data["direction"] == Direction.NORTH