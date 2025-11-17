"""
Test cases for memory and session management
"""

import pytest
import os
import tempfile
import shutil
from src.memory.memory_bank import MemoryBank
from src.memory.session_service import SessionService, Session


class TestMemoryBank:
    """Test MemoryBank functionality"""
    
    @pytest.fixture
    def temp_memory_dir(self):
        """Create temporary directory for memory tests"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_memory_bank_initialization(self, temp_memory_dir):
        """Test memory bank initializes correctly"""
        bank = MemoryBank(storage_path=temp_memory_dir)
        assert os.path.exists(bank.memory_file)
    
    def test_set_and_get(self, temp_memory_dir):
        """Test setting and getting values"""
        bank = MemoryBank(storage_path=temp_memory_dir)
        bank.set('test_key', 'test_value')
        
        assert bank.get('test_key') == 'test_value'
    
    def test_get_default_value(self, temp_memory_dir):
        """Test getting non-existent key returns default"""
        bank = MemoryBank(storage_path=temp_memory_dir)
        result = bank.get('nonexistent', 'default')
        
        assert result == 'default'
    
    def test_append_to_history(self, temp_memory_dir):
        """Test appending to history list"""
        bank = MemoryBank(storage_path=temp_memory_dir)
        bank.append_to_history('history', 'item1')
        bank.append_to_history('history', 'item2')
        
        history = bank.get('history')
        assert len(history) == 2
        assert 'item1' in history
        assert 'item2' in history
    
    def test_get_history_with_limit(self, temp_memory_dir):
        """Test getting limited history"""
        bank = MemoryBank(storage_path=temp_memory_dir)
        for i in range(10):
            bank.append_to_history('items', f'item{i}')
        
        recent = bank.get_history('items', limit=3)
        assert len(recent) == 3
        assert recent[0] == 'item7'
    
    def test_delete_key(self, temp_memory_dir):
        """Test deleting key"""
        bank = MemoryBank(storage_path=temp_memory_dir)
        bank.set('key', 'value')
        bank.delete('key')
        
        assert bank.get('key') is None
    
    def test_clear_all(self, temp_memory_dir):
        """Test clearing all memory"""
        bank = MemoryBank(storage_path=temp_memory_dir)
        bank.set('key1', 'value1')
        bank.set('key2', 'value2')
        bank.clear_all()
        
        assert bank.get_all() == {}
    
    def test_persistence(self, temp_memory_dir):
        """Test memory persists across instances"""
        bank1 = MemoryBank(storage_path=temp_memory_dir)
        bank1.set('persistent_key', 'persistent_value')
        
        bank2 = MemoryBank(storage_path=temp_memory_dir)
        assert bank2.get('persistent_key') == 'persistent_value'


class TestSession:
    """Test Session functionality"""
    
    def test_session_creation(self):
        """Test session is created correctly"""
        session = Session('test_session')
        assert session.session_id == 'test_session'
        assert session.created_at is not None
    
    def test_set_and_get(self):
        """Test setting and getting session values"""
        session = Session('test')
        session.set('key', 'value')
        
        assert session.get('key') == 'value'
    
    def test_get_default(self):
        """Test getting with default value"""
        session = Session('test')
        result = session.get('nonexistent', 'default')
        
        assert result == 'default'
    
    def test_delete(self):
        """Test deleting session key"""
        session = Session('test')
        session.set('key', 'value')
        session.delete('key')
        
        assert session.get('key') is None
    
    def test_get_all(self):
        """Test getting all session state"""
        session = Session('test')
        session.set('key1', 'value1')
        session.set('key2', 'value2')
        
        all_state = session.get_all()
        assert len(all_state) == 2
        assert all_state['key1'] == 'value1'
    
    def test_clear(self):
        """Test clearing session state"""
        session = Session('test')
        session.set('key', 'value')
        session.clear()
        
        assert session.get_all() == {}
    
    def test_get_duration(self):
        """Test getting session duration"""
        session = Session('test')
        import time
        time.sleep(0.1)
        session.set('key', 'value')
        
        duration = session.get_duration()
        assert duration >= 0.1


class TestSessionService:
    """Test SessionService functionality"""
    
    def test_create_session(self):
        """Test creating new session"""
        service = SessionService()
        session = service.create_session('test_session')
        
        assert session.session_id == 'test_session'
    
    def test_create_session_auto_id(self):
        """Test creating session with auto-generated ID"""
        service = SessionService()
        session = service.create_session()
        
        assert session.session_id is not None
        assert len(session.session_id) > 0
    
    def test_get_session(self):
        """Test getting existing session"""
        service = SessionService()
        created = service.create_session('test')
        retrieved = service.get_session('test')
        
        assert retrieved is created
    
    def test_get_nonexistent_session(self):
        """Test getting non-existent session returns None"""
        service = SessionService()
        result = service.get_session('nonexistent')
        
        assert result is None
    
    def test_end_session(self):
        """Test ending session"""
        service = SessionService()
        service.create_session('test')
        service.end_session('test')
        
        assert service.get_session('test') is None
    
    def test_get_all_sessions(self):
        """Test getting all sessions"""
        service = SessionService()
        service.create_session('session1')
        service.create_session('session2')
        
        all_sessions = service.get_all_sessions()
        assert len(all_sessions) == 2
    
    def test_clear_all_sessions(self):
        """Test clearing all sessions"""
        service = SessionService()
        service.create_session('session1')
        service.create_session('session2')
        service.clear_all_sessions()
        
        assert len(service.get_all_sessions()) == 0