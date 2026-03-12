"""
OSINT Platform 2026 - Webhooks, Chunking, Relations & Pathways System
Система вебхуків, розбиття на чанки, релацій та маршрутів зєднання
"""

from enum import Enum
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import json
import hashlib
import asyncio
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# 1. WEBHOOK SYSTEM
# ============================================================================

class WebhookEventType(str, Enum):
    """Типи подій для вебхуків"""
    INVESTIGATION_CREATED = "investigation.created"
    INVESTIGATION_COMPLETED = "investigation.completed"
    EVIDENCE_FOUND = "evidence.found"
    THREAT_DETECTED = "threat.detected"
    REPORT_GENERATED = "report.generated"
    TOOL_EXECUTED = "tool.executed"
    ANALYSIS_COMPLETED = "analysis.completed"

@dataclass
class WebhookEvent:
    """Подія вебхука"""
    type: WebhookEventType
    investigation_id: str
    data: Dict[str, Any]
    timestamp: str
    id: str = None
    
    def __post_init__(self):
        if not self.id:
            self.id = hashlib.sha256(
                json.dumps({
                    "type": self.type,
                    "investigation_id": self.investigation_id,
                    "timestamp": self.timestamp
                }).encode()
            ).hexdigest()[:16]

class WebhookRegistry:
    """Реєстр вебхуків для розслідування"""
    
    def __init__(self):
        self.webhooks: Dict[str, List[Dict]] = {}
        self.event_history: List[WebhookEvent] = []
    
    def register(self, investigation_id: str, url: str, events: List[WebhookEventType]) -> str:
        """Зареєструвати вебхук"""
        webhook_id = hashlib.sha256(f"{investigation_id}{url}{datetime.now()}".encode()).hexdigest()[:16]
        
        if investigation_id not in self.webhooks:
            self.webhooks[investigation_id] = []
        
        self.webhooks[investigation_id].append({
            "id": webhook_id,
            "url": url,
            "events": events,
            "created_at": datetime.now().isoformat(),
            "active": True
        })
        
        logger.info(f"Webhook зареєстрований: {webhook_id} для {investigation_id}")
        return webhook_id
    
    def trigger(self, event: WebhookEvent) -> List[str]:
        """Спалахнути подію для всіх вебхуків"""
        triggered_ids = []
        
        if event.investigation_id not in self.webhooks:
            return triggered_ids
        
        for webhook in self.webhooks[event.investigation_id]:
            if not webhook["active"]:
                continue
            
            if event.type in webhook["events"]:
                # Тут можна додати фактичну відправку HTTP запиту
                triggered_ids.append(webhook["id"])
                logger.info(f"Webhook спалахнув: {webhook['url']} для {event.type}")
        
        self.event_history.append(event)
        return triggered_ids
    
    def list_webhooks(self, investigation_id: str) -> List[Dict]:
        """Отримати всі вебхуки розслідування"""
        return self.webhooks.get(investigation_id, [])
    
    def disable_webhook(self, investigation_id: str, webhook_id: str) -> bool:
        """Деактивувати вебхук"""
        if investigation_id in self.webhooks:
            for webhook in self.webhooks[investigation_id]:
                if webhook["id"] == webhook_id:
                    webhook["active"] = False
                    return True
        return False

# ============================================================================
# 2. CHUNKING SYSTEM
# ============================================================================

class ChunkType(str, Enum):
    """Типи чанків даних"""
    PROFILE_CHUNK = "profile"
    INFRASTRUCTURE_CHUNK = "infrastructure"
    LOCATION_CHUNK = "location"
    FINANCIAL_CHUNK = "financial"
    THREAT_CHUNK = "threat"
    EVIDENCE_CHUNK = "evidence"
    RELATIONSHIP_CHUNK = "relationship"

@dataclass
class DataChunk:
    """Чанк даних"""
    id: str
    type: ChunkType
    data: Dict[str, Any]
    source_tool: str
    investigation_id: str
    created_at: str
    hash_sha256: str
    size_bytes: int
    parent_chunk_id: Optional[str] = None
    
    @staticmethod
    def from_data(
        data: Dict[str, Any],
        chunk_type: ChunkType,
        source_tool: str,
        investigation_id: str,
        parent_chunk_id: Optional[str] = None
    ) -> 'DataChunk':
        """Створити чанк з даних"""
        data_str = json.dumps(data, sort_keys=True)
        chunk_hash = hashlib.sha256(data_str.encode()).hexdigest()
        
        chunk_id = hashlib.sha256(
            f"{investigation_id}{chunk_type}{source_tool}{datetime.now()}".encode()
        ).hexdigest()[:16]
        
        return DataChunk(
            id=chunk_id,
            type=chunk_type,
            data=data,
            source_tool=source_tool,
            investigation_id=investigation_id,
            created_at=datetime.now().isoformat(),
            hash_sha256=chunk_hash,
            size_bytes=len(data_str.encode()),
            parent_chunk_id=parent_chunk_id
        )

