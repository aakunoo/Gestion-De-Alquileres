from odoo import models, fields, api
from odoo.exceptions import UserError

class javvGenerarMatriculaWizard(models.TransientModel):
    _name = 'javv.generar_matricula_wizard'
    _description = 'Asistente para Generar la Matrícula'

    vehiculo_id = fields.Many2one(
        'javv.vehiculos',
        string="Vehículo",
        required=True
    )
    numeros = fields.Char(string="Números (4)", size=4)
    letras = fields.Char(string="Letras (3)", size=3)

    def action_aceptar(self):
        """
        Concatenar numeros + letras y actualizar la matrícula del vehículo.
        """
        self.ensure_one()  # Asegura un único registro wizard
        if not (self.numeros and self.letras):
            raise UserError("Debes indicar números y letras para generar la matrícula.")

        nueva_matricula = f"{self.numeros}{self.letras}".upper()

        # Actualizar el vehículo
        self.vehiculo_id.write({'matricula': nueva_matricula})

        # Cerrar wizard
        return {'type': 'ir.actions.act_window_close'}

    def action_cancelar(self):
        """Cerrar el wizard sin cambios."""
        return {'type': 'ir.actions.act_window_close'}
