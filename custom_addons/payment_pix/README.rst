=====================================
Payment Provider: PIX (BACEN) — Odoo 19
=====================================

.. contents:: Índice
   :depth: 3
   :local:

Visão Geral
===========

O módulo **payment_pix** adiciona o sistema de pagamento instantâneo **PIX do Banco Central do Brasil**
ao Odoo 19, cobrindo dois fluxos distintos:

1. **Pagamentos online (portal/website)** — o cliente escolhe PIX na tela de checkout, recebe o
   QR Code e o código "Copia e Cola" gerados dinamicamente por transação, e conclui o pagamento
   pelo aplicativo do seu banco. O operador confirma manualmente o recebimento no Odoo.

2. **Registro contábil de movimentos PIX** — entradas (recebimentos de clientes) e saídas
   (pagamentos a fornecedores) registradas manualmente, com rastreamento de Chave PIX, ID E2E
   e lançamentos contábeis detalhados mostrando **de qual conta saiu** e **para qual conta foi**.

O módulo **não** requer integração com API de nenhum PSP ou banco. Tudo funciona de forma
offline/manual, seguindo o padrão EMV/BR Code definido pelo BACEN.

Funcionalidades
===============

Provedor de Pagamento Online
-----------------------------

- QR Code PIX gerado **por transação** com valor e referência do Odoo embutidos
- Formato EMV/BR Code conforme especificação do Banco Central do Brasil
- CRC16-CCITT calculado automaticamente
- **PIX Copia e Cola** — string BR Code completa para colar no app do banco
- Campo *Nome do Recebedor* e *Cidade* normalizados para ASCII (padrão BACEN)
- Validação que impede ativar o provedor sem Chave PIX, Nome e Cidade configurados
- Suporte a todos os tipos de chave: CPF, CNPJ, E-mail, Telefone, Chave Aleatória (EVP)
- Mensagem de instruções (*pending_msg*) gerada automaticamente com a chave PIX

Rastreamento Contábil
----------------------

- Campo **"Diário PIX"** no ``account.journal`` para marcar o diário dedicado a movimentos PIX
- Campos adicionais no ``account.payment``:

  - **ID E2E BACEN** — identificador de transação End-to-End para rastreabilidade
  - **Chave PIX do Parceiro** — chave do recebedor (saídas) ou pagador (entradas)
  - **Tipo de Chave** do parceiro
  - **Conta Origem** — de onde o dinheiro saiu (computado)
  - **Conta Destino** — para onde o dinheiro foi (computado)

- Menu dedicado **Contabilidade → PIX** com visões separadas para Entradas e Saídas
- Lista de movimentos PIX com colunas de Conta Origem e Conta Destino
- Filtros e agrupamentos por tipo, status, parceiro e período

Lógica Contábil (Conta Origem / Conta Destino)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-------------------------------+-------------------------------+-------------------------------+
| Tipo de Movimento             | Conta Origem (saiu de)        | Conta Destino (foi para)      |
+===============================+===============================+===============================+
| Entrada PIX (recebimento)     | Conta a Receber do cliente    | Conta PIX (banco)             |
+-------------------------------+-------------------------------+-------------------------------+
| Saída PIX (pagamento)         | Conta PIX (banco)             | Conta a Pagar ao fornecedor   |
+-------------------------------+-------------------------------+-------------------------------+

Dependências
============

+-------------------+--------------------------------------------------------------+
| Módulo            | Razão                                                        |
+===================+==============================================================+
| ``payment_custom``| Base para provedores de pagamento offline (modo custom)      |
+-------------------+--------------------------------------------------------------+
| ``account_payment``| Integração ``payment.provider`` ↔ ``account.payment``       |
+-------------------+--------------------------------------------------------------+

Biblioteca Python:

- ``qrcode`` — geração da imagem QR Code (já inclusa nas dependências do Odoo)
- ``unicodedata`` — normalização ASCII do nome/cidade (stdlib Python)

Instalação
==========

