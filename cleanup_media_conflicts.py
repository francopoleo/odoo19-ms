#!/usr/bin/env python3
"""
Script para limpar conflitos de mídias em property.media

Uso:
    python cleanup_media_conflicts.py

Limpa todos os records property.media que têm AMBOS image_1920 e file_data preenchidos,
mantendo o campo maior (assumindo que é o arquivo real).
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))

# Setup Odoo (if running in Odoo environment)
import odoo
from odoo import api, fields, models
from odoo.sql_db import db_connect

def cleanup_media_conflicts():
    """Execute cleanup via raw SQL."""
    db = db_connect('odoo19')
    cr = db.cursor()

    try:
        # Find conflicted records
        sql_find = """
            SELECT id, name,
                   OCTET_LENGTH(COALESCE(image_1920, ''::bytea)) as img_len,
                   OCTET_LENGTH(COALESCE(file_data, ''::bytea)) as file_len
            FROM property_media
            WHERE image_1920 IS NOT NULL
              AND image_1920 != ''::bytea
              AND file_data IS NOT NULL
              AND file_data != ''::bytea
            ORDER BY id
        """

        cr.execute(sql_find)
        conflicted = cr.fetchall()

        if not conflicted:
            print("✓ Nenhum conflito de mídia encontrado")
            return 0

        print(f"Found {len(conflicted)} conflicted records:")
        print("-" * 80)

        cleaned = 0
        for rec_id, rec_name, img_len, file_len in conflicted:
            print(f"ID: {rec_id} | Name: {rec_name}")
            print(f"  image_1920: {img_len} bytes | file_data: {file_len} bytes")

            if img_len > file_len:
                # Keep image, remove file
                cr.execute("UPDATE property_media SET file_data = NULL WHERE id = %s", (rec_id,))
                print(f"  → Keeping image_1920, clearing file_data")
                cleaned += 1
            else:
                # Keep file, remove image
                cr.execute("UPDATE property_media SET image_1920 = NULL WHERE id = %s", (rec_id,))
                print(f"  → Keeping file_data, clearing image_1920")
                cleaned += 1

        db.commit()
        cr.close()

        print("-" * 80)
        print(f"✓ Limpeza concluída: {cleaned} records corrigidos")
        return cleaned

    except Exception as e:
        db.rollback()
        cr.close()
        print(f"✗ Erro durante limpeza: {str(e)}")
        return -1


if __name__ == '__main__':
    result = cleanup_media_conflicts()
    sys.exit(0 if result >= 0 else 1)
