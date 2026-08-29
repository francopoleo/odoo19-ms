# Opções Completas do Módulo

Este arquivo lista as opções funcionais disponíveis no módulo. Os códigos técnicos são mantidos em inglês por padrão Odoo/desenvolvimento, mas os nomes exibidos ao usuário estão em português do Brasil.

## 1. Tipos de Aditivo

| Código | Nome |
| --- | --- |
| tenant_change | Troca de locatário |
| landlord_change | Troca de locador |
| guarantor_change | Troca de fiador/garantidor |
| assignment | Cessão de posição contratual |
| novation | Novação |
| rent_change | Alteração de aluguel |
| rent_increase | Aumento de aluguel |
| rent_reduction | Redução de aluguel |
| temporary_discount | Desconto temporário |
| permanent_discount | Desconto permanente |
| extra_charge | Acréscimo/cobrança adicional |
| charge_waiver | Renúncia/perdão de cobrança |
| billing_reschedule | Reprogramação de cobrança |
| debt_confession | Confissão/parcelamento de dívida |
| term_extension | Prorrogação de prazo |
| term_reduction | Redução de prazo |
| renewal | Renovação |
| early_termination | Rescisão antecipada |
| termination | Encerramento |
| partial_termination | Encerramento parcial |
| guarantee_change | Alteração de garantia |
| asset_area_change | Alteração de imóvel/área |
| purpose_change | Alteração de finalidade |
| index_change | Alteração de índice |
| payment_terms_change | Alteração de pagamento |
| expenses_change | Alteração de encargos/despesas |
| works_fitout | Obras, benfeitorias ou adaptação/implantação |
| sublocation_authorization | Autorização de sublocação |
| compliance_update | Ajuste jurídico/conformidade |
| force_majeure | Força maior / evento extraordinário |
| rectification | Retificação/Rerratificação |
| other | Outro |

## 2. Escopos de Aditivo

| Código | Nome |
| --- | --- |
| specific_clause | Cláusula específica |
| financial | Financeiro |
| term | Prazo/vigência |
| parties | Partes |
| asset | Imóvel/área |
| full_consolidation | Consolidação ampla |

## 3. Efeitos Econômicos

| Código | Nome |
| --- | --- |
| neutral | Neutro |
| increase | Acréscimo/a mais |
| decrease | Desconto/a menos |
| mixed | Misto |

## 4. Status de Aditivo

| Código | Nome |
| --- | --- |
| draft | Rascunho |
| legal_review | Revisão jurídica |
| commercial_review | Revisão comercial |
| financial_review | Revisão financeira |
| risk_review | Revisão de risco |
| approved | Aprovado |
| sent_to_signature | Enviado para assinatura |
| partially_signed | Parcialmente assinado |
| signed | Assinado |
| ready_to_apply | Pronto para aplicar |
| applied | Aplicado |
| rejected | Rejeitado |
| cancelled | Cancelado |
| archived | Arquivado |


## 5. Campos Controlados para Alterações do Contrato

A aba **Alterações** não exige mais digitação manual de campo técnico e rótulo. O usuário seleciona **Campo do Contrato**, e o módulo preenche os metadados automaticamente.

| Opção visível | Código técnico automático | Categoria automática | Tipo automático |
| --- | --- | --- | --- |
| Aluguel base atual | current_base_rent | Financeiro | Número |
| Aluguel original | original_monthly_rent | Financeiro | Número |
| Início vigente | current_start_date | Prazo | Data |
| Fim vigente | current_end_date | Prazo | Data |
| Desconto até | current_discount_until | Financeiro | Data |
| Dia de vencimento vigente | current_payment_day | Cobrança | Número |
| Índice de reajuste vigente | current_adjustment_index | Financeiro | Texto |
| Locatário atual | current_partner_id | Partes | Contato |
| Locatário original | original_partner_id | Partes | Contato |
| Garantia vigente | current_guarantee_type | Garantia | Texto |
| Finalidade vigente | current_purpose | Imóvel | Texto |
| Foro vigente | current_jurisdiction | Jurídico | Texto |
| Status jurídico | legal_status | Jurídico | Texto |
| Status operacional | operational_status | Operacional | Texto |
| Termos consolidados | consolidated_terms_html | Cláusula | Texto |
| Emitido por | issuer | Jurídico | Texto |

