import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class MemoryManager:
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    role TEXT,
                    content TEXT,
                    conversation_id TEXT,
                    metadata TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT,
                    conversation_id TEXT,
                    relevance FLOAT
                )
            """)

    def add_memory(self, role: str, content: str, conversation_id: str, 
                   metadata: Dict = None) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO conversations (timestamp, role, content, conversation_id, metadata) VALUES (?, ?, ?, ?, ?)",
                (datetime.now().isoformat(), role, content, conversation_id, 
                 json.dumps(metadata or {}))
            )
            
            # Indexation simple des mots-clés
            keywords = set(content.lower().split())
            for keyword in keywords:
                if len(keyword) > 3:  # Ignorer les mots trop courts
                    conn.execute(
                        "INSERT INTO memory_index (keyword, conversation_id, relevance) VALUES (?, ?, ?)",
                        (keyword, conversation_id, 1.0)
                    )

    def get_relevant_memories(self, query: str, limit: int = 5) -> List[Dict]:
        keywords = set(query.lower().split())
        relevant_memories = []
        
        with sqlite3.connect(self.db_path) as conn:
            for keyword in keywords:
                if len(keyword) > 3:
                    cursor = conn.execute("""
                        SELECT DISTINCT c.* 
                        FROM conversations c
                        JOIN memory_index m ON c.conversation_id = m.conversation_id
                        WHERE m.keyword LIKE ?
                        ORDER BY c.timestamp DESC
                        LIMIT ?
                    """, (f"%{keyword}%", limit))
                    
                    for row in cursor:
                        memory = {
                            'timestamp': row[1],
                            'role': row[2],
                            'content': row[3],
                            'conversation_id': row[4],
                            'metadata': json.loads(row[5])
                        }
                        if memory not in relevant_memories:
                            relevant_memories.append(memory)
        
        return relevant_memories[:limit]

    def get_conversation_context(self, conversation_id: str, 
                               limit: int = 5) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM conversations 
                WHERE conversation_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (conversation_id, limit))
            
            return [{
                'timestamp': row[1],
                'role': row[2],
                'content': row[3],
                'conversation_id': row[4],
                'metadata': json.loads(row[5])
            } for row in cursor.fetchall()]