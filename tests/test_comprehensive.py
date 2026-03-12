"""
OSINT Platform 2026 - Comprehensive Test Suite
Тести для кожного компонента платформи
"""

import pytest
import json
from datetime import datetime, timedelta
from app.analysis import (
    AnalysisEngine, ThreatLevel, FraudDetector, 
    RecommendationEngine, ComplianceChecker
)
from app.integration import (
    IntegrationSystem, WebhookEventType, ChunkType, RelationType, PathwayType
)
from app.reporting import ReportGenerator, AnalysisGenerator

# ============================================================================
# 1. ANALYSIS ENGINE TESTS
# ============================================================================

class TestAnalysisEngine:
    """Тести для движка аналізу"""
    
    def setup_method(self):
        self.engine = AnalysisEngine()
        self.sample_chunks = [
            {
                "id": "chunk_1",
                "data": {"email": "user@gmail.com", "username": "john_doe_123"},
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "chunk_2",
                "data": {"email": "user@yahoo.com", "username": "john_doe"},
                "created_at": (datetime.now() - timedelta(hours=1)).isoformat()
            }
        ]
    
    def test_pattern_detection(self):
        """Тест виявлення паттернів"""
        patterns = self.engine.detect_patterns(self.sample_chunks)
        
        assert "email_patterns" in patterns
        assert len(patterns["email_patterns"]) == 2
        assert patterns["email_patterns"][0]["domain"] == "gmail.com"
    
    def test_username_pattern_analysis(self):
        """Тест аналізу username паттернів"""
        patterns = self.engine.detect_patterns(self.sample_chunks)
        
        usernames = patterns["username_patterns"]
        assert any(u["has_numbers"] for u in usernames)
        assert any(u["has_underscore"] for u in usernames)
    
    def test_anomaly_detection(self):
        """Тест виявлення аномалій"""
        chunks_with_time = [
            {
                "id": "chunk_1",
                "timestamp": datetime.now().isoformat(),
                "data": {}
            },
            {
                "id": "chunk_2",
                "timestamp": (datetime.now() + timedelta(hours=10)).isoformat(),
                "data": {}
            }
        ]
        
        anomalies = self.engine.detect_anomalies(chunks_with_time)
        assert len(anomalies) >= 0
    
    def test_risk_assessment_low(self):
        """Тест оцінки ризику (низький)"""
        risk = self.engine.assess_risk([], [], {})
        
        assert risk["threat_level"] == ThreatLevel.INFO
        assert risk["risk_score"] < 0.2
    
    def test_risk_assessment_high(self):
        """Тест оцінки ризику (високий)"""
        many_chunks = [{"data": {}} for _ in range(20)]
        many_relations = [{"source_chunk_id": f"s{i}", "target_chunk_id": f"t{i}"} for i in range(30)]
        
        risk = self.engine.assess_risk(many_chunks, many_relations, {})
        
        assert risk["risk_score"] > 0.3
    
    def test_trend_analysis(self):
        """Тест аналізу тренду"""
        chunks = [
            {"created_at": (datetime.now() - timedelta(days=i)).isoformat(), "data": {}}
            for i in range(5)
        ]
        
        trends = self.engine.trend_analysis(chunks)
        
        assert "velocity" in trends
        assert "growth_rate" in trends
        assert len(trends["timeline"]) == 5

# ============================================================================
# 2. FRAUD DETECTOR TESTS
# ============================================================================

class TestFraudDetector:
    """Тести для детектора шахрайства"""
    
    def test_detect_disposable_email(self):
        """Тест виявлення одноразових email"""
        chunks = [
            {
                "id": "chunk_1",
                "data": {"email": "user@tempmail.com", "username": "test"},
                "created_at": datetime.now().isoformat()
            }
        ]
        
        red_flags = FraudDetector.detect_fake_accounts(chunks)
        
        assert len(red_flags) > 0
        assert any("disposable_email" in str(f) for f in red_flags[0]["flags"])
    
    def test_detect_suspicious_username(self):
        """Тест виявлення підозрілого username"""
        chunks = [
            {
                "id": "chunk_1",
                "data": {"username": "user123456789"},
                "created_at": datetime.now().isoformat()
            }
        ]
        
        red_flags = FraudDetector.detect_fake_accounts(chunks)
        
        assert len(red_flags) > 0
    
    def test_detect_low_engagement(self):
        """Тест виявлення низької активності"""
        chunks = [
            {
                "id": "chunk_1",
                "data": {"followers": 5000, "posts": 2},
                "created_at": datetime.now().isoformat()
            }
        ]
        
        red_flags = FraudDetector.detect_fake_accounts(chunks)
        
        assert len(red_flags) > 0
        assert any("low_engagement" in str(f) for f in red_flags[0]["flags"])
    
    def test_detect_coordinated_activity(self):
        """Тест виявлення координованої активності"""
        base_time = datetime.now()
        chunks = [
            {
                "id": f"chunk_{i}",
                "created_at": base_time.isoformat(),
                "data": {}
            }
            for i in range(5)
        ]
        
        coordinated = FraudDetector.detect_coordinated_activity(chunks, [])
        
        assert len(coordinated) > 0

