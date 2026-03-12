from fastapi import APIRouter, Depends, HTTPException, Query, Header, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.integration import (
    IntegrationSystem, WebhookEventType, ChunkType, 
    RelationType, PathwayType
)
import logging
from typing import List

logger = logging.getLogger(__name__)
router = APIRouter()

# Глобальна інстанція системи інтеграції
integration_system = IntegrationSystem()

# ============================================================================
# WEBHOOKS ENDPOINTS
# ============================================================================

@router.post("/{investigation_id}/webhooks/register")
async def register_webhook(
    investigation_id: str,
    url: str = Body(...),
    events: List[str] = Body(...),
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Зареєструвати вебхук"""
    try:
        event_types = [WebhookEventType(e) for e in events]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid event type: {e}")
    
    webhook_id = integration_system.webhooks.register(
        investigation_id, url, event_types
    )
    
    return {
        "webhook_id": webhook_id,
        "investigation_id": investigation_id,
        "url": url,
        "events": events,
        "status": "active"
    }

@router.get("/{investigation_id}/webhooks")
async def list_webhooks(
    investigation_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Отримати всі вебхуки розслідування"""
    webhooks = integration_system.webhooks.list_webhooks(investigation_id)
    
    return {
        "investigation_id": investigation_id,
        "webhooks": webhooks,
        "total": len(webhooks)
    }

@router.delete("/{investigation_id}/webhooks/{webhook_id}")
async def disable_webhook(
    investigation_id: str,
    webhook_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Деактивувати вебхук"""
    success = integration_system.webhooks.disable_webhook(investigation_id, webhook_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    return {
        "status": "disabled",
        "webhook_id": webhook_id
    }

# ============================================================================
# CHUNKING ENDPOINTS
# ============================================================================

@router.post("/{investigation_id}/chunks")
async def create_chunk(
    investigation_id: str,
    chunk_type: str = Body(...),
    data: dict = Body(...),
    source_tool: str = Body(...),
    parent_chunk_id: str = Body(None),
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Створити новий чанк даних"""
    try:
        chunk_type_enum = ChunkType(chunk_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid chunk type: {chunk_type}")
    
    chunk = integration_system.chunking.create_chunk(
        data, chunk_type_enum, source_tool, investigation_id, parent_chunk_id
    )
    
    return {
        "chunk_id": chunk.id,
        "type": chunk.type,
        "size_bytes": chunk.size_bytes,
        "hash_sha256": chunk.hash_sha256,
        "created_at": chunk.created_at
    }

@router.get("/{investigation_id}/chunks")
async def get_chunks(
    investigation_id: str,
    chunk_type: str = Query(None),
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Отримати чанки розслідування"""
    chunk_type_enum = None
    if chunk_type:
        try:
            chunk_type_enum = ChunkType(chunk_type)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid chunk type: {chunk_type}")
    
    chunks = integration_system.chunking.get_chunks(investigation_id, chunk_type_enum)
    
    return {
        "investigation_id": investigation_id,
        "total": len(chunks),
        "chunks": [
            {
                "id": c.id,
                "type": c.type,
                "source_tool": c.source_tool,
                "size_bytes": c.size_bytes,
                "created_at": c.created_at
            }
            for c in chunks
        ]
    }

@router.get("/{investigation_id}/chunks/{chunk_id}/tree")
async def get_chunk_tree(
    investigation_id: str,
    chunk_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Отримати дерево чанків"""
    tree = integration_system.chunking.get_chunk_tree(investigation_id, chunk_id)
    
    if not tree:
        raise HTTPException(status_code=404, detail="Chunk not found")
    
    return tree

@router.post("/{investigation_id}/chunks/merge")
async def merge_chunks(
    investigation_id: str,
    chunk_ids: List[str] = Body(...),
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Об'єднати кілька чанків"""
    merged = integration_system.chunking.merge_chunks(investigation_id, chunk_ids)
    
    if not merged:
        raise HTTPException(status_code=400, detail="Failed to merge chunks")
    
    return {
        "merged_chunk_id": merged.id,
        "source_chunks": chunk_ids,
        "size_bytes": merged.size_bytes,
        "hash_sha256": merged.hash_sha256
    }

# ============================================================================
# RELATIONS ENDPOINTS
# ============================================================================

@router.post("/{investigation_id}/relations")
async def create_relation(
    investigation_id: str,
    source_chunk_id: str = Body(...),
    target_chunk_id: str = Body(...),
    relation_type: str = Body(...),
    weight: float = Body(0.8),
    metadata: dict = Body(None),
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Створити зв'язок між чанками"""
    try:
        relation_type_enum = RelationType(relation_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid relation type: {relation_type}")
    
    if not (0.0 <= weight <= 1.0):
        raise HTTPException(status_code=400, detail="Weight must be between 0.0 and 1.0")
    
    relation_id = integration_system.relations.add_relation(
        source_chunk_id,
        target_chunk_id,
        relation_type_enum,
        weight,
        metadata or {}
    )
    
    return {
        "relation_id": relation_id,
        "source": source_chunk_id,
        "target": target_chunk_id,
        "type": relation_type,
        "weight": weight
    }

@router.get("/{investigation_id}/relations/path")
async def find_path(
    investigation_id: str,
    start_chunk_id: str = Query(...),
    end_chunk_id: str = Query(...),
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Знайти шлях між двома чанками"""
    path = integration_system.relations.find_path(start_chunk_id, end_chunk_id)
    
    if not path:
        raise HTTPException(status_code=404, detail="No path found between chunks")
    
    return {
        "start": start_chunk_id,
        "end": end_chunk_id,
        "path": path,
        "hops": len(path) - 1
    }

@router.get("/{investigation_id}/relations/network")
async def get_entity_network(
    investigation_id: str,
    entity_chunk_id: str = Query(...),
    depth: int = Query(2),
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Отримати мережу сутностей"""
    if depth < 1 or depth > 5:
        raise HTTPException(status_code=400, detail="Depth must be between 1 and 5")
    
    network = integration_system.relations.get_entity_network(entity_chunk_id, depth)
    
    return {
        "root_entity": entity_chunk_id,
        "depth": depth,
        "nodes_count": len(network.get("nodes", {})),
        "connections_count": len(network.get("edges", [])),
        "network": network
    }

@router.get("/{investigation_id}/relations/components")
async def get_connected_components(
    investigation_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Отримати пов'язані компоненти"""
    components = integration_system.relations.get_connected_components()
    
    return {
        "investigation_id": investigation_id,
        "components_count": len(components),
        "components": [
            {
                "id": i,
                "nodes": comp,
                "size": len(comp)
            }
            for i, comp in enumerate(components)
        ]
    }

# ============================================================================
# PATHWAYS ENDPOINTS
# ============================================================================

@router.post("/{investigation_id}/pathways")
async def create_pathway(
    investigation_id: str,
    pathway_type: str = Body(...),
    start_node: str = Body(...),
    end_node: str = Body(...),
    description: str = Body(...),
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Створити шлях зєднання"""
    try:
        pathway_type_enum = PathwayType(pathway_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid pathway type: {pathway_type}")
    
    pathway = integration_system.pathways.create_pathway(
        pathway_type_enum,
        investigation_id,
        start_node,
        end_node,
        description
    )
    
    if not pathway:
        raise HTTPException(status_code=404, detail="Could not create pathway")
    
    return {
        "pathway_id": pathway.id,
        "type": pathway.type,
        "nodes_count": len(pathway.nodes),
        "strength": pathway.strength,
        "description": description
    }

@router.get("/{investigation_id}/pathways")
async def get_pathways(
    investigation_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Отримати всі шляхи розслідування"""
    pathways = integration_system.pathways.get_investigation_pathways(investigation_id)
    
    return {
        "investigation_id": investigation_id,
        "total": len(pathways),
        "pathways": [
            {
                "id": p.id,
                "type": p.type,
                "nodes": len(p.nodes),
                "strength": p.strength,
                "description": p.description
            }
            for p in pathways
        ]
    }

@router.get("/{investigation_id}/pathways/strongest")
async def get_strongest_pathways(
    investigation_id: str,
    limit: int = Query(5),
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Отримати найсильніші шляхи"""
    if limit < 1 or limit > 20:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 20")
    
    pathways = integration_system.pathways.get_strongest_pathways(investigation_id, limit)
    
    return {
        "investigation_id": investigation_id,
        "total": len(pathways),
        "pathways": [
            {
                "id": p.id,
                "type": p.type,
                "strength": p.strength,
                "nodes": len(p.nodes)
            }
            for p in pathways
        ]
    }

@router.get("/{investigation_id}/pathways/{pathway_id}/visualize")
async def visualize_pathway(
    investigation_id: str,
    pathway_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Візуалізація шляху"""
    visualization = integration_system.pathways.visualize_pathway(pathway_id)
    
    if not visualization:
        raise HTTPException(status_code=404, detail="Pathway not found")
    
    return visualization

# ============================================================================
# INVESTIGATION MAP
# ============================================================================

@router.get("/{investigation_id}/map")
async def get_investigation_map(
    investigation_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Отримати повну карту розслідування"""
    investigation_map = integration_system.get_investigation_map(investigation_id)
    
    return {
        "investigation_id": investigation_id,
        "map": investigation_map,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }
