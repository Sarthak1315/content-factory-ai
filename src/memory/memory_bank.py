"""
Memory Bank - Long-term memory storage for agents
"""

import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime


class MemoryBank:
    """Persistent storage for agent memory"""
    
    def __init__(self, storage_path: str = './memory'):
        self.storage_path = storage_path
        self.memory_file = os.path.join(storage_path, 'memory.json')
        self._ensure_storage_exists()
        self._memory = self._load_memory()
    
    def _ensure_storage_exists(self):
        """Create storage directory if it doesn't exist"""
        os.makedirs(self.storage_path, exist_ok=True)
        
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                json.dump({}, f)
    
    def _load_memory(self) -> Dict:
        """Load memory from disk"""
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_memory(self):
        """Save memory to disk"""
        with open(self.memory_file, 'w') as f:
            json.dump(self._memory, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from memory"""
        return self._memory.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set value in memory"""
        self._memory[key] = value
        self._save_memory()
    
    def append_to_history(self, key: str, value: Any):
        """Append value to a list in memory"""
        if key not in self._memory:
            self._memory[key] = []
        
        if not isinstance(self._memory[key], list):
            self._memory[key] = [self._memory[key]]
        
        self._memory[key].append(value)
        self._save_memory()
    
    def get_history(self, key: str, limit: Optional[int] = None) -> List:
        """Get history list with optional limit"""
        history = self._memory.get(key, [])
        
        if limit:
            return history[-limit:]
        return history
    
    def delete(self, key: str):
        """Delete key from memory"""
        if key in self._memory:
            del self._memory[key]
            self._save_memory()
    
    def clear_all(self):
        """Clear all memory"""
        self._memory = {}
        self._save_memory()
    
    def get_all(self) -> Dict:
        """Get all memory"""
        return self._memory.copy()