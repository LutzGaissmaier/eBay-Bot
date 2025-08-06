#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hauptserver import get_ai_recommendation
import json

def test_ai_integration():
    """Test AI integration with sample data"""
    print("Testing AI Integration...")
    
    test_cases = [
        {
            'offer_amount': 85.0,
            'list_price': 100.0,
            'item_title': 'Test Item - High Value Offer',
            'buyer_message': 'Great item, please consider my offer'
        },
        {
            'offer_amount': 50.0,
            'list_price': 100.0,
            'item_title': 'Test Item - Low Value Offer',
            'buyer_message': 'Budget is tight, hope you can accept'
        },
        {
            'offer_amount': 75.0,
            'list_price': 100.0,
            'item_title': 'Test Item - Medium Value Offer',
            'buyer_message': 'Fair price for both of us'
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            result = get_ai_recommendation(
                test_case['offer_amount'],
                test_case['list_price'],
                test_case['item_title'],
                test_case['buyer_message']
            )
            
            print(f"\nTest Case {i}:")
            print(f"  Offer: €{test_case['offer_amount']} / €{test_case['list_price']} ({test_case['offer_amount']/test_case['list_price']*100:.1f}%)")
            print(f"  Result: {json.dumps(result, indent=4)}")
            
            required_keys = ['recommendation', 'confidence', 'reasoning', 'ai_powered']
            if not all(key in result for key in required_keys):
                print(f"  ❌ Missing required keys in result")
                all_passed = False
            elif result['confidence'] < 0 or result['confidence'] > 100:
                print(f"  ❌ Invalid confidence value: {result['confidence']}")
                all_passed = False
            elif result['recommendation'] not in ['Akzeptieren', 'Ablehnen', 'Gegenangebot']:
                print(f"  ❌ Invalid recommendation: {result['recommendation']}")
                all_passed = False
            else:
                print(f"  ✅ Test case {i} passed")
                
        except Exception as e:
            print(f"  ❌ Test case {i} failed: {str(e)}")
            all_passed = False
    
    if all_passed:
        print(f"\n✅ All AI integration tests passed!")
        return True
    else:
        print(f"\n❌ Some AI integration tests failed!")
        return False

if __name__ == "__main__":
    success = test_ai_integration()
    sys.exit(0 if success else 1)
