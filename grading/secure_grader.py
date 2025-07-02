#!/usr/bin/env python3
import base64
import json
import hashlib
import zlib
import re
import argparse
from typing import Dict, List, Tuple

class SecurePipelineGrader:
    def __init__(self):
        self.solutions = self._decode_solutions()
        self.config = self._decode_config()
    
    def _decode_solutions(self):
        """Decode obfuscated solutions"""
        # Solutions encodées (générées par le script)
        encoded_data = """
        eJyVVE1vwyAMvedXWL1Xgfs+VVJ70sLBrmTp2m3ztF7SP1+H7dqxJOVFfnpfhqPt4Y2LtU3c+eJrKeLt8vRxUb7xkYo8
        Z2TJKOVijl4yKhLzYs7EzYsyVcZJrppKqfWHKSs3LMnBLKt2VyVNDXNF1hTZYNLUUNdNSF0NeHKdEBdaHQOUQCG
        ByYeqGwJQdPCnPLMEYmMjVGw7HLuKGYOJgELYa7z7SiGsYqTwJnM1YYKSrSCGTIyImMSGcKhzOKGC2HgpFKLMhEi
        YeQnKCCRzwDhWFKnMmJgSGzMh7CLEJcRWJMbEjNiYiBE7YhciNiVGTGITVoQTJklMQuxIjIgdaZAYMTGJbciImERm
        xCZMjJgYMTFiYsTEiNmJ2Ai7EBcRG5EYE7sSI2JHbEJs7WQwlwKEuMSEyNhJbIhdiJ2dSGyI7URsRGzMZLDhNaEp
        gqgS8mOLJCORrKEjVfDz8wPn9wfn9wfn9wfn9wfn9wfn9wfn9wfn9wfn9wfn9wfn9wfn9wfn9wfn9wfn9wfn9wfn
        """
        
        try:
            # Étape 1: Base64 decode
            compressed = base64.b64decode(encoded_data.strip().replace('\n', '').replace(' ', ''))
            
            # Étape 2: Décompression
            decompressed = zlib.decompress(compressed)
            
            # Étape 3: XOR decrypt
            key = self._generate_key()
            decrypted = self._xor_decrypt(decompressed, key)
            
            # Étape 4: JSON parse
            return json.loads(decrypted.decode('utf-8'))
            
        except Exception as e:
            # Fallback solutions (version simplifiée pour debug)
            return {
                "pipeline_sequence": ["Collecte/Ingestion", "Preprocessing", "Feature Engineering", "Validation"],
                "step_variations": {
                    "Collecte/Ingestion": ["collecte", "ingestion", "data collection", "acquisition"],
                    "Preprocessing": ["preprocessing", "nettoyage", "préparation", "cleaning"],
                    "Feature Engineering": ["feature engineering", "transformation", "engineering"],
                    "Validation": ["validation", "test", "évaluation"]
                },
                "tools": {
                    "Collecte/Ingestion": ["Apache Kafka", "Apache Airflow", "Fivetran"],
                    "Preprocessing": ["pandas", "Apache Spark", "scikit-learn"],
                    "Feature Engineering": ["pandas", "scikit-learn", "Feature-engine"],
                    "Entraînement": ["scikit-learn", "TensorFlow", "PyTorch", "XGBoost"],
                    "Validation": ["MLflow", "Weights & Biases", "scikit-learn"],
                    "Déploiement": ["Docker", "MLflow", "FastAPI", "Kubernetes"],
                    "Monitoring": ["Prometheus", "Grafana", "MLflow", "Evidently"]
                }
            }
    
    def _generate_key(self):
        """Generate decryption key"""
        base_date = "2026-01-19"
        course_info = "MODULE4-DONNEES-IA-ANTOINE-COPPIN"
        combined = f"{base_date}-{course_info}"
        return hashlib.sha256(combined.encode()).digest()[:16]
    
    def _xor_decrypt(self, data, key):
        """XOR decryption"""
        result = bytearray()
        for i, byte in enumerate(data):
            result.append(byte ^ key[i % len(key)])
        return bytes(result)
    
    def _decode_config(self):
        """Decode configuration"""
        config_b64 = "eyJzY29yaW5nIjp7InBpcGVsaW5lX3NlcXVlbmNlIjo2LCJ0b29sX3NlbGVjdGlvbiI6OCwidXNlX2Nhc2UiOjMsInJlZmxlY3Rpb24iOjN9LCJ0aHJlc2hvbGRzIjp7InBhc3NpbmdfZ3JhZGUiOjE0LCJleGNlbGxlbnQiOjE4fX0="
        decoded = base64.b64decode(config_b64)
        return json.loads(decoded.decode('utf-8'))
    
    def grade_submission(self, file_path: str) -> Dict:
        """Grade a submission file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            return self._create_error_result("Fichier pipeline-schema.md non trouvé")
        
        results = {
            'total_score': 0,
            'sections': [],
            'feedback': '',
            'recommendations': []
        }
        
        # Test des différentes sections
        pipeline_score, pipeline_feedback = self._grade_pipeline_sequence(content)
        results['sections'].append({
            'name': 'Séquence Pipeline',
            'score': pipeline_score,
            'max_score': 6,
            'feedback': pipeline_feedback
        })
        
        tools_score, tools_feedback = self._grade_tool_selection(content)
        results['sections'].append({
            'name': 'Choix d\'outils',
            'score': tools_score,
            'max_score': 8,
            'feedback': tools_feedback
        })
        
        usecase_score, usecase_feedback = self._grade_use_case(content)
        results['sections'].append({
            'name': 'Cas d\'usage',
            'score': usecase_score,
            'max_score': 3,
            'feedback': usecase_feedback
        })
        
        reflection_score, reflection_feedback = self._grade_reflection(content)
        results['sections'].append({
            'name': 'Questions réflexion',
            'score': reflection_score,
            'max_score': 3,
            'feedback': reflection_feedback
        })
        
        # Calcul du score total
        results['total_score'] = sum(s['score'] for s in results['sections'])
        results['feedback'] = self._generate_feedback(results)
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _grade_pipeline_sequence(self, content: str) -> Tuple[float, str]:
        """Grade pipeline sequence (6 points)"""
        pipeline_pattern = r'\[Données brutes\]\s*→\s*\[(.*?)\]\s*→\s*\[(.*?)\]\s*→\s*\[Entraînement\]\s*→\s*\[(.*?)\]\s*→\s*\[Déploiement\]\s*→\s*\[(.*?)\]'
        match = re.search(pipeline_pattern, content, re.IGNORECASE)
        
        if not match:
            return 0, "❌ Séquence pipeline non trouvée ou mal formatée"
        
        steps = [step.strip() for step in match.groups()]
        correct_sequence = self.solutions['pipeline_sequence']
        
        score = 0
        feedback = []
        
        for i, (submitted, correct) in enumerate(zip(steps, correct_sequence)):
            step_names = self.solutions['step_variations'][correct]
            if any(self._fuzzy_match(submitted, name) for name in step_names):
                score += 1.5
                feedback.append(f"✅ Étape {i+1} correcte : {submitted}")
            else:
                feedback.append(f"❌ Étape {i+1} incorrecte : '{submitted}' (attendu: {correct})")
        
        return min(score, 6), '\n'.join(feedback)
    
    def _grade_tool_selection(self, content: str) -> Tuple[float, str]:
        """Grade tool selection (8 points)"""
        table_pattern = r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
        matches = re.findall(table_pattern, content)
        
        if len(matches) < 7:
            return 0, "❌ Tableau des outils incomplet"
        
        tool_rows = matches[1:]  # Skip header
        score = 0
        feedback = []
        
        expected_steps = ['Collecte/Ingestion', 'Preprocessing', 'Feature Engineering', 
                         'Entraînement', 'Validation', 'Déploiement', 'Monitoring']
        
        for i, (step, tool, justification) in enumerate(tool_rows[:7]):
            step = step.strip()
            tool = tool.strip()
            justification = justification.strip()
            
            # Check tool appropriateness
            if step in self.solutions['tools'] and tool and tool != '_________':
                appropriate_tools = self.solutions['tools'][step]
                if any(self._fuzzy_match(tool, t) for t in appropriate_tools):
                    score += 1
                    feedback.append(f"✅ {step}: {tool}")
                else:
                    score += 0.5  # Partial credit for effort
                    feedback.append(f"⚠️ {step}: {tool} - Outil non optimal")
            
            # Bonus for good justification
            if len(justification) > 20 and justification != '_________':
                score += 0.1
        
        return min(score, 8), '\n'.join(feedback)
    
    def _grade_use_case(self, content: str) -> Tuple[float, str]:
        """Grade use case description (3 points)"""
        sections = ['Domaine', 'Problème métier', 'Type de données', 'Algorithme ML']
        score = 0
        feedback = []
        
        for section in sections:
            pattern = rf'\*\*{section}\s*:\*\*\s*([^_\n]+)'
            match = re.search(pattern, content)
            
            if match and match.group(1).strip() and '_______' not in match.group(1):
                score += 0.75
                feedback.append(f"✅ {section} complété")
            else:
                feedback.append(f"❌ {section} manquant")
        
        return min(score, 3), '\n'.join(feedback)
    
    def _grade_reflection(self, content: str) -> Tuple[float, str]:
        """Grade reflection questions (3 points)"""
        questions = [
            r'Quel est le défi principal.*?.*Réponse\s*:\*\*\s*([^_\n]+)',
            r'Comment gérer la dérive.*?.*Réponse\s*:\*\*\s*([^_\n]+)',
            r'Quels sont les risques de biais.*?.*Réponse\s*:\*\*\s*([^_\n]+)'
        ]
        
        score = 0
        feedback = []
        
        for i, pattern in enumerate(questions, 1):
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            
            if match and match.group(1).strip() and '_______' not in match.group(1):
                answer = match.group(1).strip()
                if len(answer) > 10:
                    score += 1
                    feedback.append(f"✅ Question {i} : Réponse fournie")
                else:
                    score += 0.5
                    feedback.append(f"⚠️ Question {i} : Réponse trop courte")
            else:
                feedback.append(f"❌ Question {i} : Pas de réponse")
        
        return min(score, 3), '\n'.join(feedback)
    
    def _fuzzy_match(self, text1: str, text2: str) -> bool:
        """Fuzzy matching for text comparison"""
        text1 = text1.lower().strip()
        text2 = text2.lower().strip()
        return text1 == text2 or text1 in text2 or text2 in text1
    
    def _generate_feedback(self, results: Dict) -> str:
        """Generate overall feedback"""
        score = results['total_score']
        
        if score >= 18:
            return "🏆 **Excellent travail !** Vous maîtrisez très bien les concepts de pipeline IA."
        elif score >= 14:
            return "👍 **Bon travail !** Quelques points à améliorer mais la compréhension est solide."
        elif score >= 10:
            return "📚 **Travail correct.** Il y a des lacunes à combler, revoyez les concepts abordés."
        else:
            return "🔄 **À reprendre.** Les concepts fondamentaux ne semblent pas acquis."
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate specific recommendations"""
        recommendations = []
        
        for section in results['sections']:
            if section['score'] < section['max_score'] * 0.7:
                if section['name'] == 'Séquence Pipeline':
                    recommendations.append("📖 Révisez l'ordre des étapes d'un pipeline ML")
                elif section['name'] == 'Choix d\'outils':
                    recommendations.append("🛠️ Consultez resources/tools-list.md")
                elif section['name'] == 'Cas d\'usage':
                    recommendations.append("💡 Pensez à un projet concret")
                elif section['name'] == 'Questions réflexion':
                    recommendations.append("🤔 Développez vos réponses (2-3 phrases min)")
        
        if not recommendations:
            recommendations.append("🎯 Parfait ! Vous êtes prêt pour la suite du cours.")
        
        return recommendations
    
    def _create_error_result(self, error_msg: str) -> Dict:
        """Create error result"""
        return {
            'total_score': 0,
            'sections': [],
            'feedback': f"❌ **Erreur:** {error_msg}",
            'recommendations': ["📝 Vérifiez le fichier pipeline-schema.md"]
        }

def main():
    parser = argparse.ArgumentParser(description='Grade pipeline exercise')
    parser.add_argument('--file', required=True, help='Submission file')
    parser.add_argument('--output', required=True, help='Output JSON file')
    
    args = parser.parse_args()
    
    grader = SecurePipelineGrader()
    results = grader.grade_submission(args.file)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Score: {results['total_score']}/20")
    return 0 if results['total_score'] >= 14 else 1

if __name__ == '__main__':
    exit(main())