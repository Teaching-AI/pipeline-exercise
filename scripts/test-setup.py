#!/usr/bin/env python3
"""Script de test pour valider le setup du repository"""

import os
import json
import subprocess
import sys

def test_file_structure():
    """Test que tous les fichiers nécessaires sont présents"""
    required_files = [
        'README.md',
        'pipeline-schema.md',
        '.github/workflows/grade-submission.yml',
        'grading/secure_grader.py',
        'resources/tools-list.md',
        'resources/help-github.md',
        'resources/examples/good-example.md',
        'resources/examples/bad-example.md'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Fichiers manquants: {missing}")
        return False
    
    print("✅ Structure des fichiers OK")
    return True

def test_grader():
    """Test que le grader fonctionne"""
    try:
        # Test avec l'exemple correct
        result = subprocess.run([
            'python', 'grading/secure_grader.py', 
            '--file', 'resources/examples/good-example.md',
            '--output', 'test-results.json'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            with open('test-results.json', 'r') as f:
                results = json.load(f)
            
            score = results['total_score']
            print(f"✅ Grader fonctionne - Score exemple: {score}/20")
            
            # Cleanup
            os.remove('test-results.json')
            return True
        else:
            print(f"❌ Erreur grader: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Exception grader: {e}")
        return False

def test_workflow_syntax():
    """Test que le workflow YAML est valide"""
    try:
        import yaml
        with open('.github/workflows/grade-submission.yml', 'r') as f:
            yaml.safe_load(f)
        print("✅ Workflow YAML valide")
        return True
    except Exception as e:
        print(f"❌ Workflow YAML invalide: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Test du setup repository...\n")
    
    tests = [
        ("Structure fichiers", test_file_structure),
        ("Grader fonctionnel", test_grader),
        ("Workflow YAML", test_workflow_syntax)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"Testing {name}...")
        success = test_func()
        results.append(success)
        print()
    
    if all(results):
        print("🎉 Tous les tests passent ! Repository prêt.")
        return 0
    else:
        print("❌ Certains tests échouent. Vérifiez la configuration.")
        return 1

if __name__ == '__main__':
    sys.exit(main())