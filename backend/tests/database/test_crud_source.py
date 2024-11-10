# backend/tests/database/test_crud_source.py

import pytest
from sqlalchemy.orm import Session
from app.crud.source import (
    get_source,
    get_source_by_name,
    get_sources,
    create_source,
    update_source,
    delete_source
)
from app.schemas.source import SourceCreate, SourceUpdate
from app.models.source import Source
from app.db.session import SessionLocal
from fastapi.exceptions import HTTPException

# Fixture for providing a test database session
@pytest.fixture
def test_db_session():
    """Fixture to provide a database session with rollback for testing."""
    db = SessionLocal()
    db.begin_nested()

    yield db

    db.rollback()
    db.close()

# Mock data for source creation
mock_source_data = {
    "name": "Test Source",
    "api_endpoint": "http://api.testsource.com",
    "scrape_source_url": "http://testsource.com"
}

def test_create_source(test_db_session: Session):
    """Test creating a new source."""
    source_in = SourceCreate(**mock_source_data)
    created_source = create_source(test_db_session, source_in)

    assert created_source.name == mock_source_data["name"]
    assert created_source.api_endpoint == mock_source_data["api_endpoint"]
    assert created_source.scrape_source_url == mock_source_data["scrape_source_url"]
    delete_source(test_db_session, created_source.source_id)
def test_get_source(test_db_session: Session):
    """Test retrieving a source by ID."""
    # First, create the source to retrieve
    source_in = SourceCreate(**mock_source_data)
    created_source = create_source(test_db_session, source_in)

    # Retrieve the source
    fetched_source = get_source(test_db_session, created_source.source_id)
    assert fetched_source.source_id == created_source.source_id
    delete_source(test_db_session, created_source.source_id)
def test_get_source_by_name(test_db_session: Session):
    """Test retrieving a source by name."""
    # First, create the source to retrieve
    source_in = SourceCreate(**mock_source_data)
    created_source = create_source(test_db_session, source_in)

    # Retrieve the source by name
    fetched_source = get_source_by_name(test_db_session, mock_source_data["name"])
    assert fetched_source.name == mock_source_data["name"]
    delete_source(test_db_session, created_source.source_id)
def test_get_sources(test_db_session: Session):
    """Test retrieving a list of sources with pagination."""
    # Create a few sources for pagination test
    sources_data = [
        {"name": "Source 1", "api_endpoint": "http://api.source1.com", "scrape_source_url": "http://source1.com"},
        {"name": "Source 2", "api_endpoint": "http://api.source2.com", "scrape_source_url": "http://source2.com"},
        {"name": "Source 3", "api_endpoint": "http://api.source3.com", "scrape_source_url": "http://source3.com"}
    ]
    new_sources = []
    for data in sources_data:
        source_in = SourceCreate(**data)
        new_source = create_source(test_db_session, source_in)
        new_sources.append(new_source)

    # Retrieve paginated sources
    sources = get_sources(test_db_session, skip=0, limit=2)
    assert len(sources) == 2  # Should return only 2 as per limit
    for source in new_sources:
        delete_source(test_db_session, source.source_id)

def test_update_source(test_db_session: Session):
    """Test updating a source."""
    # First, create a source to update
    source_in = SourceCreate(**mock_source_data)
    created_source = create_source(test_db_session, source_in)

    # Update data
    update_data = SourceUpdate(name="Updated Source", api_endpoint="http://updatedapi.com")
    updated_source = update_source(test_db_session, created_source.source_id, update_data)

    # Verify the updated fields
    assert updated_source.name == "Updated Source"
    assert updated_source.api_endpoint == "http://updatedapi.com"
    delete_source(test_db_session, created_source.source_id)

def test_delete_source(test_db_session: Session):
    """Test deleting a source."""
    # Create a source to delete
    source_in = SourceCreate(**mock_source_data)
    created_source = create_source(test_db_session, source_in)

    # Delete the source
    deleted_source = delete_source(test_db_session, created_source.source_id)
    assert deleted_source.source_id == created_source.source_id

    # Verify source no longer exists
    with pytest.raises(HTTPException) as exc_info:
        get_source(test_db_session, created_source.source_id)
    assert exc_info.value.status_code == 404

def test_get_source_not_found(test_db_session: Session):
    """Test error handling when a source is not found by ID."""
    with pytest.raises(HTTPException) as exc_info:
        get_source(test_db_session, source_id=9999)
    assert exc_info.value.status_code == 404

def test_get_source_by_name_not_found(test_db_session: Session):
    """Test error handling when a source is not found by name."""
    with pytest.raises(HTTPException) as exc_info:
        get_source_by_name(test_db_session, source="NonExistentSource")
    assert exc_info.value.status_code == 404

def test_delete_source_not_found(test_db_session: Session):
    """Test error handling when trying to delete a non-existent source."""
    with pytest.raises(HTTPException) as exc_info:
        delete_source(test_db_session, source_id=9999)
    assert exc_info.value.status_code == 404