### Valores técnicos aceitos em campos de seleção

Para **Índice de reajuste vigente**, preencha o novo valor com um dos códigos abaixo:

| Código | Significado |
| --- | --- |
| none | Sem reajuste |
| igpm | IGP-M |
| ipca | IPCA |
| incc | INCC |
| fixed | Fixo |
| other | Outro |

Para **Status jurídico**, preencha o novo valor com um dos códigos abaixo:

| Código | Significado |
| --- | --- |
| draft | Rascunho |
| under_review | Em revisão |
| signed | Assinado |
| amended | Aditado |
| terminated | Encerrado |
| expired | Expirado |
| cancelled | Cancelado |

Para **Status operacional**, preencha o novo valor com um dos códigos abaixo:

| Código | Significado |
| --- | --- |
| pending_start | Aguardando início |
| active | Ativo |
| suspended | Suspenso |
| ending_soon | Próximo do fim |
| ended | Encerrado |
| cancelled | Cancelado |

## 6. Tipos de Cobrança da Tabela de Valores

| Código | Nome |
| --- | --- |
| base_rent | Aluguel-base |
| discount | Desconto |
| extra_charge | Acréscimo |
| rent_free_period | Período sem aluguel |
| grace_period | Carência |
| step_rent | Aluguel escalonado |
| percentage_rent | Aluguel percentual |
| minimum_rent | Aluguel mínimo |
| turnover_rent | Aluguel sobre faturamento |
| iptu | IPTU |
| condominium | Condomínio |
| cam | Despesas comuns |
| insurance | Seguro |
| utilities | Utilidades |
| marketing_fund | Fundo de marketing |
| service_charge | Taxa de serviço |
| penalty | Multa |
| interest | Juros |
| monetary_correction | Correção monetária |
| adjustment | Ajuste |
| credit | Crédito |
| other | Outro |

## 7. Tipos de Ajuste Financeiro

| Código | Nome |
| --- | --- |
| retroactive_credit | Crédito retroativo |
| retroactive_debit | Débito retroativo |
| overbilling_credit | Crédito por cobrança a maior |
| underbilling_debit | Débito por cobrança a menor |
| penalty_waiver | Perdão de multa |
| interest_waiver | Perdão de juros |
| settlement_credit | Crédito de acordo |
| settlement_debit | Débito de acordo |

## 8. Motivos de Aditivo


### Encargos e Despesas

| Nome | Código | Categoria | Descrição |
| --- | --- | --- | --- |
| Ajuste de auditoria | audit_adjustment | Encargos e Despesas | Ajuste decorrente de auditoria. |
| Alteração de despesas comuns | cam_charge_change | Encargos e Despesas | Mudança de despesas comuns, rateio ou despesas comuns. |
| Alteração de encargo de seguro | insurance_charge_change | Encargos e Despesas | Mudança de repasse ou responsabilidade de seguro. |
| Alteração de fundo de marketing | marketing_fund_change | Encargos e Despesas | Mudança de contribuição de marketing. |
| Alteração de fundo promocional | promotion_fund_change | Encargos e Despesas | Mudança de fundo promocional. |
| Alteração de responsabilidade por IPTU | iptu_responsibility_change | Encargos e Despesas | Mudança de responsabilidade por IPTU. |
| Alteração de responsabilidade por condomínio | condominium_responsibility_change | Encargos e Despesas | Mudança de responsabilidade por condomínio. |
| Alteração de taxa de serviço | service_charge_change | Encargos e Despesas | Mudança de taxa de serviço. |
| Alteração de teto de despesas | expense_cap_change | Encargos e Despesas | Mudança de cap de despesas. |
| Alteração de utilidades | utility_charge_change | Encargos e Despesas | Água, energia, gás, telecom etc. |
| Reconciliação de despesas comuns | common_cost_reconciliation | Encargos e Despesas | Apuração ou ajuste de rateios. |

### Encerramento

