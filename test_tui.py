#!/usr/bin/env python3
"""
Test script for the Astrolabe TUI
Validates that the TUI can be imported and basic functionality works
"""

import sys
import json
import os
from pathlib import Path

def test_tui_import():
    """Test that the TUI can be imported"""
    try:
        from tui import TUI, ModelManager
        print("✓ TUI imports successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import TUI: {e}")
        return False

def test_model_manager():
    """Test the ModelManager class"""
    try:
        from tui import ModelManager
        
        # Test with a temporary models file
        test_file = "test_models.json"
        
        # Clean up if exists
        if os.path.exists(test_file):
            os.remove(test_file)
        
        manager = ModelManager(test_file)
        
        # Test add model
        test_config = {
            "name": "test_model",
            "optimizer_type": "Standard Optimizer",
            "num_params": 2,
            "mins": [0.0, 0.0],
            "maxs": [1.0, 1.0],
            "learning_rates": [0.0001, 0.0001],
            "initial_weights": [0.5, 0.5],
            "current_weights": [0.5, 0.5]
        }
        
        manager.add_model("test_model", test_config)
        print("✓ ModelManager can add models")
        
        # Test get model
        retrieved = manager.get_model("test_model")
        if retrieved and retrieved["name"] == "test_model":
            print("✓ ModelManager can retrieve models")
        else:
            print("✗ ModelManager failed to retrieve model")
            return False
        
        # Test get all models
        all_models = manager.get_all_models()
        if "test_model" in all_models:
            print("✓ ModelManager can list all models")
        else:
            print("✗ ModelManager failed to list models")
            return False
        
        # Test remove model
        manager.remove_model("test_model")
        if not manager.model_exists("test_model"):
            print("✓ ModelManager can remove models")
        else:
            print("✗ ModelManager failed to remove model")
            return False
        
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
        
        return True
    except Exception as e:
        print(f"✗ ModelManager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_models_json():
    """Test that models.json exists and is valid"""
    try:
        if not os.path.exists("models.json"):
            print("✗ models.json does not exist")
            return False
        
        with open("models.json", 'r') as f:
            models = json.load(f)
        
        print(f"✓ models.json is valid JSON with {len(models)} models")
        
        # Verify demo models
        if "demo_pid_controller" in models:
            print("  ✓ demo_pid_controller found")
        if "demo_momentum_controller" in models:
            print("  ✓ demo_momentum_controller found")
        
        return True
    except Exception as e:
        print(f"✗ models.json validation failed: {e}")
        return False

def test_tui_instantiation():
    """Test that TUI can be instantiated"""
    try:
        from tui import TUI
        tui = TUI()
        print("✓ TUI can be instantiated")
        
        # Verify it has the necessary attributes
        if hasattr(tui, 'manager') and hasattr(tui, 'running'):
            print("✓ TUI has required attributes")
            return True
        else:
            print("✗ TUI missing required attributes")
            return False
    except Exception as e:
        print(f"✗ TUI instantiation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("  Astrolabe TUI Test Suite")
    print("=" * 60)
    print()
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    tests = [
        ("TUI Import", test_tui_import),
        ("models.json Validation", test_models_json),
        ("ModelManager Class", test_model_manager),
        ("TUI Instantiation", test_tui_instantiation),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
        print()
    
    # Summary
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! TUI is ready to use.")
        print("\nRun the TUI with: python3 tui.py")
        return 0
    else:
        print("✗ Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
