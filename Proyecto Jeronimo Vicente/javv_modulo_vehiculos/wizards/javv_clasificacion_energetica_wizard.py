from odoo import models, fields, api
from odoo.exceptions import UserError

class javvClasificacionEnergeticaWizard(models.TransientModel):
    _name = 'javv.clasificacion_energetica_wizard'
    _description = 'Asistente para Establecer la Clasificación Energética'

    tipo_vehiculo_id = fields.Many2one(
        'javv.tipos_vehiculos',
        string="Tipo de Vehículo",
        required=True
    )

    opcion_combustible = fields.Selection([
        ('op1', 'Eléctrico de batería'),
        ('op2', 'Eléctrico de autonomía extendida'),
        ('op3', 'Eléctrico híbrido enchufable'),
        ('op4', 'Híbrido no enchufable'),
        ('op5', 'Gas'),
        ('op6', 'Gasolina matriculado a partir de enero de 2006'),
        ('op7', 'Diésel matriculado a partir de septiembre de 2015'),
        ('op8', 'Gasolina matriculado entre 2001 y 2006'),
        ('op9', 'Diésel matriculado entre 2006 y 2015'),
        ('op10', 'Otros')
    ], string="Combustible")

    def action_aceptar(self):
        """
        Asigna la clasificación energética según
        la opción elegida en opcion_combustible.
        """
        self.ensure_one()
        if not self.opcion_combustible:
            raise UserError("Debes seleccionar una opción de combustible.")

        clasif = 'sin_clasificar'
        if self.opcion_combustible in ['op1', 'op2', 'op3']:
            clasif = '0'
        elif self.opcion_combustible in ['op4', 'op5']:
            clasif = 'eco'
        elif self.opcion_combustible in ['op6', 'op7']:
            clasif = 'c'
        elif self.opcion_combustible in ['op8', 'op9']:
            clasif = 'b'
        elif self.opcion_combustible == 'op10':
            clasif = 'sin_clasificar'

        self.tipo_vehiculo_id.write({'clasificacion_energetica': clasif})

        return {'type': 'ir.actions.act_window_close'}

    def action_cancelar(self):
        """Cerrar el asistente sin hacer nada."""
        return {'type': 'ir.actions.act_window_close'}