| Nome | Código | Categoria | Descrição |
| --- | --- | --- | --- |
| Acordo pós-rescisão | settlement_after_termination | Encerramento | Composição após encerramento. |
| Devolução de chaves | key_return | Encerramento | Devolução formal de chaves. |
| Distrato | distrato | Encerramento | Distrato consensual. |
| Encerramento | termination | Encerramento | Encerramento contratual. |
| Regularização de entrega | handover_regularization | Encerramento | Regularização de devolução/entrega de chaves. |
| Regularização de término | expiration_regularization | Encerramento | Regularização após término. |
| Rescisão | rescission | Encerramento | Rescisão por motivo contratual. |
| Rescisão amigável | mutual_termination | Encerramento | Encerramento por acordo. |
| Rescisão parcial | partial_termination | Encerramento | Encerramento parcial. |
| Rescisão por inadimplência | default_termination | Encerramento | Encerramento por descumprimento. |

### Financeiro

| Nome | Código | Categoria | Descrição |
| --- | --- | --- | --- |
| Abatimento | abatement | Financeiro | Abatimento parcial de cobrança. |
| Acordo financeiro | settlement | Financeiro | Composição financeira ou quitação. |
| Ajuste retroativo | retroactive_adjustment | Financeiro | Débito ou crédito retroativo. |
| Alteração da forma de pagamento | payment_method_change | Financeiro | Boleto, transferência, invoice etc. |
| Alteração da frequência de cobrança | billing_frequency_change | Financeiro | Mensal, trimestral, anual etc. |
| Alteração da multa por atraso | late_fee_change | Financeiro | Mudança de multa moratória. |
| Alteração de aluguel mínimo | minimum_rent_change | Financeiro | Mudança de aluguel mínimo garantido. |
| Alteração de aluguel percentual | percentage_rent_change | Financeiro | Mudança de percentual sobre faturamento. |
| Alteração de aluguel sobre faturamento | turnover_rent_change | Financeiro | Mudança do aluguel de varejo baseado em faturamento. |
| Alteração de aluguel variável | variable_rent_change | Financeiro | Mudança de cobrança variável. |
| Alteração de juros | interest_change | Financeiro | Mudança de juros de mora. |
| Alteração de penalidade | penalty_change | Financeiro | Mudança de penalidade contratual. |
| Alteração de índice de reajuste | index_change | Financeiro | Mudança de IPCA, IGPM, INCC ou índice contratual. |
| Alteração do dia de vencimento | payment_day_change | Financeiro | Mudança do dia de pagamento. |
| Aluguel escalonado | step_rent | Financeiro | Alteração programada de aluguel por etapas. |
| Aumento de aluguel | rent_increase | Financeiro | Aumento permanente do aluguel-base. |
| Carência | grace_period | Financeiro | Carência total ou parcial. |
| Crédito contratual | credit_memo | Financeiro | Geração de crédito a favor de uma parte. |
| Desconto permanente | permanent_discount | Financeiro | Desconto permanente sobre a cobrança. |
| Desconto temporário | temporary_discount | Financeiro | Desconto por período determinado. |
| Período sem aluguel | rent_free_period | Financeiro | Período de isenção de aluguel. |
| Reajuste extraordinário | extraordinary_adjustment | Financeiro | Reajuste fora da regra ordinária. |
| Reajuste fixo | fixed_adjustment | Financeiro | Percentual ou valor fixo de reajuste. |
| Redução de aluguel | rent_reduction | Financeiro | Redução permanente do aluguel-base. |
| Renúncia de cobrança | waiver | Financeiro | Perdão ou renúncia de valor. |

### Garantias

| Nome | Código | Categoria | Descrição |
| --- | --- | --- | --- |
| Alteração de caução | deposit_change | Garantias | Mudança de caução. |
| Alteração de fiança | surety_change | Garantias | Mudança de fiança. |
| Alteração de garantia bancária | bank_guarantee_change | Garantias | Mudança de carta fiança ou garantia bancária. |
| Alteração de garantia corporativa | corporate_guarantee_change | Garantias | Mudança de garantia empresarial. |
| Alteração de seguro-fiança | insurance_bond_change | Garantias | Mudança de seguro-fiança. |
| Liberação de caução | deposit_release | Garantias | Liberação total ou parcial de caução. |
| Liberação de garantia | guarantee_release | Garantias | Extinção ou liberação de garantia. |
| Reforço de caução | deposit_reinforcement | Garantias | Aumento ou complementação de caução. |
| Regularização de garantia vencida | guarantee_expiration_regularization | Garantias | Regularização ou renovação de garantia vencida. |
| Substituição de fiador | guarantor_replacement | Garantias | Substituição do fiador. |