1. Copie a pasta ``payment_pix`` para o diretório de addons customizados do seu Odoo
   (ex.: ``custom_addons/``).

2. Certifique-se de que o caminho está listado em ``addons_path`` no ``odoo.conf``::

    addons_path = /caminho/para/odoo/addons, /caminho/para/custom_addons

3. Atualize a lista de módulos::

    Configurações → Módulos → Atualizar Lista de Módulos

4. Instale o módulo buscando por **"PIX"** em Configurações → Módulos.

Configuração
============

Passo 1 — Criar o Diário PIX
------------------------------

1. Acesse **Contabilidade → Configuração → Diários**.
2. Clique em **Novo**.
3. Preencha:

   - **Nome**: ``PIX``
   - **Tipo**: ``Banco``
   - **Moeda**: ``BRL``
   - **Conta de Débito/Crédito padrão**: selecione ou crie uma conta do tipo
     *Ativos Circulantes / Banco e Dinheiro* (ex.: ``1.1.2.03 - Banco PIX``).

4. Na aba **Avançado**, marque o campo **"Diário PIX"**.
5. Salve.

.. note::
   O campo "Diário PIX" garante que todos os pagamentos registrados neste diário
   apareçam no menu **Contabilidade → PIX** e tenham os campos de rastreamento PIX habilitados.

Passo 2 — Configurar o Provedor PIX
-------------------------------------

1. Acesse **Contabilidade → Configuração → Provedores de Pagamento**.
2. Clique no registro **PIX**.
3. Preencha os campos obrigatórios:

   - **Tipo de Chave**: selecione o tipo da sua chave PIX
   - **Chave PIX**: informe a chave cadastrada no Banco Central
   - **Nome do Recebedor**: nome exibido no QR Code (máx. 25 caracteres, sem acentos)
   - **Cidade do Recebedor**: cidade (máx. 15 caracteres, sem acentos)

4. Clique em **"Recarregar Mensagem PIX"** para gerar a mensagem de instrução.
5. Em **Diário**, selecione o diário PIX criado no Passo 1.
6. Mude o **Estado** para **Habilitado**.

.. warning::
   O provedor não pode ser ativado sem Chave PIX, Nome e Cidade configurados.
   Uma validação impedirá a ativação e exibirá mensagem de erro.

Passo 3 — Publicar no Website (opcional)
-----------------------------------------

Se utilizar o módulo ``website_payment``:

1. No formulário do provedor PIX, marque **"Publicado"**.
2. O PIX aparecerá como opção de pagamento no checkout do website.

Uso
===

Pagamentos Online (Portal / Website)
--------------------------------------

Fluxo do cliente:

1. O cliente acessa o link de pagamento (fatura ou pedido de venda).
2. Seleciona **PIX** como forma de pagamento e clica em **Pagar**.
3. A tela de confirmação exibe:

   - **Instruções** com a chave PIX do recebedor
   - **QR Code PIX** gerado com o valor exato e a referência do Odoo
   - **PIX Copia e Cola** — a string BR Code completa para colar no app

4. O cliente paga pelo app do banco.
5. O operador verifica o recebimento no extrato PIX e **confirma o pagamento** no Odoo:
   acesse a transação em **Contabilidade → Pagamentos** e clique em **Confirmar**.
6. O pagamento é lançado no diário PIX e reconciliado com a fatura.

Registro de Entradas PIX (Recebimentos)
-----------------------------------------

Para registrar um recebimento PIX que não veio pelo portal:

1. Acesse **Contabilidade → PIX → Entradas (Recebimentos)**.
2. Clique em **Novo**.
3. Preencha:

   - **Data**: data do crédito PIX
   - **Parceiro**: cliente
   - **Valor**: valor recebido
   - **Diário**: selecione o diário PIX
   - **Chave PIX do Parceiro**: chave do pagador (opcional, para rastreamento)
   - **ID E2E BACEN**: código E2E da notificação PIX (opcional)
   - **Memo**: descrição do pagamento

4. Clique em **Confirmar**.

O Odoo criará o lançamento contábil:

