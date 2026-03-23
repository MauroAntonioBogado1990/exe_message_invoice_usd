# -*- coding: utf-8 -*-
from odoo import models, api, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('currency_id')
    def _onchange_currency_legal_terms(self):
        """
        Agrega términos y condiciones automáticos para facturas en USD.
        """
        # Definimos el texto legal
        terminos_usd = (
            "Esta factura es emitida y debe ser pagada en dólares estadounidenses. "
            "Para el caso que la misma sea pagada en moneda nacional de curso legal, "
            "los importes serán recibidos a cuenta, tomándose al tipo de cambio vendedor "
            "del Banco Nación Argentina del día de la acreditación efectiva del pago y "
            "luego se emitirá N/C o N/D según corresponda, debiendo ser cancelada dentro "
            "de los 7 días de su emisión."
        )

        for rec in self:
            # Verificamos si es una factura de cliente y si la moneda es USD
            if rec.move_type in ['out_invoice', 'out_refund'] and rec.currency_id.name == 'USD':
                # Si el campo está vacío o tiene el texto por defecto, lo reemplazamos
                if not rec.narration or rec.narration == '':
                    rec.narration = terminos_usd
            elif rec.currency_id.name == 'ARS':
                # Opcional: Limpiar si vuelve a ARS y el texto es el de USD
                if rec.narration == terminos_usd:
                    rec.narration = False