class ChunkingSystem:
    """Система розбиття даних на чанки"""
    
    def __init__(self):
        self.chunks: Dict[str, List[DataChunk]] = {}
        self.chunk_index: Dict[str, DataChunk] = {}
    
    def create_chunk(
        self,
        data: Dict[str, Any],
        chunk_type: ChunkType,
        source_tool: str,
        investigation_id: str,
        parent_chunk_id: Optional[str] = None
    ) -> DataChunk:
        """Створити та зберегти чанк"""
        chunk = DataChunk.from_data(
            data, chunk_type, source_tool, investigation_id, parent_chunk_id
        )
        
        if investigation_id not in self.chunks:
            self.chunks[investigation_id] = []
        
        self.chunks[investigation_id].append(chunk)
        self.chunk_index[chunk.id] = chunk
        
        logger.info(f"Чанк створений: {chunk.id} ({chunk_type})")
        return chunk
    
    def get_chunks(
        self,
        investigation_id: str,
        chunk_type: Optional[ChunkType] = None
    ) -> List[DataChunk]:
        """Отримати чанки розслідування"""
        chunks = self.chunks.get(investigation_id, [])
        
        if chunk_type:
            chunks = [c for c in chunks if c.type == chunk_type]
        
        return chunks
    
    def get_chunk_tree(self, investigation_id: str, root_chunk_id: str) -> Dict:
        """Отримати дерево чанків"""
        root_chunk = self.chunk_index.get(root_chunk_id)
        if not root_chunk:
            return {}
        
        children = [
            c for c in self.chunks.get(investigation_id, [])
            if c.parent_chunk_id == root_chunk_id
        ]
        
        return {
            "chunk": asdict(root_chunk),
            "children": [
                self.get_chunk_tree(investigation_id, c.id)
                for c in children
            ]
        }
    
    def merge_chunks(
        self,
        investigation_id: str,
        chunk_ids: List[str]
    ) -> Optional[DataChunk]:
        """Об'єднати кілька чанків"""
        chunks = [self.chunk_index.get(cid) for cid in chunk_ids if cid in self.chunk_index]
        
        if not chunks:
            return None
        
        merged_data = {}
        for chunk in chunks:
            merged_data.update(chunk.data)
        
        new_chunk = DataChunk.from_data(
            merged_data,
            ChunkType.EVIDENCE_CHUNK,
            "merged",
            investigation_id,
            parent_chunk_id=chunks[0].id
        )
        
        if investigation_id not in self.chunks:
            self.chunks[investigation_id] = []
        
        self.chunks[investigation_id].append(new_chunk)
        self.chunk_index[new_chunk.id] = new_chunk
        
        return new_chunk

# ============================================================================
# 3. RELATION SYSTEM (Зв'язки даних)
# ============================================================================

class RelationType(str, Enum):
    """Типи зв'язків між даними"""
    OWNS = "owns"  # Власність
    WORKS_FOR = "works_for"  # Працює для
    LOCATED_IN = "located_in"  # Розташований у
    REGISTERED_ON = "registered_on"  # Зареєстрований на
    CONNECTED_TO = "connected_to"  # Пов'язано з
    MENTIONS = "mentions"  # Згадує
    FOLLOWS = "follows"  # Стежить за
    FRIENDS_WITH = "friends_with"  # Друзі з
    SAME_AS = "same_as"  # Те саме, що
    RELATED_TO = "related_to"  # Пов'язано з

@dataclass
class Relation:
    """Зв'язок між двома сутностями"""
    id: str
    source_chunk_id: str
    target_chunk_id: str
    relation_type: RelationType
    weight: float  # 0.0 - 1.0 впевненість
    metadata: Dict[str, Any]
    created_at: str
    verified: bool = False

