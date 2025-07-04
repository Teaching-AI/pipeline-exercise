#!/usr/bin/env python3
import json
import argparse
import base64
import hashlib
import zlib
from typing import Dict, Tuple
from datetime import datetime

class SecureIntermediateGrader:
    def __init__(self):
        self.solutions = self._decode_solutions()
    
    def _decode_solutions(self):
        """Decode obfuscated solutions"""
        
        ENCODED_SOLUTIONS = """\
        eyJxY20iOiB7InEwMSI6ICJCIiwgInEwMiI6ICJCIiwgInEwMyI6ICJCIiwgInEwNCI6ICJCIiw \
        gInEwNSI6ICJCIiwgInEwNiI6ICJCIiwgInEwNyI6ICJDIiwgInEwOCI6ICJCIiwgInEwOSI6IC \ 
        JDIiwgInExMCI6ICJCIn0sICJjb2RlIjogeyJjMDEiOiAibG9nX21ldHJpYyIsICJjMDIiOiAiZ \
        2V0X2R1bW1pZXMiLCAiYzAzIjogIjAuMiIsICJjMDQiOiAiZjFfc2NvcmUiLCAiYzA1IjogIkNP \
        UFkiLCAiYzA2IjogImxvZ19tb2RlbCIsICJjMDciOiAibG9hZCIsICJjMDgiOiAiUE9TVCIsICJ \
        jMDkiOiAiNSIsICJjMTAiOiAibWVkaWFuIn19
        """
        # Décodage simple Base64 pour commencer
        decoded = base64.b64decode(ENCODED_SOLUTIONS).decode('utf-8')
        solutions = json.loads(decoded)
        return solutions
        
    
    def grade_submission(self, file_path: str) -> Dict:
        """Grade QCM + Code completion - niveau intermédiaire"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                submission = json.load(f)
        except FileNotFoundError:
            return self._create_error_result(f"Fichier non trouvé: {file_path}")
        except json.JSONDecodeError as e:
            return self._create_error_result(f"Erreur JSON: {e}")
        except Exception as e:
            return self._create_error_result(f"Erreur lecture fichier: {e}")
        
        # Grade QCM section (10 points)
        qcm_score, qcm_details = self._grade_qcm(submission.get("qcm_questions", {}))
        
        # Grade Code section (10 points)  
        code_score, code_details = self._grade_code(submission.get("code_completion", {}))
        
        total_score = qcm_score + code_score
        
        # Detailed analysis
        category_analysis = self._analyze_categories(qcm_details, code_details)
        
        results = {
            "total_score": total_score,
            "max_score": 20,
            "qcm_score": qcm_score,
            "code_score": code_score,
            "percentage": round((total_score / 20) * 100, 1),
            "passed": total_score >= 14,
            "grade_letter": self._get_grade_letter(total_score),
            "feedback": self._generate_feedback(total_score, qcm_score, code_score),
            "category_analysis": category_analysis,
            "student_answers": self._get_student_answers(qcm_details, code_details),
            "timestamp": datetime.now().isoformat(),
            "course_info": {
                "course": "MODULE 4 – Données, IA & transformation digitale",
                "instructor": "Antoine Coppin",
                "date": "19/01/2026"
            }
        }
        
        return results
    
    def _get_student_answers(self, qcm_details: Dict, code_details: Dict) -> Dict:
        """Get only student answers without revealing correct ones"""
        student_answers = {
            "qcm": {},
            "code": {}
        }
        
        # QCM answers (only what student submitted)
        for q_id, details in qcm_details.items():
            student_answers["qcm"][q_id] = {
                "submitted": details["submitted"],
                "correct": details["correct"],
                "category": details["category"]
                # 🚫 NO "expected" field - solutions hidden!
            }
        
        # Code answers (only what student submitted)
        for c_id, details in code_details.items():
            student_answers["code"][c_id] = {
                "submitted": details["submitted"],
                "correct": details["correct"],
                "category": details["category"]
                # 🚫 NO "expected" field - solutions hidden!
            }
        
        return student_answers
    
    def _create_error_result(self, error_msg: str) -> Dict:
        """Create standardized error result"""
        return {
            "total_score": 0,
            "max_score": 20,
            "qcm_score": 0,
            "code_score": 0,
            "percentage": 0.0,
            "passed": False,
            "grade_letter": "F",
            "error": error_msg,
            "feedback": f"❌ Erreur: {error_msg}",
            "category_analysis": {},
            "student_answers": {"qcm": {}, "code": {}},
            "timestamp": datetime.now().isoformat(),
            "course_info": {
                "course": "MODULE 4 – Données, IA & transformation digitale", 
                "instructor": "Antoine Coppin",
                "date": "19/01/2026"
            }
        }
    
    def _grade_qcm(self, qcm_questions: Dict) -> Tuple[int, Dict]:
        """Grade QCM section"""
        score = 0
        details = {}
        
        for q_id, correct_answer in self.solutions["qcm"].items():
            if q_id in qcm_questions:
                submitted = qcm_questions[q_id].get("answer", "").strip().upper()
                correct = submitted == correct_answer
                
                if correct:
                    score += 1
                
                details[q_id] = {
                    "correct": correct,
                    "submitted": submitted,
                    "expected": correct_answer,  # Used internally only
                    "category": self._get_qcm_category(q_id)
                }
            else:
                details[q_id] = {
                    "correct": False,
                    "submitted": "NOT_ANSWERED",
                    "expected": correct_answer,  # Used internally only
                    "category": self._get_qcm_category(q_id)
                }
        
        return score, details
    
    def _grade_code(self, code_completion: Dict) -> Tuple[int, Dict]:
        """Grade code completion section"""
        score = 0
        details = {}
        
        for c_id, correct_answer in self.solutions["code"].items():
            if c_id in code_completion:
                submitted = code_completion[c_id].get("answer", "").strip()
                
                # Flexible matching for code answers
                correct = self._code_match(submitted, correct_answer)
                
                if correct:
                    score += 1
                
                details[c_id] = {
                    "correct": correct,
                    "submitted": submitted,
                    "expected": correct_answer,  # Used internally only
                    "category": self._get_code_category(c_id)
                }
            else:
                details[c_id] = {
                    "correct": False,
                    "submitted": "NOT_ANSWERED",
                    "expected": correct_answer,  # Used internally only
                    "category": self._get_code_category(c_id)
                }
        
        return score, details
    
    def _code_match(self, submitted: str, expected: str) -> bool:
        """Flexible matching for code answers"""
        submitted_clean = submitted.lower().strip().replace("'", "").replace('"', "")
        expected_clean = expected.lower().strip()
        
        # Exact match
        if submitted_clean == expected_clean:
            return True
        
        # Common variations
        variations = {
            "log_metric": ["log_metric", "logmetric"],
            "get_dummies": ["get_dummies", "getdummies"],
            "0.2": ["0.2", "0.20", ".2"],
            "f1_score": ["f1_score", "f1score"],
            "copy": ["copy", "COPY"],
            "log_model": ["log_model", "logmodel"],
            "load": ["load"],
            "post": ["post", "POST"],
            "5": ["5", "5.0"],
            "median": ["median"]
        }
        
        for expected_var, accepted_vars in variations.items():
            if expected_clean == expected_var:
                return submitted_clean in [var.lower() for var in accepted_vars]
        
        return False
    
    def _get_qcm_category(self, q_id: str) -> str:
        """Get category for QCM question"""
        categories = {
            "q01": "Pipeline ML", "q02": "MLOps", "q03": "Data Drift", "q04": "RGPD",
            "q05": "Métriques ML", "q06": "Biais Algorithmiques", "q07": "Architecture Déploiement",
            "q08": "Feature Engineering", "q09": "Monitoring", "q10": "Sécurité & Ethics"
        }
        return categories.get(q_id, "Autre")
    
    def _get_code_category(self, c_id: str) -> str:
        """Get category for code completion"""
        categories = {
            "c01": "MLflow", "c02": "pandas", "c03": "scikit-learn", "c04": "Métriques",
            "c05": "Docker", "c06": "MLflow", "c07": "Python", "c08": "API",
            "c09": "Validation", "c10": "Preprocessing"
        }
        return categories.get(c_id, "Autre")
    
    def _analyze_categories(self, qcm_details: Dict, code_details: Dict) -> Dict:
        """Analyze performance by category"""
        categories = {}
        
        # Analyze QCM by category
        for q_id, result in qcm_details.items():
            category = result["category"]
            if category not in categories:
                categories[category] = {"correct": 0, "total": 0}
            
            categories[category]["total"] += 1
            if result["correct"]:
                categories[category]["correct"] += 1
        
        # Analyze Code by category
        for c_id, result in code_details.items():
            category = result["category"]
            if category not in categories:
                categories[category] = {"correct": 0, "total": 0}
            
            categories[category]["total"] += 1
            if result["correct"]:
                categories[category]["correct"] += 1
        
        # Calculate percentages
        for category in categories:
            correct = categories[category]["correct"]
            total = categories[category]["total"]
            categories[category]["percentage"] = round((correct / total) * 100, 1) if total > 0 else 0
        
        return categories
    
    def _get_grade_letter(self, score: int) -> str:
        """Convert numeric score to letter grade"""
        if score >= 18:
            return "A"
        elif score >= 16:
            return "B+"
        elif score >= 14:
            return "B"
        elif score >= 12:
            return "C+"
        elif score >= 10:
            return "C"
        else:
            return "D"
    
    def _generate_feedback(self, total_score: int, qcm_score: int, code_score: int) -> str:
        """Generate detailed feedback"""
        feedback_parts = []
        
        # Overall performance
        if total_score >= 18:
            feedback_parts.append("🏆 Excellent ! Vous maîtrisez très bien les concepts MLOps et leur mise en pratique.")
        elif total_score >= 16:
            feedback_parts.append("🥇 Très bon travail ! Solides connaissances théoriques et pratiques.")
        elif total_score >= 14:
            feedback_parts.append("👍 Bien ! Vous avez validé le module avec un niveau satisfaisant.")
        elif total_score >= 12:
            feedback_parts.append("⚠️ Passable. Quelques lacunes à combler avant d'être opérationnel.")
        elif total_score >= 10:
            feedback_parts.append("📚 Insuffisant. Révision nécessaire des concepts fondamentaux.")
        else:
            feedback_parts.append("❌ Très insuffisant. Reprise complète du module recommandée.")
        
        # QCM analysis
        if qcm_score >= 8:
            feedback_parts.append(f"Théorie ({qcm_score}/10): Concepts bien assimilés.")
        elif qcm_score >= 6:
            feedback_parts.append(f"Théorie ({qcm_score}/10): Bases correctes, approfondissement nécessaire.")
        else:
            feedback_parts.append(f"Théorie ({qcm_score}/10): Lacunes importantes dans les concepts.")
        
        # Code analysis
        if code_score >= 8:
            feedback_parts.append(f"Pratique ({code_score}/10): Bonne maîtrise des outils.")
        elif code_score >= 6:
            feedback_parts.append(f"Pratique ({code_score}/10): Connaissances pratiques à consolider.")
        else:
            feedback_parts.append(f"Pratique ({code_score}/10): Travail nécessaire sur la syntaxe et les APIs.")
        
        return " ".join(feedback_parts)

def main():
    parser = argparse.ArgumentParser(description='Grade Secure Intermediate ML Exercise')
    parser.add_argument('--file', required=True, help='JSON submission file')
    parser.add_argument('--output', required=True, help='Results JSON file')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    grader = SecureIntermediateGrader()
    results = grader.grade_submission(args.file)
    
    # Save detailed results (WITHOUT revealing correct answers)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Console output
    print(f"📊 RÉSULTATS - MODULE 4 - Données, IA & transformation digitale")
    print(f"Score total: {results['total_score']}/20 ({results['percentage']}%) - Note: {results['grade_letter']}")
    print(f"QCM: {results['qcm_score']}/10 | Code: {results['code_score']}/10")
    print(f"Status: {'✅ VALIDÉ' if results['passed'] else '❌ NON VALIDÉ'}")
    
    if 'error' in results:
        print(f"Erreur: {results['error']}")
    
    if args.verbose and 'error' not in results:
        print(f"\nFeedback: {results['feedback']}")
        print(f"\nPerformance par catégorie:")
        for category, data in results['category_analysis'].items():
            print(f"  - {category}: {data['correct']}/{data['total']} ({data['percentage']}%)")
    
    return 0 if results['passed'] else 1

if __name__ == '__main__':
    exit(main())