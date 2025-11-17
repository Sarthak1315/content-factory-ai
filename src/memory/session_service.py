"""
Session Service - Manages session state for agent workflows
"""

from typing import Any, Dict, Optional
from datetime import datetime
import uuid


class Session:
    """Represents a session with state management"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self._state: Dict[str, Any] = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from session state"""
        return self._state.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set value in session state"""
        self._state[key] = value
        self.updated_at = datetime.now()
    
    def delete(self, key: str):
        """Delete key from session state"""
        if key in self._state:
            del self._state[key]
            self.updated_at = datetime.now()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all session state"""
        return self._state.copy()
    
    def clear(self):
        """Clear all session state"""
        self._state = {}
        self.updated_at = datetime.now()
    
    def get_duration(self) -> float:
        """Get session duration in seconds"""
        return (self.updated_at - self.created_at).total_seconds()


class SessionService:
    """Manages multiple sessions (InMemorySessionService)"""
    
    def __init__(self):
        self._sessions: Dict[str, Session] = {}
    
    def create_session(self, session_id: Optional[str] = None) -> Session:
        """Create new session"""
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        if session_id in self._sessions:
            return self._sessions[session_id]
        
        session = Session(session_id)
        self._sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get existing session"""
        return self._sessions.get(session_id)
    
    def end_session(self, session_id: str):
        """End and remove session"""
        if session_id in self._sessions:
            del self._sessions[session_id]
    
    def get_all_sessions(self) -> Dict[str, Session]:
        """Get all active sessions"""
        return self._sessions.copy()
    
    def clear_all_sessions(self):
        """Clear all sessions"""
        self._sessions = {}