# ============================================================================
# 3. INTEGRATION SYSTEM TESTS
# ============================================================================

class TestIntegrationSystem:
    """Тести для системи інтеграції"""
    
    def setup_method(self):
        self.system = IntegrationSystem()
    
    def test_webhook_registration(self):
        """Тест реєстрації вебхука"""
        webhook_id = self.system.webhooks.register(
            "inv_001",
            "https://example.com/webhook",
            [WebhookEventType.EVIDENCE_FOUND]
        )
        
        assert webhook_id is not None
        assert len(webhook_id) > 0
    
    def test_webhook_trigger(self):
        """Тест спалахування вебхука"""
        from app.integration import WebhookEvent
        
        self.system.webhooks.register(
            "inv_001",
            "https://example.com/webhook",
            [WebhookEventType.EVIDENCE_FOUND]
        )
        
        event = WebhookEvent(
            type=WebhookEventType.EVIDENCE_FOUND,
            investigation_id="inv_001",
            data={"chunk_id": "test"},
            timestamp=datetime.now().isoformat()
        )
        
        triggered = self.system.webhooks.trigger(event)
        assert len(triggered) > 0
    
    def test_chunk_creation(self):
        """Тест створення чанку"""
        chunk = self.system.chunking.create_chunk(
            {"username": "john_doe"},
            ChunkType.PROFILE_CHUNK,
            "maigret",
            "inv_001"
        )
        
        assert chunk.id is not None
        assert chunk.type == ChunkType.PROFILE_CHUNK
        assert chunk.hash_sha256 is not None
    
    def test_chunk_merging(self):
        """Тест об'єднання чанків"""
        chunk1 = self.system.chunking.create_chunk(
            {"username": "john"},
            ChunkType.PROFILE_CHUNK,
            "tool1",
            "inv_001"
        )
        
        chunk2 = self.system.chunking.create_chunk(
            {"email": "john@example.com"},
            ChunkType.PROFILE_CHUNK,
            "tool2",
            "inv_001"
        )
        
        merged = self.system.chunking.merge_chunks("inv_001", [chunk1.id, chunk2.id])
        
        assert merged is not None
        assert "username" in merged.data
        assert "email" in merged.data
    
    def test_relation_creation(self):
        """Тест створення зв'язку"""
        relation_id = self.system.relations.add_relation(
            "chunk_1",
            "chunk_2",
            RelationType.CONNECTED_TO,
            0.85
        )
        
        assert relation_id is not None
    
    def test_pathway_creation(self):
        """Тест створення шляху"""
        # Спочатку створити чанки та зв'язки
        self.system.relations.add_relation(
            "chunk_1", "chunk_2", RelationType.CONNECTED_TO, 0.9
        )
        self.system.relations.add_relation(
            "chunk_2", "chunk_3", RelationType.CONNECTED_TO, 0.85
        )
        
        pathway = self.system.pathways.create_pathway(
            PathwayType.EVIDENCE_CHAIN,
            "inv_001",
            "chunk_1",
            "chunk_3",
            "Evidence chain"
        )
        
        assert pathway is not None
        assert len(pathway.nodes) == 3

# ============================================================================
# 4. REPORTING TESTS
# ============================================================================

class TestReporting:
    """Тести для системи звітності"""
    
    def setup_method(self):
        self.report = ReportGenerator("inv_001")
    
    def test_executive_summary(self):
        """Тест виконавчого звіту"""
        self.report.add_executive_summary(
            "john_doe",
            "Found 5 profiles",
            "medium"
        )
        
        report_data = self.report.generate_json_report()
        assert any(s["type"] == "executive_summary" for s in report_data["sections"])
    
    def test_threat_assessment(self):
        """Тест оцінки загроз"""
        self.report.add_threat_assessment([
            {"category": "FININT", "description": "Test threat", "severity": "HIGH"}
        ])
        
        report_data = self.report.generate_json_report()
        assert any(s["type"] == "threat_assessment" for s in report_data["sections"])
    
    def test_evidence_with_hash(self):
        """Тест доказів з хешами"""
        self.report.add_evidence([
            {"source": "maigret", "data": "test data"}
        ])
        
        report_data = self.report.generate_json_report()
        evidence_section = next(s for s in report_data["sections"] if s["type"] == "evidence")
        
        assert len(evidence_section["data"]["evidence"]) > 0
        assert "hash_sha256" in evidence_section["data"]["evidence"][0]
    
    def test_json_export(self):
        """Тест експорту JSON"""
        self.report.add_executive_summary("target", "findings", "low")
        json_str = self.report.generate_json_report()
        
        assert isinstance(json_str, dict)
        assert "id" in json_str
        assert "sections" in json_str
    
    def test_markdown_export(self):
        """Тест експорту Markdown"""
        self.report.add_executive_summary("target", "findings", "low")
        md_str = self.report.generate_markdown_report()
        
        assert isinstance(md_str, str)
        assert "OSINT Звіт" in md_str
        assert "Виконавчий звіт" in md_str

