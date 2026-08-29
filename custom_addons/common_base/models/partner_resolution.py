from email.utils import parseaddr
from odoo import api, models

# Exportado para uso em Selection fields de outros módulos
MATCH_SOURCES = [
    ('email_exact', 'E-mail Exato'),
    ('email_ilike', 'E-mail (normalizado)'),
    ('tenant_email', 'E-mail de Locatário'),
    ('owner_email', 'E-mail de Proprietário'),
    ('lead_email', 'E-mail de Lead'),
    ('phone_exact', 'Telefone Exato'),
    ('new', 'Contato Criado'),
    ('manual', 'Vinculação Manual'),
]


class ResPartnerContactResolver(models.Model):
    _inherit = 'res.partner'

    @api.model
    def resolve_contact(self, email=None, phone=None, create_if_missing=True):
        """Resolve res.partner a partir de atributos de comunicação recebida.

        Retorna (partner, source, confidence, created):
          partner    — res.partner recordset (pode ser vazio se create_if_missing=False)
          source     — chave de MATCH_SOURCES indicando a estratégia vencedora
          confidence — int 0-100 (100 = email exato, 0 = contato criado agora)
          created    — True quando um novo res.partner foi criado nesta chamada

        Estratégias em ordem de prioridade:
          1. email =  (case-sensitive, usa índice btree)         → 100
          2. email =ilike (case-insensitive)                     →  90
          3. _resolve_contact_extended() — hook para submodules  → var.
          4. phone/mobile = exato                                →  75
          5. criar novo contato                                  →   0
        """
        email_clean = (email or '').strip().lower()
        phone_clean = (phone or '').strip()

        if not email_clean and not phone_clean:
            return (self.env['res.partner'].browse(), 'new', 0, False)

        # Cache por requisição — evita bater no banco múltiplas vezes
        # para o mesmo remetente dentro do mesmo request HTTP
        cache_key = f'{email_clean}|{phone_clean}'
        if not hasattr(self.env.cr, '_contact_resolver_cache'):
            self.env.cr._contact_resolver_cache = {}
        cached = self.env.cr._contact_resolver_cache.get(cache_key)
        if cached is not None:
            return cached

        P = self.sudo()

        if email_clean:
            # Estratégia 1: exato — usa o índice btree sem scan completo
            p = P.search([('email', '=', email_clean)], limit=1)
            if p:
                return self._resolver_cache(cache_key, p, 'email_exact', 100)

            # Estratégia 2: case-insensitive
            p = P.search([('email', '=ilike', email_clean)], limit=1)
            if p:
                return self._resolver_cache(cache_key, p, 'email_ilike', 90)

        # Estratégia 3: hook de extensão (property_core injeta tenant/owner/lead)
        ext_partner, ext_source, ext_confidence = self._resolve_contact_extended(
            email=email_clean, phone=phone_clean
        )
        if ext_partner:
            return self._resolver_cache(cache_key, ext_partner, ext_source, ext_confidence)

        # Estratégia 4: telefone exato
        if phone_clean:
            p = P.search(
                ['|', ('phone', '=', phone_clean), ('mobile', '=', phone_clean)], limit=1
            )
            if p:
                return self._resolver_cache(cache_key, p, 'phone_exact', 75)

        # Estratégia 5: criar novo contato
        if create_if_missing:
            parsed_name, parsed_email = parseaddr(email or '')
            vals = {
                'name': parsed_name or parsed_email or email_clean or phone_clean or 'Desconhecido',
            }
            if parsed_email or email_clean:
                vals['email'] = parsed_email or email_clean
            if phone_clean:
                vals['phone'] = phone_clean
            p = P.create(vals)
            return self._resolver_cache(cache_key, p, 'new', 0, created=True)

        return (self.env['res.partner'].browse(), 'new', 0, False)

    @api.model
    def _resolve_contact_extended(self, email=None, phone=None):
        """Hook para módulos filhos adicionarem estratégias de resolução.

        Deve retornar (partner, source, confidence) ou (False, None, 0).
        Exemplo em property_core: busca em property.tenant, property.owner, property.lead.
        """
        return (False, None, 0)

    @api.model
    def _resolver_cache(self, key, partner, source, confidence, created=False):
        result = (partner, source, confidence, created)
        self.env.cr._contact_resolver_cache[key] = result
        return result