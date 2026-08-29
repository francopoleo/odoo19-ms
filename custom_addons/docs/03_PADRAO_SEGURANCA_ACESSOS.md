# Padrão de Segurança e Acessos

## Princípios

| Princípio | Aplicação |
| --- | --- |
| Menor privilégio | Usuários veem apenas o necessário para operar. |
| Responsabilidade explícita | Registros com agenda devem ter responsável principal e equipe. |
| Auditoria | Evitar exclusão definitiva de registros operacionais. |
| Visibilidade por contexto | Agenda Geral e registros críticos consideram responsáveis, participantes e grupos administrativos. |

## Checklist por módulo

- [ ] Grupos de acesso definidos em `security/*.xml`.
- [ ] ACLs definidas em `security/ir.model.access.csv`.
- [ ] Record rules revisadas para multiempresa e responsabilidade.
- [ ] Menus disponíveis somente para grupos adequados.
- [ ] Fluxos críticos testados com usuário operacional e administrador.