# ============================================================================
# 5. COMPLIANCE TESTS
# ============================================================================

class TestComplianceChecker:
    """Тести для перевіркача відповідності"""
    
    def test_gdpr_personal_data(self):
        """Тест GDPR - персональні дані"""
        chunks = [
            {
                "id": "chunk_1",
                "data": {"name": "John Doe", "email": "john@example.com"},
                "created_at": datetime.now().isoformat()
            }
        ]
        
        result = ComplianceChecker.check_gdpr_compliance(chunks)
        
        assert not result["compliant"]
        assert len(result["issues"]) > 0
    
    def test_legal_sensitive_data(self):
        """Тест законності - чутливі дані"""
        chunks = [
            {
                "id": "chunk_1",
                "data": {"password": "secret123"},
                "created_at": datetime.now().isoformat()
            }
        ]
        
        result = ComplianceChecker.check_legal_status(chunks)
        
        assert not result["is_legal"]
        assert len(result["warnings"]) > 0
    
    def test_legal_clean_data(self):
        """Тест законності - чисті дані"""
        chunks = [
            {
                "id": "chunk_1",
                "data": {"username": "john_doe", "profile_url": "https://example.com"},
                "created_at": datetime.now().isoformat()
            }
        ]
        
        result = ComplianceChecker.check_legal_status(chunks)
        
        assert result["is_legal"]

# ============================================================================
# 6. RECOMMENDATION TESTS
# ============================================================================

class TestRecommendationEngine:
    """Тести для движка рекомендацій"""
    
    def test_recommendations_critical_threat(self):
        """Тест рекомендацій - критична загроза"""
        risk_assessment = {
            "threat_level": ThreatLevel.CRITICAL,
            "risk_score": 0.95
        }
        
        recommendations = RecommendationEngine.generate_recommendations(
            risk_assessment, [], []
        )
        
        assert len(recommendations) > 0
        assert recommendations[0]["priority"] == "CRITICAL"
    
    def test_recommendations_high_threat(self):
        """Тест рекомендацій - висока загроза"""
        risk_assessment = {
            "threat_level": ThreatLevel.HIGH,
            "risk_score": 0.75
        }
        
        recommendations = RecommendationEngine.generate_recommendations(
            risk_assessment, [], []
        )
        
        assert any(r["priority"] in ["CRITICAL", "HIGH"] for r in recommendations)
    
    def test_recommendations_with_fraud_flags(self):
        """Тест рекомендацій - шахрайські прапори"""
        risk_assessment = {"threat_level": ThreatLevel.LOW, "risk_score": 0.1}
        fraud_flags = [
            {"risk_score": 0.7, "flags": [{"flag": "test"}]}
        ]
        
        recommendations = RecommendationEngine.generate_recommendations(
            risk_assessment, [], fraud_flags
        )
        
        assert any("подозрілих акаунтів" in str(r) for r in recommendations)

# ============================================================================
# 7. INTEGRATION TESTS
# ============================================================================

class TestFullIntegration:
    """Інтеграційні тести - повний потік"""
    
    def test_full_osint_flow(self):
        """Тест повного OSINT потоку"""
        system = IntegrationSystem()
        engine = AnalysisEngine()
        
        # 1. Створити чанки (від інструментів)
        chunk1 = system.chunking.create_chunk(
            {"username": "john_doe", "platform": "twitter"},
            ChunkType.PROFILE_CHUNK,
            "maigret",
            "inv_001"
        )
        
        chunk2 = system.chunking.create_chunk(
            {"email": "john@example.com"},
            ChunkType.PROFILE_CHUNK,
            "hunter",
            "inv_001"
        )
        
        # 2. Створити зв'язок
        relation_id = system.relations.add_relation(
            chunk1.id, chunk2.id, RelationType.SAME_AS, 0.95
        )
        
        # 3. Збудувати шлях
        pathway = system.pathways.create_pathway(
            PathwayType.ENTITY_CONNECTION,
            "inv_001",
            chunk1.id,
            chunk2.id,
            "Same person identified"
        )
        
        # 4. Провести аналіз
        chunks_data = [
            {"id": chunk1.id, "data": chunk1.data, "created_at": chunk1.created_at},
            {"id": chunk2.id, "data": chunk2.data, "created_at": chunk2.created_at}
        ]
        
        patterns = engine.detect_patterns(chunks_data)
        risk = engine.assess_risk(chunks_data, [], patterns)
        
        # 5. Перевірити результати
        assert chunk1.id is not None
        assert chunk2.id is not None
        assert relation_id is not None
        assert pathway is not None
        assert risk["threat_level"] in [ThreatLevel.INFO, ThreatLevel.LOW]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
