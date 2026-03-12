"""
OSINT Platform 2026 - Analysis Logic
Логіка аналізу даних для виявлення закономірностей та загроз
"""

from typing import List, Dict, Any, Tuple, Optional
from enum import Enum
import re
import hashlib
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# 1. ANALYSIS ENGINE
# ============================================================================

class ThreatLevel(str, Enum):
    """Рівні загроз"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class AnalysisType(str, Enum):
    """Типи аналізу"""
    PATTERN_DETECTION = "pattern_detection"
    ANOMALY_DETECTION = "anomaly_detection"
    RELATIONSHIP_ANALYSIS = "relationship_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    TREND_ANALYSIS = "trend_analysis"

class AnalysisEngine:
    """Основний двигун аналізу"""
    
    def __init__(self):
        self.analysis_results = {}
        self.confidence_threshold = 0.7
    
    def detect_patterns(self, chunks: List[Dict]) -> Dict[str, Any]:
        """Виявити закономірності в даних"""
        patterns = {
            "email_patterns": [],
            "username_patterns": [],
            "ip_patterns": [],
            "phone_patterns": [],
            "url_patterns": []
        }
        
        for chunk in chunks:
            data = chunk.get("data", {})
            
            # Email паттерни
            if "email" in data:
                email_domain = data["email"].split("@")[1] if "@" in data["email"] else None
                patterns["email_patterns"].append({
                    "email": data["email"],
                    "domain": email_domain
                })
            
            # Username паттерни
            if "username" in data:
                patterns["username_patterns"].append({
                    "username": data["username"],
                    "length": len(data["username"]),
                    "has_numbers": any(c.isdigit() for c in data["username"]),
                    "has_underscore": "_" in data["username"]
                })
            
            # IP паттерни
            if "ip" in data:
                patterns["ip_patterns"].append({
                    "ip": data["ip"],
                    "subnet": ".".join(data["ip"].split(".")[:3]) + ".0/24"
                })
            
            # Phone паттерни
            if "phone" in data:
                phone = data["phone"].replace("+", "").replace("-", "")
                patterns["phone_patterns"].append({
                    "phone": data["phone"],
                    "country_code": phone[:2] if len(phone) >= 2 else None
                })
            
            # URL паттерни
            if "url" in data:
                url = data["url"]
                patterns["url_patterns"].append({
                    "url": url,
                    "domain": url.split("/")[2] if "/" in url else url
                })
        
        logger.info(f"Знайдено паттерни: {len(patterns['email_patterns'])} email, {len(patterns['username_patterns'])} username")
        return patterns
    
    def detect_anomalies(self, chunks: List[Dict]) -> List[Dict]:
        """Виявити аномалії в даних"""
        anomalies = []
        
        # Аналіз аномалій часу
        timestamps = []
        for chunk in chunks:
            if "timestamp" in chunk:
                timestamps.append(chunk["timestamp"])
        
        if timestamps:
            time_diffs = []
            for i in range(1, len(timestamps)):
                try:
                    t1 = datetime.fromisoformat(timestamps[i-1])
                    t2 = datetime.fromisoformat(timestamps[i])
                    time_diffs.append((t2 - t1).total_seconds())
                except:
                    pass
            
            if time_diffs:
                avg_diff = sum(time_diffs) / len(time_diffs)
                for diff in time_diffs:
                    if diff > avg_diff * 2:
                        anomalies.append({
                            "type": "time_anomaly",
                            "value": diff,
                            "average": avg_diff,
                            "severity": "medium"
                        })
        
        # Аналіз географічних аномалій
        locations = [c.get("data", {}).get("location") for c in chunks if "location" in c.get("data", {})]
        if len(locations) > 1:
            for i in range(len(locations) - 1):
                # Якщо дві локації дуже близько по часу, але далеко географічно - аномалія
                anomalies.append({
                    "type": "geographic_anomaly",
                    "locations": [locations[i], locations[i+1]],
                    "severity": "high" if len(locations) > 5 else "medium"
                })
        
        logger.info(f"Виявлено {len(anomalies)} аномалій")
        return anomalies
    
    def analyze_relationships(self, relations: List[Dict]) -> Dict[str, Any]:
        """Аналізувати взаємозв'язки"""
        relationship_analysis = {
            "clusters": [],
            "key_nodes": [],
            "central_figures": [],
            "network_density": 0.0
        }
        
        if not relations:
            return relationship_analysis
        
        # Підрахунок ступенів вузлів
        node_degrees = {}
        for relation in relations:
            source = relation.get("source_chunk_id")
            target = relation.get("target_chunk_id")
            
            node_degrees[source] = node_degrees.get(source, 0) + 1
            node_degrees[target] = node_degrees.get(target, 0) + 1
        
        # Знайти центральні фігури (найвищий ступінь)
        if node_degrees:
            sorted_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)
            relationship_analysis["central_figures"] = sorted_nodes[:3]
            relationship_analysis["key_nodes"] = [n[0] for n in sorted_nodes[:5]]
            
            # Розрахувати щільність мережи
            total_nodes = len(node_degrees)
            total_edges = len(relations)
            max_edges = total_nodes * (total_nodes - 1) / 2
            relationship_analysis["network_density"] = total_edges / max_edges if max_edges > 0 else 0
        
        logger.info(f"Аналіз взаємозв'язків: {len(node_degrees)} вузлів, щільність: {relationship_analysis['network_density']:.2f}")
        return relationship_analysis
    
    def assess_risk(self, chunks: List[Dict], relations: List[Dict], patterns: Dict) -> Dict[str, Any]:
        """Оцінити ризик"""
        risk_factors = []
        total_risk_score = 0.0
        
        # Фактор 1: Кількість знахідок
        findings_factor = min(len(chunks) / 10, 1.0) * 0.2
        risk_factors.append({"factor": "findings_count", "score": findings_factor, "weight": 0.2})
        
        # Фактор 2: Кількість взаємозв'язків
        relations_factor = min(len(relations) / 20, 1.0) * 0.3
        risk_factors.append({"factor": "relations_count", "score": relations_factor, "weight": 0.3})
        
        # Фактор 3: Консистентність даних
        consistency_factor = 0.0
        if patterns.get("email_patterns"):
            domains = set([p.get("domain") for p in patterns["email_patterns"]])
            domain_consistency = 1 - (len(domains) / len(patterns["email_patterns"])) if patterns["email_patterns"] else 0
            consistency_factor = domain_consistency * 0.25
        risk_factors.append({"factor": "data_consistency", "score": consistency_factor, "weight": 0.25})
        
        # Фактор 4: Географічна аномалія
        geo_factor = 0.15 if len([c for c in chunks if "location" in c.get("data", {})]) > 2 else 0
        risk_factors.append({"factor": "geographic_anomaly", "score": geo_factor, "weight": 0.15})
        
        # Фактор 5: Временні паттерни
        time_factor = 0.1
        risk_factors.append({"factor": "temporal_pattern", "score": time_factor, "weight": 0.1})
        
        # Розрахувати загальний ризик
        for factor in risk_factors:
            total_risk_score += factor["score"] * factor["weight"]
        
        # Визначити рівень загрози
        if total_risk_score >= 0.8:
            threat_level = ThreatLevel.CRITICAL
        elif total_risk_score >= 0.6:
            threat_level = ThreatLevel.HIGH
        elif total_risk_score >= 0.4:
            threat_level = ThreatLevel.MEDIUM
        elif total_risk_score >= 0.2:
            threat_level = ThreatLevel.LOW
        else:
            threat_level = ThreatLevel.INFO
        
        return {
            "risk_score": total_risk_score,
            "threat_level": threat_level,
            "risk_factors": risk_factors,
            "confidence": min(total_risk_score + 0.2, 1.0)
        }
    
    def trend_analysis(self, chunks: List[Dict]) -> Dict[str, Any]:
        """Аналіз тренду"""
        trends = {
            "timeline": [],
            "growth_rate": 0.0,
            "velocity": "unknown"
        }
        
        # Сортувати за часом
        sorted_chunks = sorted(chunks, key=lambda c: c.get("created_at", ""))
        
        if len(sorted_chunks) > 1:
            trends["timeline"] = [c.get("created_at") for c in sorted_chunks]
            
            # Розрахувати темп росту
            time_diff = None
            try:
                t1 = datetime.fromisoformat(sorted_chunks[0].get("created_at", ""))
                t2 = datetime.fromisoformat(sorted_chunks[-1].get("created_at", ""))
                time_diff = (t2 - t1).days
            except:
                pass
            
            if time_diff and time_diff > 0:
                growth_rate = len(sorted_chunks) / time_diff
                trends["growth_rate"] = growth_rate
                
                if growth_rate > 5:
                    trends["velocity"] = "very_high"
                elif growth_rate > 2:
                    trends["velocity"] = "high"
                elif growth_rate > 1:
                    trends["velocity"] = "medium"
                else:
                    trends["velocity"] = "low"
        
        return trends