### Geral

| Nome | Código | Categoria | Descrição |
| --- | --- | --- | --- |
| Cessão | assignment | Geral | Cessão de posição contratual ou direitos. |
| Consolidação | consolidation | Geral | Consolidação de termos vigentes. |
| Esclarecimento | clarification | Geral | Esclarecimento ou interpretação de cláusula. |
| Novação | novation | Geral | Substituição jurídica de obrigação anterior. |
| Outros | other | Geral | Motivo não classificado. |
| Ratificação | ratification | Geral | Confirmação de condições já pactuadas. |
| Rerratificação integral | full_restatement | Geral | Reformulação integral do instrumento. |
| Rerratificação parcial | partial_restatement | Geral | Reformulação parcial de cláusulas. |
| Retificação | rectification | Geral | Correção formal de informações do contrato. |

### Imóvel/Área

| Nome | Código | Categoria | Descrição |
| --- | --- | --- | --- |
| Alteração de depósito | storage_area_change | Imóvel/Área | Alteração de área de depósito. |
| Alteração de imóvel | asset_change | Imóvel/Área | Substituição do imóvel locado. |
| Alteração de vagas | parking_space_change | Imóvel/Área | Inclusão, exclusão ou troca de vagas. |
| Alteração de área comum | common_area_change | Imóvel/Área | Mudança de uso de área comum. |
| Atualização registral | registration_update | Imóvel/Área | Atualização em matrícula, inscrição ou registro. |
| Correção de metragem | measurement_correction | Imóvel/Área | Correção de área ou medição. |
| Devolução parcial | partial_return | Imóvel/Área | Devolução parcial da área. |
| Entrega parcial | partial_delivery | Imóvel/Área | Entrega parcial da área. |
| Expansão de área | area_expansion | Imóvel/Área | Aumento da área locada. |
| Redução de área | area_reduction | Imóvel/Área | Redução da área locada. |
| Retificação da descrição do imóvel | property_description_rectification | Imóvel/Área | Correção de endereço, matrícula, área ou cadastro. |
| Substituição de unidade | unit_substitution | Imóvel/Área | Troca de loja, sala, galpão ou unidade. |

### Jurídico/Conformidade

| Nome | Código | Categoria | Descrição |
| --- | --- | --- | --- |
| Ajuste por força maior | force_majeure_adjustment | Jurídico/Conformidade | Ajuste decorrente de força maior. |
| Alteração ambiental | environmental_obligation_change | Jurídico/Conformidade | Mudança de obrigação ambiental. |
| Alteração anticorrupção | anti_corruption_clause_change | Jurídico/Conformidade | Mudança de conformidade anticorrupção. |
| Alteração de arbitragem | arbitration_clause_change | Jurídico/Conformidade | Mudança de cláusula arbitral. |
| Alteração de cláusula LGPD | lgpd_clause_change | Jurídico/Conformidade | Mudança de tratamento de dados. |
| Alteração de confidencialidade | confidentiality_change | Jurídico/Conformidade | Mudança de confidencialidade. |
| Alteração de desapropriação | expropriation_clause_change | Jurídico/Conformidade | Mudança de cláusula de desapropriação. |
| Alteração de foro | jurisdiction_change | Jurídico/Conformidade | Mudança de foro. |
| Alteração de licenças | license_obligation_change | Jurídico/Conformidade | Mudança de licenças exigidas. |
| Alteração de obrigação de seguro | insurance_obligation_change | Jurídico/Conformidade | Mudança de obrigação de seguro. |
| Alteração de solução de disputas | dispute_resolution_change | Jurídico/Conformidade | Mudança de mediação, arbitragem ou foro. |

### Obras e Benfeitorias

