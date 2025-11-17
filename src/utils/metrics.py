"""
Metrics Collector - Track performance metrics and timings
"""

from typing import Dict, List, Optional
from datetime import datetime
import time


class MetricsCollector:
    """Collect and track metrics for agents and workflows"""
    
    def __init__(self):
        self._timers: Dict[str, float] = {}
        self._metrics: Dict[str, List[float]] = {}
        self._counters: Dict[str, int] = {}
    
    def start_timer(self, name: str):
        """Start a timer"""
        self._timers[name] = time.time()
    
    def stop_timer(self, name: str) -> float:
        """Stop a timer and return elapsed time"""
        if name not in self._timers:
            return 0.0
        
        elapsed = time.time() - self._timers[name]
        
        if name not in self._metrics:
            self._metrics[name] = []
        self._metrics[name].append(elapsed)
        
        del self._timers[name]
        
        return elapsed
    
    def get_timer(self, name: str) -> Optional[float]:
        """Get current timer value"""
        if name not in self._timers:
            return None
        return time.time() - self._timers[name]
    
    def record_metric(self, name: str, value: float):
        """Record a metric value"""
        if name not in self._metrics:
            self._metrics[name] = []
        self._metrics[name].append(value)
    
    def increment_counter(self, name: str, amount: int = 1):
        """Increment a counter"""
        if name not in self._counters:
            self._counters[name] = 0
        self._counters[name] += amount
    
    def get_metric_stats(self, name: str) -> Dict:
        """Get statistics for a metric"""
        if name not in self._metrics or not self._metrics[name]:
            return {
                'count': 0,
                'mean': 0,
                'min': 0,
                'max': 0,
                'total': 0
            }
        
        values = self._metrics[name]
        return {
            'count': len(values),
            'mean': sum(values) / len(values),
            'min': min(values),
            'max': max(values),
            'total': sum(values)
        }
    
    def get_counter(self, name: str) -> int:
        """Get counter value"""
        return self._counters.get(name, 0)
    
    def get_all_timings(self) -> Dict[str, Dict]:
        """Get all timing statistics"""
        result = {}
        for name in self._metrics:
            stats = self.get_metric_stats(name)
            result[name] = {
                'avg_seconds': round(stats['mean'], 2),
                'min_seconds': round(stats['min'], 2),
                'max_seconds': round(stats['max'], 2),
                'total_seconds': round(stats['total'], 2),
                'count': stats['count']
            }
        return result
    
    def get_all_counters(self) -> Dict[str, int]:
        """Get all counters"""
        return self._counters.copy()
    
    def reset(self):
        """Reset all metrics"""
        self._timers = {}
        self._metrics = {}
        self._counters = {}
    
    def get_summary(self) -> Dict:
        """Get comprehensive metrics summary"""
        return {
            'timings': self.get_all_timings(),
            'counters': self.get_all_counters(),
            'active_timers': list(self._timers.keys())
        }