class RelationGraph:
    """Граф зв'язків даних"""
    
    def __init__(self):
        self.relations: Dict[str, Relation] = {}
        self.adjacency_list: Dict[str, List[str]] = {}
    
    def add_relation(
        self,
        source_chunk_id: str,
        target_chunk_id: str,
        relation_type: RelationType,
        weight: float = 0.8,
        metadata: Optional[Dict] = None
    ) -> str:
        """Додати зв'язок"""
        relation_id = hashlib.sha256(
            f"{source_chunk_id}{target_chunk_id}{relation_type}{datetime.now()}".encode()
        ).hexdigest()[:16]
        
        relation = Relation(
            id=relation_id,
            source_chunk_id=source_chunk_id,
            target_chunk_id=target_chunk_id,
            relation_type=relation_type,
            weight=weight,
            metadata=metadata or {},
            created_at=datetime.now().isoformat()
        )
        
        self.relations[relation_id] = relation
        
        if source_chunk_id not in self.adjacency_list:
            self.adjacency_list[source_chunk_id] = []
        self.adjacency_list[source_chunk_id].append(relation_id)
        
        logger.info(f"Зв'язок додано: {source_chunk_id} -> {target_chunk_id} ({relation_type})")
        return relation_id
    
    def find_path(self, start_chunk_id: str, end_chunk_id: str) -> List[str]:
        """Знайти шлях між двома чанками (BFS)"""
        if start_chunk_id not in self.adjacency_list:
            return []
        
        visited = set()
        queue = [(start_chunk_id, [start_chunk_id])]
        
        while queue:
            current, path = queue.pop(0)
            
            if current == end_chunk_id:
                return path
            
            if current in visited:
                continue
            visited.add(current)
            
            for relation_id in self.adjacency_list.get(current, []):
                relation = self.relations[relation_id]
                next_chunk = relation.target_chunk_id
                
                if next_chunk not in visited:
                    queue.append((next_chunk, path + [next_chunk]))
        
        return []
    
    def get_connected_components(self) -> List[List[str]]:
        """Отримати пов'язані компоненти"""
        visited = set()
        components = []
        
        for chunk_id in self.adjacency_list:
            if chunk_id not in visited:
                component = []
                stack = [chunk_id]
                
                while stack:
                    current = stack.pop()
                    if current in visited:
                        continue
                    
                    visited.add(current)
                    component.append(current)
                    
                    for relation_id in self.adjacency_list.get(current, []):
                        relation = self.relations[relation_id]
                        if relation.target_chunk_id not in visited:
                            stack.append(relation.target_chunk_id)
                
                components.append(component)
        
        return components
    
    def get_entity_network(self, entity_chunk_id: str, depth: int = 2) -> Dict:
        """Отримати мережу сутностей з глибиною"""
        network = {
            "root": entity_chunk_id,
            "depth": depth,
            "nodes": {entity_chunk_id: {"type": "entity"}},
            "edges": []
        }
        
        current_level = [entity_chunk_id]
        
        for _ in range(depth):
            next_level = set()
            
            for chunk_id in current_level:
                for relation_id in self.adjacency_list.get(chunk_id, []):
                    relation = self.relations[relation_id]
                    target_id = relation.target_chunk_id
                    
                    if target_id not in network["nodes"]:
                        network["nodes"][target_id] = {"type": "connected"}
                        next_level.add(target_id)
                    
                    network["edges"].append({
                        "source": chunk_id,
                        "target": target_id,
                        "type": relation.relation_type,
                        "weight": relation.weight
                    })
            
            current_level = list(next_level)
        
        return network

# ============================================================================
# 4. PATHWAY SYSTEM (Шляхи зєднань)
# ============================================================================

class PathwayType(str, Enum):
    """Типи шляхів зєднання"""
    INVESTIGATION_FLOW = "investigation_flow"  # Потік розслідування
    DATA_FLOW = "data_flow"  # Потік даних
    EVIDENCE_CHAIN = "evidence_chain"  # Ланцюг доказів
    THREAT_PATH = "threat_path"  # Шлях загрози
    ENTITY_CONNECTION = "entity_connection"  # Зв'язок сутностей

@dataclass
class Pathway:
    """Шлях зєднання компонентів"""
    id: str
    type: PathwayType
    investigation_id: str
    nodes: List[str]  # IDs чанків/елементів
    connections: List[Relation]
    description: str
    created_at: str
    strength: float  # 0.0 - 1.0