# ============================================================================
# 2. FRAUD DETECTION
# ============================================================================

class FraudDetector:
    """Детектор шахрайства"""
    
    @staticmethod
    def detect_fake_accounts(chunks: List[Dict]) -> List[Dict]:
        """Виявити фальшиві акаунти"""
        red_flags = []
        
        for chunk in chunks:
            data = chunk.get("data", {})
            flags = []
            
            # Прапор 1: Новий акаунт
            if "created_at" in data:
                try:
                    created = datetime.fromisoformat(data["created_at"])
                    if (datetime.now() - created).days < 7:
                        flags.append({"flag": "new_account", "severity": "medium"})
                except:
                    pass
            
            # Прапор 2: Низька активність
            if "followers" in data and "posts" in data:
                followers = int(data.get("followers", 0))
                posts = int(data.get("posts", 0))
                if followers > 1000 and posts < 10:
                    flags.append({"flag": "low_engagement", "severity": "high"})
            
            # Прапор 3: Підозрілий username
            if "username" in data:
                username = data["username"]
                if re.match(r".*\d{6,}.*", username):  # Багато цифр
                    flags.append({"flag": "suspicious_username", "severity": "medium"})
            
            # Прапор 4: Email з фальшивого домену
            if "email" in data:
                email = data["email"]
                if any(domain in email for domain in ["tempmail", "10minutemail", "guerrillamail"]):
                    flags.append({"flag": "disposable_email", "severity": "high"})
            
            if flags:
                red_flags.append({
                    "chunk_id": chunk.get("id"),
                    "flags": flags,
                    "risk_score": sum(1 for f in flags if f["severity"] == "high") * 0.3 + 
                                 sum(1 for f in flags if f["severity"] == "medium") * 0.15
                })
        
        return red_flags
    
    @staticmethod
    def detect_coordinated_activity(chunks: List[Dict], relations: List[Dict]) -> List[Dict]:
        """Виявити координовану активність"""
        coordinated = []
        
        # Групувати за часом
        time_groups = {}
        for chunk in chunks:
            try:
                created = datetime.fromisoformat(chunk.get("created_at", ""))
                hour_key = created.strftime("%Y-%m-%d %H:00")
                if hour_key not in time_groups:
                    time_groups[hour_key] = []
                time_groups[hour_key].append(chunk.get("id"))
            except:
                pass
        
        # Знайти години з багатьма активностями
        for hour, chunks_ids in time_groups.items():
            if len(chunks_ids) >= 3:
                coordinated.append({
                    "hour": hour,
                    "activity_count": len(chunks_ids),
                    "risk": "high" if len(chunks_ids) >= 5 else "medium"
                })
        
        return coordinated

