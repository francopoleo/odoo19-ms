import base64

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CondominiumCnabService(models.AbstractModel):
    _name = "property.condominium.cnab.service"
    _description = "Serviço CNAB do Condomínio"

    def _get_profile(self, complex_rec):
        profile = complex_rec.cnab_profile_id
        if not profile:
            raise UserError(_("Configure o perfil CNAB no complexo."))
        return profile

    def _format_line(self, tag, value, width=120):
        text = f"{tag}|{value}"
        return text[:width].ljust(width)

    def generate_remittance(self, charges):
        if not charges:
            raise UserError(_("Selecione ao menos uma cobrança."))
        complex_rec = charges[0].complex_id
        profile = self._get_profile(complex_rec)
        header = self._format_line("HEADER", f"{profile.bank_code}|{profile.cnab_type}|{complex_rec.name}")
        lines = [header]
        for charge in charges:
            lines.append(self._format_line(
                "DETAIL",
                "|".join([
                    str(charge.id),
                    charge.partner_id.name or "",
                    charge.unit_id.display_name_full or charge.unit_id.name or "",
                    fields.Date.to_string(charge.due_date) if charge.due_date else "",
                    f"{charge.amount_base or 0.0:.2f}",
                    f"{charge.amount_fine or 0.0:.2f}",
                    f"{charge.amount_interest or 0.0:.2f}",
                    f"{charge.amount_total or 0.0:.2f}",
                ]),
            ))
        lines.append(self._format_line("TRAILER", str(len(charges))))
        payload = "\n".join(lines).encode("utf-8")
        filename = f"cnab_{profile.bank_code}_{profile.cnab_type}_{fields.Date.today()}.txt"
        return filename, payload

    def generate_return_file(self, charges):
        filename, payload = self.generate_remittance(charges)
        return filename.replace(".txt", "_retorno.txt"), payload

    def import_return(self, content):
        lines = content.decode("utf-8", errors="ignore").splitlines()
        Charge = self.env["property.condominium.charge"]
        updated = 0
        for line in lines:
            parts = line.split("|")
            if len(parts) < 3 or parts[0] != "DETAIL":
                continue
            charge_id = int(parts[1] or 0)
            status = (parts[2] or "").upper()
            charge = Charge.browse(charge_id).exists()
            if not charge:
                continue
            if status in ("PAID", "PAGO", "LIQUIDADO"):
                charge.action_mark_paid()
                charge.remittance_state = "returned"
            elif status in ("SENT", "ENVIADO"):
                charge.remittance_state = "sent"
            updated += 1
        return updated
