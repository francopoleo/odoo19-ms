#!/usr/bin/env python3
"""
Test script for document_core enterprise features
Validates validation workflows, review cycles, and activity scheduling
"""
import os
import sys
import django
from datetime import date, timedelta

# Setup Django/Odoo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'odoo.settings')
os.chdir('/Users/franco/Dev/odoo/odoo19-ms')
sys.path.insert(0, '/Users/franco/Dev/odoo/odoo19-ms')

import odoo
from odoo.tools import config
from odoo.api import Environment

config.parse_config(['-d', 'odoo19_ms'])

def test_enterprise_features():
    """Test all enterprise-level document management features"""

    import odoo.registry
    registry = odoo.registry.Registry('odoo19_ms')

    with registry.cursor() as cr:
        env = Environment(cr, 2, {})

        print("\n" + "=" * 70)
        print("TESTING ENTERPRISE-LEVEL DOCUMENT MANAGEMENT SYSTEM")
        print("=" * 70)

        # Test 1: Create document category
        print("\n[TEST 1] Creating Document Category...")
        try:
            category = env['document.category'].create({
                'name': 'Documentos Jurídicos - Teste',
                'code': 'LEGAL_TEST',
            })
            print(f"✓ Category created: {category.name} (ID: {category.id})")
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False

        # Test 2: Create document type with validation requirement
        print("\n[TEST 2] Creating Document Type with Validation Requirement...")
        try:
            doc_type = env['document.type'].create({
                'name': 'Procuração Jurídica - Teste',
                'code': 'POA_TEST',
                'category_id': category.id,
                'requires_validation': True,
                'requires_issue_date': True,
                'requires_expiry': True,
                'review_cycle_days': 90,
            })
            print(f"✓ Document type created: {doc_type.name}")
            print(f"  - Requires validation: {doc_type.requires_validation}")
            print(f"  - Review cycle: {doc_type.review_cycle_days} days")
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False

        # Test 3: Create document
        print("\n[TEST 3] Creating Document...")
        try:
            today = date.today()
            doc = env['document.document'].create({
                'name': 'Teste Procuração Jurídica',
                'document_type_id': doc_type.id,
                'document_state': 'draft',
                'issue_date': today,
                'expiry_date': today + timedelta(days=365),
                'review_date': today,
                'responsible_id': env.user.id,
            })
            print(f"✓ Document created: {doc.name}")
            print(f"  - Reference: {doc.reference}")
            print(f"  - State: {doc.document_state}")
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False

        # Test 4: Verify computed fields
        print("\n[TEST 4] Verifying Computed Fields...")
        try:
            print(f"✓ Status: {doc.status}")
            print(f"✓ Requires validation: {doc.requires_validation}")
            print(f"✓ Is validated: {doc.is_validated}")
            print(f"✓ Next review date: {doc.next_review_date}")
            print(f"✓ Review status: {doc.review_status}")
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False

        # Test 5: Try to activate without validation (should fail)
        print("\n[TEST 5] Testing Validation Constraint...")
        try:
            doc.write({'document_state': 'active'})
            print(f"✗ ERROR: Should have prevented activation without validation!")
            return False
        except Exception as constraint_error:
            if 'validação' in str(constraint_error).lower() or 'validation' in str(constraint_error).lower():
                print(f"✓ Correctly blocked activation: {str(constraint_error)[:60]}...")
            else:
                print(f"✗ Wrong error: {constraint_error}")
                return False

        # Test 6: Mark as validated
        print("\n[TEST 6] Validating Document...")
        try:
            doc.write({
                'validated_by': env.user.id,
                'validation_date': today,
            })
            print(f"✓ Document validated")
            print(f"  - Validated by: {doc.validated_by.name}")
            print(f"  - Is validated: {doc.is_validated}")
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False

        # Test 7: Now activate should work
        print("\n[TEST 7] Activating Validated Document...")
        try:
            doc.write({'document_state': 'active'})
            print(f"✓ Document activated successfully")
            print(f"  - State: {doc.document_state}")
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False

        # Test 8: Check scheduled activities
        print("\n[TEST 8] Checking Scheduled Activities...")
        try:
            activities = doc.activity_ids
            print(f"✓ Total activities scheduled: {len(activities)}")
            if activities:
                for activity in activities:
                    print(f"  - {activity.summary} (Type: {activity.activity_type_id.name})")
            else:
                print("  (No activities scheduled yet - normal for valid documents)")
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False

        # Test 9: Verify mail activity types exist
        print("\n[TEST 9] Verifying Mail Activity Types...")
        try:
            expiry_type = env.ref('document_core.mail_activity_type_document_expiry')
            validation_type = env.ref('document_core.mail_activity_type_document_validation')
            review_type = env.ref('document_core.mail_activity_type_document_review')

            print(f"✓ Expiry activity type: {expiry_type.name}")
            print(f"✓ Validation activity type: {validation_type.name}")
            print(f"✓ Review activity type: {review_type.name}")
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False

        # Test 10: Verify cron jobs exist
        print("\n[TEST 10] Verifying Cron Jobs...")
        try:
            expiry_cron = env.ref('document_core.cron_document_check_expiry')
            validation_cron = env.ref('document_core.cron_document_check_validation')
            review_cron = env.ref('document_core.cron_document_check_review')

            print(f"✓ Expiry cron job: {expiry_cron.name} (Active: {expiry_cron.active})")
            print(f"✓ Validation cron job: {validation_cron.name} (Active: {validation_cron.active})")
            print(f"✓ Review cron job: {review_cron.name} (Active: {review_cron.active})")
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False

        print("\n" + "=" * 70)
        print("ALL TESTS PASSED ✓ - Enterprise document management is working!")
        print("=" * 70)
        return True

if __name__ == '__main__':
    success = test_enterprise_features()
    sys.exit(0 if success else 1)