# ============================================================================
# 3. RECOMMENDATION ENGINE
# ============================================================================

class RecommendationEngine:
    """Двигун рекомендацій"""
    
    @staticmethod
    def generate_recommendations(
        risk_assessment: Dict,
        anomalies: List[Dict],
        fraud_flags: List[Dict]
    ) -> List[Dict]:
        """Генерувати рекомендації"""
        recommendations = []
        
        # Рекомендація 1: На основі рівня загрози
        threat_level = risk_assessment.get("threat_level")
        
        if threat_level == ThreatLevel.CRITICAL:
            recommendations.append({
                "priority": "CRITICAL",
                "action": "Негайно передати до правоохоронних органів",
                "reason": "Критичний рівень загрози",
                "estimated_impact": "high"
            })
        elif threat_level == ThreatLevel.HIGH:
            recommendations.append({
                "priority": "HIGH",
                "action": "Провести детальну перевірку",
                "reason": f"Високий рівень загрози ({threat_level})",
                "estimated_impact": "high"
            })
        
        # Рекомендація 2: На основі аномалій
        if anomalies:
            geo_anomalies = [a for a in anomalies if a["type"] == "geographic_anomaly"]
            if geo_anomalies:
                recommendations.append({
                    "priority": "MEDIUM",
                    "action": "Перевірити географічні розбіжності",
                    "reason": f"Виявлено {len(geo_anomalies)} географічних аномалій",
                    "estimated_impact": "medium"
                })
        
        # Рекомендація 3: На основі фальшивих акаунтів
        if fraud_flags:
            high_risk_flags = [f for f in fraud_flags if f["risk_score"] > 0.5]
            if high_risk_flags:
                recommendations.append({
                    "priority": "HIGH",
                    "action": "Перевірити підозрілі акаунти",
                    "reason": f"Виявлено {len(high_risk_flags)} подозрілих акаунтів",
                    "estimated_impact": "high"
                })
        
        return sorted(recommendations, key=lambda r: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get(r["priority"], 4))

