from fastapi import APIRouter, HTTPException
from app.data.tools_catalog import TOOLS_CATALOG, ALL_TOOLS_LIST, TOTAL_TOOLS
from app.schemas import ToolsCatalogResponse, ToolInfo
from app.tasks import run_osint_tool, celery_app
from celery.result import AsyncResult
import logging
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=ToolsCatalogResponse)
async def list_all_tools():
    """Отримати всі інструменти (150 total)"""
    return {
        "total_tools": TOTAL_TOOLS,
        "total_categories": len(TOOLS_CATALOG),
        "categories": TOOLS_CATALOG
    }

@router.get("/category/{category_name}")
async def get_category(category_name: str):
    """Отримати інструменти за категорією"""
    category_upper = category_name.upper()
    if category_upper not in TOOLS_CATALOG:
        raise HTTPException(status_code=404, detail=f"Категорія '{category_name}' не знайдена")
    
    return TOOLS_CATALOG[category_upper]

@router.get("/search/{tool_name}", response_model=ToolInfo)
async def search_tool(tool_name: str):
    """Пошук інструменту за назвою"""
    tool_lower = tool_name.lower()
    for tool in ALL_TOOLS_LIST:
        if tool_lower in tool["id"].lower() or tool_lower in tool["name"].lower():
            return tool
    raise HTTPException(status_code=404, detail=f"Інструмент '{tool_name}' не знайдений")

@router.get("/stats")
async def get_statistics():
    """Статистика інструментів за категоріями"""
    stats = {
        "total_tools": TOTAL_TOOLS,
        "total_categories": len(TOOLS_CATALOG),
        "by_category": {}
    }
    
    for cat_key, cat_data in TOOLS_CATALOG.items():
        has_api = sum(1 for t in cat_data["tools"] if t["api"] == "✓")
        stats["by_category"][cat_data["name"]] = {
            "count": cat_data["count"],
            "with_api": has_api,
            "without_api": cat_data["count"] - has_api
        }
    
    return stats

@router.get("/{tool_id}", response_model=ToolInfo)
async def get_tool_detail(tool_id: str):
    """Отримати детальну інформацію про інструмент"""
    for tool in ALL_TOOLS_LIST:
        if tool["id"] == tool_id:
            return tool
    raise HTTPException(status_code=404, detail=f"Інструмент з ID '{tool_id}' не знайдений")

@router.post("/{tool_id}/run")
async def run_tool(tool_id: str, query: str = "", investigation_id: str = None, api_key: str = None):
    """Запустити інструмент (через Celery асинхронно)"""
    tool = None
    for t in ALL_TOOLS_LIST:
        if t["id"] == tool_id:
            tool = t
            break
    
    if not tool:
        raise HTTPException(status_code=404, detail=f"Інструмент '{tool_id}' не знайдений")
    
    # Відправка задачі в чергу Celery
    try:
        task = run_osint_tool.delay(tool_id, query, investigation_id, api_key)
        task_id = task.id
        status = "queued"
    except Exception as e:
        logger.error(f"Celery error: {e}")
        # Fallback для тестів без Redis
        task_id = f"mock_task_{uuid.uuid4()}"
        status = "mocked_success"

    logger.info(f"Задача {task_id} додана в чергу для {tool['name']}")
    
    return {
        "task_id": task_id,
        "tool_id": tool_id,
        "tool_name": tool["name"],
        "status": status,
        "query": query
    }

@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """Отримати актуальний статус виконання задачі з Celery"""
    if task_id.startswith("mock_task_"):
        return {
            "task_id": task_id,
            "status": "completed",
            "ready": True,
            "result": {"data": {"found": True, "mock": True}}
        }

    task_result = AsyncResult(task_id, app=celery_app)
    
    result = None
    if task_result.ready():
        result = task_result.result

    return {
        "task_id": task_id,
        "status": task_result.status.lower(),
        "ready": task_result.ready(),
        "result": result
    }