.. code-block:: text

   Débito:  Conta PIX (banco)         R$ XXX,XX
   Crédito: Contas a Receber          R$ XXX,XX

Registro de Saídas PIX (Pagamentos a Fornecedores)
-----------------------------------------------------

Para registrar um pagamento PIX enviado a um fornecedor:

1. Acesse **Contabilidade → PIX → Saídas (Pagamentos)**.
2. Clique em **Novo**.
3. Preencha:

   - **Data**: data do débito PIX
   - **Parceiro**: fornecedor
   - **Valor**: valor pago
   - **Diário**: selecione o diário PIX
   - **Chave PIX do Parceiro**: chave PIX do fornecedor recebedor
   - **ID E2E BACEN**: código E2E da confirmação do banco
   - **Memo**: descrição / referência da nota fiscal

4. Clique em **Confirmar**.

O Odoo criará o lançamento contábil:

.. code-block:: text

   Débito:  Contas a Pagar            R$ XXX,XX
   Crédito: Conta PIX (banco)         R$ XXX,XX

.. tip::
   Alternativamente, você pode registrar pagamentos PIX diretamente a partir da
   **fatura do fornecedor** → botão **"Registrar Pagamento"** → selecione o diário PIX.
   Os campos PIX ficarão visíveis no formulário.

Consulta de Movimentos PIX
---------------------------

Acesse **Contabilidade → PIX → Todos os Movimentos**.

A lista exibe:

- Data, Referência, Parceiro
- Tipo: **Entrada** (recebimento) ou **Saída** (pagamento)
- **Conta Origem** — de onde saiu o dinheiro
- **Conta Destino** — para onde foi o dinheiro
- Valor, Chave PIX do Parceiro, ID E2E, Status

Use os filtros **Entradas** / **Saídas** ou agrupe por Parceiro, Data ou Status.

Detalhes Técnicos
=================

Geração do QR Code PIX (BR Code / EMV)
-----------------------------------------

O módulo implementa o formato **EMV QR Code** (BR Code) conforme o
*Manual de Padrões para Iniciação do PIX* do Banco Central do Brasil.

Estrutura do payload::

   000201                       Payload Format Indicator (fixo: "01")
   010212                       Point of Initiation Method (12 = QR dinâmico por transação)
   26NN                         Merchant Account Information
     0014BR.GOV.BCB.PIX         GUI (identificador do arranjo PIX)
     01NN<chave_pix>            Chave PIX do recebedor
   520400005303986              MCC (0000) + Currency (986 = BRL)
   5406<valor>                  Transaction Amount (formato: "1234.56")
   5802BR                       Country Code
   5913<nome>                   Merchant Name (ASCII, máx. 25 chars)
   6009<cidade>                 Merchant City (ASCII, máx. 15 chars)
   6218                         Additional Data Field
     0514<txid>                 Transaction ID (referência do Odoo, máx. 25 chars)
   6304<CRC>                    CRC16-CCITT em hexadecimal maiúsculo (4 chars)

CRC16-CCITT::

   Polinômio : 0x1021
   Valor inicial: 0xFFFF
   Calculado sobre todo o payload incluindo o prefixo "6304"

O método ``_pix_build_br_code(amount, txid)`` em ``models/payment_provider.py`` executa
essa lógica. O método ``_pix_build_qr_code_base64(amount, txid)`` utiliza a biblioteca
``qrcode`` para gerar a imagem PNG e retornar uma *data URI* base64.

Modelos Estendidos
-------------------

+-------------------------+----------------------------------------------------------+
| Modelo                  | Campos adicionados                                       |
+=========================+==========================================================+
| ``payment.provider``    | ``custom_mode`` += ``'pix'``                             |
|                         | ``pix_key_type``, ``pix_key``                            |
|                         | ``pix_merchant_name``, ``pix_merchant_city``             |
+-------------------------+----------------------------------------------------------+
| ``account.journal``     | ``is_pix``                                               |
+-------------------------+----------------------------------------------------------+
| ``account.payment``     | ``is_pix`` (computed), ``pix_e2e_id``                    |
|                         | ``pix_partner_key``, ``pix_partner_key_type``            |
|                         | ``pix_conta_origem_id`` (computed)                       |
|                         | ``pix_conta_destino_id`` (computed)                      |
+-------------------------+----------------------------------------------------------+