| Nome | Código | Categoria | Descrição |
| --- | --- | --- | --- |
| Alteração de responsabilidade de manutenção | maintenance_responsibility_change | Obras e Benfeitorias | Mudança de obrigação de manutenção. |
| Aprovação de projeto técnico | technical_project_approval | Obras e Benfeitorias | Aprovação de projeto técnico ou arquitetônico. |
| Autorização de adaptação/implantação | fit_out_authorization | Obras e Benfeitorias | Autorização para obras de implantação. |
| Benfeitoria do locatário | tenant_improvement | Obras e Benfeitorias | Benfeitorias feitas pelo locatário. |
| Compensação por atraso de obra | work_delay_compensation | Obras e Benfeitorias | Compensação por atraso de entrega ou obra. |
| Obra do locador | landlord_work | Obras e Benfeitorias | Obra de responsabilidade do locador. |
| Obrigação de recomposição | reinstatement_obligation | Obras e Benfeitorias | Obrigação de devolver/recompor imóvel. |
| Obrigação de reforma | renovation_obligation | Obras e Benfeitorias | Inclusão de obrigação de reforma. |
| Reembolso de CAPEX | capex_reimbursement | Obras e Benfeitorias | Reembolso de investimento ou obra. |
| Verba de obra | construction_allowance | Obras e Benfeitorias | Concessão de verba para obra. |

### Partes

| Nome | Código | Categoria | Descrição |
| --- | --- | --- | --- |
| Alteração de contato | contact_change | Partes | Atualização de contatos contratuais. |
| Alteração de devedor solidário | solidary_debtor_change | Partes | Inclusão, substituição ou exclusão de responsável solidário. |
| Alteração de representante | representative_change | Partes | Mudança de representante legal ou procurador. |
| Alteração do responsável pelo faturamento | billing_responsible_change | Partes | Mudança do responsável pelo pagamento ou recebimento. |
| Fusão ou aquisição | merger_or_acquisition | Partes | Alteração decorrente de M&A. |
| Reorganização societária | corporate_reorganization | Partes | Cisão, incorporação, fusão ou alteração societária com impacto contratual. |
| Sucessão contratual | successor_party | Partes | Substituição por sucessor legal ou contratual. |
| Troca de fiador/garantidor | guarantor_change | Partes | Alteração de fiador ou garantidor. |
| Troca de locador | landlord_change | Partes | Substituição do locador. |
| Troca de locatário | tenant_change | Partes | Substituição do locatário. |

### Prazo

| Nome | Código | Categoria | Descrição |
| --- | --- | --- | --- |
| Alteração da data de posse | possession_date_change | Prazo | Mudança da data de posse ou entrega. |
| Alteração da data final | end_date_change | Prazo | Mudança da data de encerramento. |
| Alteração da data inicial | start_date_change | Prazo | Mudança da data de início. |
| Cláusula de renovação automática | automatic_renewal_clause | Prazo | Inclusão ou alteração de renovação automática. |
| Prorrogação de prazo | term_extension | Prazo | Extensão da vigência contratual. |
| Reativação | reactivation | Prazo | Reativação de contrato suspenso ou encerrado. |
| Redução de prazo | term_reduction | Prazo | Redução da vigência contratual. |
| Regularização de permanência após prazo | holdover_regularization | Prazo | Regularização de ocupação após fim do contrato. |
| Renovação | renewal | Prazo | Renovação contratual. |
| Renovação antecipada | early_renewal | Prazo | Renovação antes do fim da vigência. |
| Suspensão temporária | suspension_period | Prazo | Suspensão de vigência ou obrigações. |

### Uso e Operação

| Nome | Código | Categoria | Descrição |
| --- | --- | --- | --- |
| Alteração de finalidade | purpose_change | Uso e Operação | Mudança da finalidade da locação. |
| Alteração de horário de funcionamento | operating_hours_change | Uso e Operação | Mudança de horário de operação. |
| Alteração de marca | brand_change | Uso e Operação | Mudança de marca operada no imóvel. |
| Alteração de nome fantasia | trade_name_change | Uso e Operação | Mudança de nome fantasia. |
| Alteração de restrição de uso | use_restriction_change | Uso e Operação | Inclusão ou remoção de restrições de uso. |
| Autorização de cessão | cession_authorization | Uso e Operação | Autorização de cessão contratual. |
| Autorização de sublicença | sublicense_authorization | Uso e Operação | Autorização operacional específica. |
| Autorização de sublocação | sublocation_authorization | Uso e Operação | Autorização para sublocação. |
| Concessão de exclusividade | exclusivity_grant | Uso e Operação | Criação de exclusividade comercial. |
| Expansão de atividade | activity_expansion | Uso e Operação | Permissão para novas atividades. |
| Remoção de exclusividade | exclusivity_removal | Uso e Operação | Extinção de exclusividade comercial. |
| Restrição de atividade | activity_restriction | Uso e Operação | Restrição de atividades permitidas. |