class PathwaySystem:
    """Система шляхів зєднань"""
    
    def __init__(self, relation_graph: RelationGraph):
        self.relation_graph = relation_graph
        self.pathways: Dict[str, Pathway] = {}
    
    def create_pathway(
        self,
        pathway_type: PathwayType,
        investigation_id: str,
        start_node: str,
        end_node: str,
        description: str
    ) -> Optional[Pathway]:
        """Створити шлях зєднання"""
        path = self.relation_graph.find_path(start_node, end_node)
        
        if not path:
            logger.warning(f"Шлях не знайдено: {start_node} -> {end_node}")
            return None
        
        connections = []
        total_weight = 0.0
        
        for i in range(len(path) - 1):
            for relation_id in self.relation_graph.adjacency_list.get(path[i], []):
                relation = self.relation_graph.relations[relation_id]
                if relation.target_chunk_id == path[i + 1]:
                    connections.append(relation)
                    total_weight += relation.weight
        
        avg_strength = total_weight / len(connections) if connections else 0.0
        
        pathway_id = hashlib.sha256(
            f"{investigation_id}{start_node}{end_node}{datetime.now()}".encode()
        ).hexdigest()[:16]
        
        pathway = Pathway(
            id=pathway_id,
            type=pathway_type,
            investigation_id=investigation_id,
            nodes=path,
            connections=connections,
            description=description,
            created_at=datetime.now().isoformat(),
            strength=avg_strength
        )
        
        self.pathways[pathway_id] = pathway
        logger.info(f"Шлях створено: {pathway_id} ({len(path)} нодів)")
        return pathway
    
    def get_investigation_pathways(self, investigation_id: str) -> List[Pathway]:
        """Отримати всі шляхи розслідування"""
        return [
            p for p in self.pathways.values()
            if p.investigation_id == investigation_id
        ]
    
    def get_strongest_pathways(
        self,
        investigation_id: str,
        limit: int = 5
    ) -> List[Pathway]:
        """Отримати найсильніші шляхи"""
        pathways = self.get_investigation_pathways(investigation_id)
        return sorted(pathways, key=lambda p: p.strength, reverse=True)[:limit]
    
    def visualize_pathway(self, pathway_id: str) -> Dict:
        """Візуалізація шляху"""
        pathway = self.pathways.get(pathway_id)
        if not pathway:
            return {}
        
        return {
            "id": pathway.id,
            "type": pathway.type,
            "description": pathway.description,
            "strength": pathway.strength,
            "nodes": pathway.nodes,
            "connections": [
                {
                    "source": conn.source_chunk_id,
                    "target": conn.target_chunk_id,
                    "type": conn.relation_type,
                    "weight": conn.weight
                }
                for conn in pathway.connections
            ]
        }

# ============================================================================
# 5. INTEGRATION SYSTEM
# ============================================================================

class IntegrationSystem:
    """Система інтеграції всіх компонентів"""
    
    def __init__(self):
        self.webhooks = WebhookRegistry()
        self.chunking = ChunkingSystem()
        self.relations = RelationGraph()
        self.pathways = PathwaySystem(self.relations)
    
    async def process_tool_result(
        self,
        investigation_id: str,
        tool_name: str,
        result_data: Dict[str, Any]
    ):
        """Обробити результат інструменту"""
        # 1. Створити чанк
        chunk = self.chunking.create_chunk(
            result_data,
            ChunkType.EVIDENCE_CHUNK,
            tool_name,
            investigation_id
        )
        
        # 2. Спалахнути вебхук EVIDENCE_FOUND
        event = WebhookEvent(
            type=WebhookEventType.EVIDENCE_FOUND,
            investigation_id=investigation_id,
            data={"chunk_id": chunk.id, "tool": tool_name},
            timestamp=datetime.now().isoformat()
        )
        self.webhooks.trigger(event)
        
        logger.info(f"Результат {tool_name} оброблений: {chunk.id}")
        return chunk
    
    async def analyze_relations(
        self,
        investigation_id: str,
        chunk_ids: List[str]
    ):
        """Аналізувати зв'язки між чанками"""
        relations_found = []
        
        for i, chunk_id1 in enumerate(chunk_ids):
            for chunk_id2 in chunk_ids[i+1:]:
                # Тут можна додати логіку аналізу зв'язків
                # Простий приклад:
                relation_id = self.relations.add_relation(
                    chunk_id1,
                    chunk_id2,
                    RelationType.RELATED_TO,
                    weight=0.7,
                    metadata={"auto_detected": True}
                )
                relations_found.append(relation_id)
        
        logger.info(f"Знайдено {len(relations_found)} зв'язків")
        return relations_found
    
    async def build_evidence_chain(
        self,
        investigation_id: str,
        start_chunk_id: str,
        end_chunk_id: str
    ) -> Optional[Pathway]:
        """Побудувати ланцюг доказів"""
        pathway = self.pathways.create_pathway(
            PathwayType.EVIDENCE_CHAIN,
            investigation_id,
            start_chunk_id,
            end_chunk_id,
            "Ланцюг доказів"
        )
        
        if pathway:
            event = WebhookEvent(
                type=WebhookEventType.ANALYSIS_COMPLETED,
                investigation_id=investigation_id,
                data={"pathway_id": pathway.id, "strength": pathway.strength},
                timestamp=datetime.now().isoformat()
            )
            self.webhooks.trigger(event)
        
        return pathway
    
    def get_investigation_map(self, investigation_id: str) -> Dict:
        """Отримати повну карту розслідування"""
        chunks = self.chunking.get_chunks(investigation_id)
        pathways = self.pathways.get_investigation_pathways(investigation_id)
        
        return {
            "investigation_id": investigation_id,
            "chunks": {
                "total": len(chunks),
                "by_type": {
                    ct: len([c for c in chunks if c.type == ct])
                    for ct in ChunkType
                }
            },
            "relations": {
                "total": len(self.relations.relations)
            },
            "pathways": {
                "total": len(pathways),
                "by_type": {
                    pt: len([p for p in pathways if p.type == pt])
                    for pt in PathwayType
                }
            }
        }