Métodos Principais
-------------------

``payment.provider``
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   _pix_build_br_code(amount, txid) -> str
   """
   Gera a string EMV/BR Code para o QR Code PIX.
   Retorna '' se pix_key não estiver configurada.
   """

   _pix_build_qr_code_base64(amount, txid) -> str | False
   """
   Retorna a imagem QR Code como data URI PNG (base64).
   Retorna False se pix_key não estiver configurada ou em caso de erro.
   """

   _pix_update_pending_msg() -> None
   """
   Atualiza o pending_msg do provedor com as instruções PIX e a chave configurada.
   Chamado via botão "Recarregar Mensagem PIX" ou pelo hook de instalação.
   """

   action_recompute_pending_msg() -> None
   """
   Override do payment_custom: delega para _pix_update_pending_msg()
   nos provedores PIX antes de chamar o super() para os demais.
   """

``account.payment``
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   _compute_is_pix()
   """Verdadeiro quando journal_id.is_pix == True."""

   _compute_pix_flow_accounts()
   """
   Computa pix_conta_origem_id e pix_conta_destino_id a partir de
   payment_type, journal_id.default_account_id e destination_account_id.
   """

Templates QWeb
--------------

+-------------------------------------------+------------------------------------------------------+
| Template ID                               | Descrição                                            |
+===========================================+======================================================+
| ``payment_pix.payment_pix_state_header``  | Herda ``payment_custom.custom_state_header``:        |
|                                           | substitui geração do QR Code para usar BR Code PIX   |
|                                           | e adiciona seção "PIX Copia e Cola"                  |
+-------------------------------------------+------------------------------------------------------+

Hooks de Instalação
-------------------

- ``post_init_hook`` — chama ``setup_provider(env, 'custom', custom_mode='pix')``
  para ativar o provedor PIX recém-criado.
- ``uninstall_hook`` — chama ``reset_payment_provider(env, 'custom', custom_mode='pix')``
  para desativar o provedor ao desinstalar o módulo.

Limitações Conhecidas
=====================

1. **Confirmação manual** — o módulo não possui webhook ou integração com API de banco.
   O operador precisa confirmar manualmente cada recebimento PIX no Odoo após verificar
   o extrato no aplicativo do banco ou no sistema do PSP.

2. **QR Code estático por chave** — o QR Code é gerado a partir da chave PIX configurada
   no provedor. Não há geração de QR Codes via API BACEN/PSP com expiração automática.

3. **Sem confirmação automática** — transações ficam no estado ``pending`` até confirmação
   manual. Para confirmação automática via webhook, é necessário integrar com um PSP
   (ex.: Efipay, PagSeguro, Mercado Pago, Stripe).

4. **Uma chave PIX por empresa** — o provedor suporta uma única chave PIX por registro.
   Para múltiplas chaves ou empresas, crie múltiplos provedores (multi-company).

Changelog
=========

**v1.0** (2026-04-25)
   - Provedor de pagamento PIX para portal/website (modo offline/manual)
   - Geração de QR Code BR Code (EMV) com CRC16-CCITT
   - PIX Copia e Cola na tela de confirmação de pagamento
   - Campo ``is_pix`` no ``account.journal``
   - Campos ``pix_e2e_id``, ``pix_partner_key`` no ``account.payment``
   - Campos computados ``pix_conta_origem_id`` / ``pix_conta_destino_id``
   - Menu Contabilidade → PIX com visões de Entradas e Saídas
   - Extensão do formulário de pagamento com campos PIX

Suporte
=======

Para dúvidas, melhorias ou reportar problemas, consulte a equipe de desenvolvimento interno
ou abra uma issue no repositório do projeto.

Licença
=======

LGPL-3 — Lesser General Public License v3.