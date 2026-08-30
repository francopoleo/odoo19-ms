-- Script para limpar conflitos em property.media
-- Onde AMBOS image_1920 e file_data estão preenchidos
-- Execute com: psql -U odoo -d odoo19 -f cleanup_media_conflicts.sql

-- 1. Mostrar records conflitados
SELECT
    id,
    name,
    OCTET_LENGTH(COALESCE(image_1920, ''::bytea)) as img_bytes,
    OCTET_LENGTH(COALESCE(file_data, ''::bytea)) as file_bytes,
    CASE
        WHEN OCTET_LENGTH(image_1920) > OCTET_LENGTH(file_data) THEN 'Keep image, clear file_data'
        ELSE 'Keep file_data, clear image_1920'
    END as action
FROM property_media
WHERE image_1920 IS NOT NULL
  AND image_1920 != ''::bytea
  AND file_data IS NOT NULL
  AND file_data != ''::bytea
ORDER BY id;

-- 2. Limpar conflitos (image maior = manter image, senão manter file)
UPDATE property_media
SET file_data = NULL
WHERE id IN (
    SELECT id FROM property_media
    WHERE image_1920 IS NOT NULL
      AND image_1920 != ''::bytea
      AND file_data IS NOT NULL
      AND file_data != ''::bytea
      AND OCTET_LENGTH(image_1920) > OCTET_LENGTH(file_data)
);

UPDATE property_media
SET image_1920 = NULL
WHERE id IN (
    SELECT id FROM property_media
    WHERE image_1920 IS NOT NULL
      AND image_1920 != ''::bytea
      AND file_data IS NOT NULL
      AND file_data != ''::bytea
      AND OCTET_LENGTH(file_data) >= OCTET_LENGTH(image_1920)
);

-- 3. Verificar se limpeza foi sucesso
SELECT COUNT(*) as remaining_conflicts
FROM property_media
WHERE image_1920 IS NOT NULL
  AND image_1920 != ''::bytea
  AND file_data IS NOT NULL
  AND file_data != ''::bytea;