# ============================================================================
# 4. COMPLIANCE CHECKER
# ============================================================================

class ComplianceChecker:
    """Перевіркач відповідності стандартам"""
    
    @staticmethod
    def check_gdpr_compliance(chunks: List[Dict]) -> Dict[str, Any]:
        """Перевірити GDPR відповідність"""
        issues = []
        
        for chunk in chunks:
            data = chunk.get("data", {})
            
            # Перевірка ПІБ
            if any(field in data for field in ["name", "full_name", "surname"]):
                issues.append({
                    "issue": "Personal name data collected",
                    "severity": "high",
                    "action": "Ensure consent and proper handling"
                })
            
            # Перевірка IP адреси
            if "ip" in data or "ip_address" in data:
                issues.append({
                    "issue": "IP address collected",
                    "severity": "medium",
                    "action": "Anonymize or pseudonymize"
                })
        
        return {
            "compliant": len(issues) == 0,
            "issues": issues,
            "compliance_score": max(0, 1 - (len(issues) * 0.2))
        }
    
    @staticmethod
    def check_legal_status(chunks: List[Dict]) -> Dict[str, Any]:
        """Перевірити законність збору"""
        legal_check = {
            "is_legal": True,
            "warnings": [],
            "recommendations": []
        }
        
        # Перевірка на приватні дані
        private_fields = ["password", "credit_card", "ssn", "private_key"]
        for chunk in chunks:
            data = chunk.get("data", {})
            for field in private_fields:
                if field in data:
                    legal_check["is_legal"] = False
                    legal_check["warnings"].append(f"Highly sensitive data: {field}")
        
        if not legal_check["is_legal"]:
            legal_check["recommendations"].append("Delete sensitive data immediately")
            legal_check["recommendations"].append("Review data collection practices")
        
        return legal_check
