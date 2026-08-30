#!/usr/bin/env python3
"""
Script de migração de arquivos do armazenamento local para S3/DigitalOcean Spaces
Uso: python migrate_to_s3.py -d database_name -s s3_bucket
"""

import os
import sys
import argparse
import logging
from datetime import datetime

import boto3

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Migrar arquivos Odoo do storage local para S3'
    )
    parser.add_argument('-d', '--database', required=True, help='Nome do banco de dados Odoo')
    parser.add_argument('-e', '--endpoint', required=True, help='Endpoint S3 (ex: https://nyc3.digitaloceanspaces.com)')
    parser.add_argument('-k', '--access-key', required=True, help='Access Key S3')
    parser.add_argument('-s', '--secret-key', required=True, help='Secret Key S3')
    parser.add_argument('-b', '--bucket', required=True, help='Nome do bucket S3')
    parser.add_argument('-r', '--region', default='nyc3', help='Região S3 (default: nyc3)')
    parser.add_argument('--dry-run', action='store_true', help='Executar em modo simulação (sem fazer upload)')

    args = parser.parse_args()

    logger.info("=" * 70)
    logger.info("Migração de Arquivos para S3/DigitalOcean Spaces")
    logger.info("=" * 70)
    logger.info(f"Banco de dados: {args.database}")
    logger.info(f"Bucket S3: {args.bucket}")
    logger.info(f"Modo: {'SIMULAÇÃO (dry-run)' if args.dry_run else 'REAL (vai fazer upload)'}")
    logger.info("")

    # Inicializar cliente S3
    s3_client = boto3.client(
        's3',
        endpoint_url=args.endpoint,
        aws_access_key_id=args.access_key,
        aws_secret_access_key=args.secret_key,
        region_name=args.region,
    )

    # Testar conexão
    try:
        s3_client.head_bucket(Bucket=args.bucket)
        logger.info(f"✓ Conexão com S3 bem-sucedida")
    except Exception as e:
        logger.error(f"✗ Erro ao conectar com S3: {str(e)}")
        sys.exit(1)

    # Encontrar arquivos locais do Odoo
    filestore_path = f"/opt/odoo/var/filestore/{args.database}"
    if not os.path.exists(filestore_path):
        logger.error(f"✗ Diretório não encontrado: {filestore_path}")
        sys.exit(1)

    logger.info(f"✓ Diretório encontrado: {filestore_path}")
    logger.info("")

    # Varrer arquivos
    total_files = 0
    uploaded_files = 0
    failed_files = 0
    total_size = 0

    logger.info("Processando arquivos...")

    for root, dirs, files in os.walk(filestore_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, filestore_path)
            file_size = os.path.getsize(file_path)

            total_files += 1
            total_size += file_size

            s3_key = f"documents/migrated/{relative_path}"

            try:
                if not args.dry_run:
                    # Upload para S3
                    with open(file_path, 'rb') as f:
                        s3_client.put_object(
                            Bucket=args.bucket,
                            Key=s3_key,
                            Body=f.read(),
                            Metadata={
                                'migrated_date': datetime.now().isoformat(),
                                'original_path': relative_path,
                            }
                        )
                    uploaded_files += 1
                    logger.info(f"  ✓ {relative_path} ({file_size / 1024:.1f} KB)")
                else:
                    logger.info(f"  [SIM] {relative_path} ({file_size / 1024:.1f} KB)")
                    uploaded_files += 1

            except Exception as e:
                failed_files += 1
                logger.error(f"  ✗ {relative_path}: {str(e)}")

    logger.info("")
    logger.info("=" * 70)
    logger.info("RESUMO DA MIGRAÇÃO")
    logger.info("=" * 70)
    logger.info(f"Total de arquivos: {total_files}")
    logger.info(f"Arquivos processados: {uploaded_files}")
    logger.info(f"Falhas: {failed_files}")
    logger.info(f"Tamanho total: {total_size / 1024 / 1024:.1f} MB")
    logger.info("")

    if args.dry_run:
        logger.info("ℹ Modo simulação - nenhum arquivo foi realmente enviado")
        logger.info("Execute sem --dry-run para fazer upload dos arquivos")
    else:
        logger.info("✓ Migração concluída!")

    logger.info("")

    # Próximos passos
    logger.info("Próximos passos:")
    logger.info("1. Fazer backup dos arquivos locais antes de deletar")
    logger.info("2. Atualizar banco de dados: UPDATE ir_attachment SET storage_location = 's3'")
    logger.info("3. Testar download de alguns arquivos")
    logger.info("4. Após confirmar, deletar /opt/odoo/var/filestore/{args.database}")

    return 0 if failed_files == 0 else 1


if __name__ == '__main__':
    sys.exit(main())