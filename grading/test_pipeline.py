#!/usr/bin/env python3
import yaml
import re
import json
import argparse
from typing import Dict, List, Tuple

class PipelineGrader:
    def __init__(self, config_path: str, solutions_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        with open(solutions_path, 'r', encoding='utf-8') as f:
            self.solutions = yaml.safe_load(f)
    
    def grade_submission(self, file_path: str) -> Dict:
        """Grade a submission file and return detailed results"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            return self._create_error_result("Fichier pipeline-schema.md non trouvé")
        
        results = {
            'total_score': 0,
            'max_score': 20,
            'sections': [],
            'feedback': '',
            'recommendations': []
        }
        
        # Test 1: Pipeline sequence (6 points)
        pipeline_score, pipeline_feedback = self._grade_pipeline_sequence(content)
        results['sections'].append({
            'name': 'Séquence Pipeline',
            'score': pipeline_score,
            'max_score': 6,
            'feedback': pipeline_feedback
        })
        
        # Test 2: Tool selection (8 points)
        tools_score, tools_feedback = self._grade_tool_selection(content)
        results['sections'].append({
            'name': 'Choix d\'outils',
            'score': tools_score,
            'max_score': 8,
            'feedback': tools_feedback
        })
        
        # Test 3: Use case description (3 points)
        usecase_score, usecase_feedback = self._grade_use_case(content)
        results['sections'].append({
            'name': 'Cas d\'usage',
            'score': usecase_score,
            'max_score': 3,
            'feedback': usecase_feedback
        })
        
        # Test 4: Reflection questions (3 points)
        reflection_score, reflection_feedback = self._grade_reflection(content)
        results['sections'].append({
            'name': 'Questions réflexion',
            'score': reflection_score,
            'max_score': 3,
            'feedback': reflection_feedback
        })
        
        # Calculate total
        results['total_score'] = sum(s['score'] for s in results['sections'])
        
        # Generate feedback and recommendations
        results['feedback'] = self._generate_feedback(results)
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _grade_pipeline_sequence(self, content: str) -> Tuple[int, str]:
        """Grade the pipeline sequence ordering (6 points)"""
        # Extract the pipeline sequence from markdown
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
    
    def _grade_tool_selection(self, content: str) -> Tuple[int, str]:
        """Grade tool selection for each step (8 points)"""
        # Extract tools table
        table_pattern = r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
        matches = re.findall(table_pattern, content)
        
        if len(matches) < 7:  # Header + 6 data rows minimum
            return 0, "❌ Tableau des outils incomplet ou mal formaté"
        
        # Skip header row
        tool_rows = matches[1:]
        
        score = 0
        feedback = []
        
        expected_steps = ['Collecte/Ingestion', 'Preprocessing', 'Feature Engineering', 
                         'Entraînement', 'Validation', 'Déploiement', 'Monitoring']
        
        for i, (step, tool, justification) in enumerate(tool_rows[:7]):
            step = step.strip()
            tool = tool.strip()
            justification = justification.strip()
            
            # Check if tool is appropriate (1 point per step)
            if step in self.solutions['tools'] and tool:
                appropriate_tools = self.solutions['tools'][step]
                if any(self._fuzzy_match(tool, t) for t in appropriate_tools):
                    score += 1
                    feedback.append(f"✅ {step}: {tool} - Choix approprié")
                else:
                    feedback.append(f"⚠️ {step}: {tool} - Outil non optimal (suggestions: {', '.join(appropriate_tools[:3])})")
            
            # Check justification quality (bonus points)
            if len(justification) > 20 and any(keyword in justification.lower() 
                   for keyword in ['performance', 'scalabilité', 'facilité', 'coût', 'maintenance']):
                score += 0.2
                feedback.append(f"💡 Bonne justification pour {step}")
        
        return min(score, 8), '\n'.join(feedback)
    
    def _grade_use_case(self, content: str) -> Tuple[int, str]:
        """Grade use case description (3 points)"""
        sections = ['Domaine', 'Problème métier', 'Type de données', 'Algorithme ML']
        score = 0
        feedback = []
        
        for section in sections:
            pattern = rf'\*\*{section}\s*:\*\*\s*([^_\n]+)'
            match = re.search(pattern, content)
            
            if match and match.group(1).strip() and match.group(1).strip() != '________________':
                score += 0.75
                feedback.append(f"✅ {section} complété")
            else:
                feedback.append(f"❌ {section} manquant ou incomplet")
        
        return min(score, 3), '\n'.join(feedback)
    
    def _grade_reflection(self, content: str) -> Tuple[int, str]:
        """Grade reflection questions (3 points)"""
        questions = [
            r'Quel est le défi principal.*?.*Réponse\s*:\s*([^_\n]+)',
            r'Comment gérer la dérive.*?.*Réponse\s*:\s*([^_\n]+)',
            r'Quels sont les risques de biais.*?.*Réponse\s*:\s*([^_\n]+)'
        ]
        
        score = 0
        feedback = []
        
        for i, pattern in enumerate(questions, 1):
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            
            if match and match.group(1).strip() and match.group(1).strip() != '________________':
                answer = match.group(1).strip()
                if len(answer) > 10:  # Minimum effort check
                    score += 1
                    feedback.append(f"✅ Question {i} : Réponse fournie")
                else:
                    feedback.append(f"⚠️ Question {i} : Réponse trop courte")
            else:
                feedback.append(f"❌ Question {i} : Pas de réponse")
        
        return min(score, 3), '\n'.join(feedback)
    
    def _fuzzy_match(self, text1: str, text2: str) -> bool:
        """Fuzzy matching for tool names"""
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
                    recommendations.append("📖 Révisez l'ordre des étapes d'un pipeline ML (cours slide 15)")
                elif section['name'] == 'Choix d\'outils':
                    recommendations.append("🛠️ Consultez la liste des outils recommandés (resources/tools-list.md)")
                elif section['name'] == 'Cas d\'usage':
                    recommendations.append("💡 Pensez à un projet concret pour illustrer votre pipeline")
                elif section['name'] == 'Questions réflexion':
                    recommendations.append("🤔 Développez davantage vos réponses (minimum 2-3 phrases)")
        
        if not recommendations:
            recommendations.append("🎯 Parfait ! Vous êtes prêt pour la suite du cours.")
        
        return recommendations
    
    def _create_error_result(self, error_msg: str) -> Dict:
        """Create error result structure"""
        return {
            'total_score': 0,
            'max_score': 20,
            'sections': [],
            'feedback': f"❌ **Erreur:** {error_msg}",
            'recommendations': ["📝 Vérifiez que vous avez bien modifié le fichier pipeline-schema.md"]
        }

def main():
    parser = argparse.ArgumentParser(description='Grade pipeline exercise submission')
    parser.add_argument('--file', required=True, help='Submission file to grade')
    parser.add_argument('--output', required=True, help='Output JSON file for results')
    
    args = parser.parse_args()
    
    grader = PipelineGrader('grading/grading_config.yml', 'grading/solutions.yml')
    results = grader.grade_submission(args.file)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Score: {results['total_score']}/20")
    return 0 if results['total_score'] >= 14 else 1

if __name__ == '__main__':
    exit(main())