## 8. Motivos Financeiros


### A mais / Débito / Acréscimo

| Nome | Código | Impacto |
| --- | --- | --- |
| Adicional por permanência após prazo | holdover_premium | A mais / Débito / Acréscimo |
| Aluguel escalonado crescente | step_up_rent | A mais / Débito / Acréscimo |
| Aluguel percentual sobre faturamento | turnover_percentage_rent | A mais / Débito / Acréscimo |
| Amortização de obras de adaptação | fit_out_amortization | A mais / Débito / Acréscimo |
| Aumento do aluguel mínimo | minimum_rent_increase | A mais / Débito / Acréscimo |
| Aumento do aluguel-base | base_rent_increase | A mais / Débito / Acréscimo |
| Cobrança de depósito/armazenagem | storage_charge | A mais / Débito / Acréscimo |
| Cobrança de energia elétrica | electricity_charge | A mais / Débito / Acréscimo |
| Cobrança de estacionamento | parking_charge | A mais / Débito / Acréscimo |
| Cobrança de fundo de marketing | marketing_fund_charge | A mais / Débito / Acréscimo |
| Cobrança de fundo promocional | promotion_fund_charge | A mais / Débito / Acréscimo |
| Cobrança de gás | gas_charge | A mais / Débito / Acréscimo |
| Cobrança de letreiro/sinalização | signage_charge | A mais / Débito / Acréscimo |
| Cobrança de multa | penalty_charge | A mais / Débito / Acréscimo |
| Cobrança de quiosque | kiosk_charge | A mais / Débito / Acréscimo |
| Cobrança de regularização de ocupação | occupancy_regularization_charge | A mais / Débito / Acréscimo |
| Cobrança de resíduos/lixo | waste_charge | A mais / Débito / Acréscimo |
| Cobrança de seguro de responsabilidade civil | liability_insurance_charge | A mais / Débito / Acréscimo |
| Cobrança de seguro incêndio | fire_insurance_charge | A mais / Débito / Acréscimo |
| Cobrança de serviço de limpeza | cleaning_service_charge | A mais / Débito / Acréscimo |
| Cobrança de serviço de manutenção | maintenance_service_charge | A mais / Débito / Acréscimo |
| Cobrança de serviço de segurança | security_service_charge | A mais / Débito / Acréscimo |
| Cobrança de variação cambial | currency_variation_charge | A mais / Débito / Acréscimo |
| Cobrança de água | water_charge | A mais / Débito / Acréscimo |
| Cobrança por aumento de metragem | measurement_increase_charge | A mais / Débito / Acréscimo |
| Cobrança por direito exclusivo | exclusive_right_charge | A mais / Débito / Acréscimo |
| Cobrança por expansão de área | area_expansion_charge | A mais / Débito / Acréscimo |
| Cobrança por unidade adicional | additional_unit_charge | A mais / Débito / Acréscimo |
| Cobrança por uso de marca | brand_use_charge | A mais / Débito / Acréscimo |
| Cobrança por uso de área comum | common_area_use_charge | A mais / Débito / Acréscimo |
| Correção de cobrança a menor | underbilling_correction | A mais / Débito / Acréscimo |
| Correção monetária | monetary_correction | A mais / Débito / Acréscimo |
| Diferença retroativa de índice | retroactive_index_difference | A mais / Débito / Acréscimo |
| Débito de acordo | settlement_debit | A mais / Débito / Acréscimo |
| Débito por reversão de fatura | invoice_reversal_debit | A mais / Débito / Acréscimo |
| Débito retroativo | retroactive_debit | A mais / Débito / Acréscimo |
| Excedente de aluguel variável | variable_rent_overage | A mais / Débito / Acréscimo |
| Juros por atraso | late_interest | A mais / Débito / Acréscimo |
| Multa de saída/rescisão | break_fee | A mais / Débito / Acréscimo |
| Multa por atraso | late_fee | A mais / Débito / Acréscimo |
| Reajuste anual por índice | annual_index_adjustment | A mais / Débito / Acréscimo |
| Reajuste percentual fixo | fixed_percentage_adjustment | A mais / Débito / Acréscimo |
| Recomposição tributária | tax_gross_up | A mais / Débito / Acréscimo |
| Recuperação de custo de obra | construction_cost_recovery | A mais / Débito / Acréscimo |
| Recuperação de despesas comuns | cam_recovery | A mais / Débito / Acréscimo |
| Recuperação de despesas comuns | common_expense_recovery | A mais / Débito / Acréscimo |
| Recuperação de investimento/CAPEX | capex_recovery | A mais / Débito / Acréscimo |
| Reembolso de IPTU | iptu_reimbursement | A mais / Débito / Acréscimo |
| Reembolso de benfeitoria do locatário | tenant_improvement_reimbursement | A mais / Débito / Acréscimo |
| Reembolso de condomínio | condominium_reimbursement | A mais / Débito / Acréscimo |
| Reembolso de custo de cobrança | collection_cost_reimbursement | A mais / Débito / Acréscimo |
| Reembolso de custo de fiança bancária | bank_guarantee_cost_reimbursement | A mais / Débito / Acréscimo |
| Reembolso de custo de licença | license_cost_reimbursement | A mais / Débito / Acréscimo |
| Reembolso de custo de seguro garantia | insurance_bond_cost_reimbursement | A mais / Débito / Acréscimo |
| Reembolso de custo jurídico | legal_cost_reimbursement | A mais / Débito / Acréscimo |
| Reembolso de imposto retido | withholding_tax_reimbursement | A mais / Débito / Acréscimo |
| Reembolso de obra do locador | landlord_work_reimbursement | A mais / Débito / Acréscimo |
| Reembolso de seguro | insurance_reimbursement | A mais / Débito / Acréscimo |
| Reembolso de utilidades | utility_reimbursement | A mais / Débito / Acréscimo |
| Reforço de caução/depósito de garantia | security_deposit_reinforcement | A mais / Débito / Acréscimo |
| Reversão de crédito | credit_reversal | A mais / Débito / Acréscimo |
| Revisão de aluguel a mercado | market_rent_review | A mais / Débito / Acréscimo |
| Revisão extraordinária do aluguel | extraordinary_rent_review | A mais / Débito / Acréscimo |
| Taxa administrativa | administrative_fee | A mais / Débito / Acréscimo |
| Taxa de cessão | assignment_fee | A mais / Débito / Acréscimo |
| Taxa de cobrança | collection_fee | A mais / Débito / Acréscimo |
| Taxa de faturamento/cobrança | billing_fee | A mais / Débito / Acréscimo |
| Taxa de gestão | management_fee | A mais / Débito / Acréscimo |
| Taxa de novação | novation_fee | A mais / Débito / Acréscimo |
| Taxa de renovação | renewal_fee | A mais / Débito / Acréscimo |
| Taxa de sublicenciamento | sublicensing_fee | A mais / Débito / Acréscimo |

### A menos / Crédito / Desconto

| Nome | Código | Impacto |
| --- | --- | --- |
| Abatimento | abatement | A menos / Crédito / Desconto |
| Carência | grace_period | A menos / Crédito / Desconto |
| Compensação contra caução/depósito | offset_against_deposit | A menos / Crédito / Desconto |
| Compensação por desapropriação | expropriation_compensation | A menos / Crédito / Desconto |
| Compensação por sinistro | casualty_compensation | A menos / Crédito / Desconto |
| Contribuição de investimento/CAPEX | capex_contribution | A menos / Crédito / Desconto |
| Correção de cobrança a maior | overbilling_correction | A menos / Crédito / Desconto |
| Crédito de acordo | settlement_credit | A menos / Crédito / Desconto |
| Crédito de acordo de rescisão | termination_settlement_credit | A menos / Crédito / Desconto |
| Crédito de compensação | compensation_credit | A menos / Crédito / Desconto |
| Crédito de despesa comum | common_expense_credit | A menos / Crédito / Desconto |
| Crédito de reconciliação de condomínio | condominium_reconciliation_credit | A menos / Crédito / Desconto |
| Crédito de reconciliação de despesas comuns | cam_reconciliation_credit | A menos / Crédito / Desconto |
| Crédito de sinistro de seguro | insurance_claim_credit | A menos / Crédito / Desconto |
| Crédito por atraso de obra do locador | landlord_work_delay_credit | A menos / Crédito / Desconto |
| Crédito por cancelamento de fatura | invoice_cancellation_credit | A menos / Crédito / Desconto |
| Crédito por devolução parcial | partial_return_credit | A menos / Crédito / Desconto |
| Crédito por falha de serviço | service_failure_credit | A menos / Crédito / Desconto |
| Crédito por indisponibilidade de unidade | unit_unavailability_credit | A menos / Crédito / Desconto |
| Crédito por redução de metragem | measurement_reduction_credit | A menos / Crédito / Desconto |
| Crédito por redução de área | area_reduction_credit | A menos / Crédito / Desconto |
| Crédito retroativo | retroactive_credit | A menos / Crédito / Desconto |
| Desconto comercial | commercial_discount | A menos / Crédito / Desconto |
| Desconto de acordo | settlement_discount | A menos / Crédito / Desconto |
| Desconto por fechamento parcial | partial_closure_discount | A menos / Crédito / Desconto |
| Desconto por fidelidade | loyalty_discount | A menos / Crédito / Desconto |
| Desconto por força maior | force_majeure_discount | A menos / Crédito / Desconto |
| Desconto por interferência de obra | construction_disruption_discount | A menos / Crédito / Desconto |
| Desconto por pagamento antecipado | early_payment_discount | A menos / Crédito / Desconto |
| Desconto por pandemia | pandemic_discount | A menos / Crédito / Desconto |
| Desconto por restrição de acesso | access_restriction_discount | A menos / Crédito / Desconto |
| Desconto por restrição operacional | operation_restriction_discount | A menos / Crédito / Desconto |
| Desconto temporário de aluguel | temporary_rent_discount | A menos / Crédito / Desconto |
| Incentivo de locação | lease_incentive | A menos / Crédito / Desconto |
| Incentivo de marketing | marketing_incentive | A menos / Crédito / Desconto |
| Incentivo de renovação | renewal_incentive | A menos / Crédito / Desconto |
| Incentivo de vacância/ocupação | vacancy_incentive | A menos / Crédito / Desconto |
| Incentivo promocional | promotion_incentive | A menos / Crédito / Desconto |
| Liberação de caução/depósito de garantia | security_deposit_release | A menos / Crédito / Desconto |
| Memorando de crédito | credit_memo | A menos / Crédito / Desconto |
| Perdão de aluguel | rent_waiver | A menos / Crédito / Desconto |
| Perdão de juros | interest_waiver | A menos / Crédito / Desconto |
| Perdão de multa | penalty_waiver | A menos / Crédito / Desconto |
| Perdão de multa por atraso | late_fee_waiver | A menos / Crédito / Desconto |
| Período gratuito de armazenagem | free_storage_period | A menos / Crédito / Desconto |
| Período gratuito de estacionamento | free_parking_period | A menos / Crédito / Desconto |
| Período gratuito de sinalização | free_signage_period | A menos / Crédito / Desconto |
| Período sem aluguel | rent_free_period | A menos / Crédito / Desconto |
| Redução permanente de aluguel | permanent_rent_reduction | A menos / Crédito / Desconto |
| Reembolso de custo de garantia | guarantee_cost_reimbursement | A menos / Crédito / Desconto |
| Repasse de crédito tributário | tax_credit_pass_through | A menos / Crédito / Desconto |
| Repasse de isenção de IPTU | iptu_exemption_pass_through | A menos / Crédito / Desconto |
| Subsídio de obra | construction_allowance | A menos / Crédito / Desconto |
| Subsídio para benfeitoria do locatário | tenant_improvement_allowance | A menos / Crédito / Desconto |
| Subsídio para obras de adaptação | fit_out_allowance | A menos / Crédito / Desconto |

### Neutro

| Nome | Código | Impacto |
| --- | --- | --- |

## 9. Tipos de Documento

| Nome | Código | Sequência |
| --- | --- | --- |
| Contrato Original | original_contract | 1 |
| Aditivo | amendment | 2 |
| Certificado de Assinatura | signature_certificate | 3 |
| Registro | registration | 4 |
| Notificação | notice | 5 |
| Suporte Financeiro | invoice_support | 6 |
| Documento de Aprovação | approval_document | 7 |
| Documento de Encerramento | termination_document | 8 |
| Outro | other | 9 |