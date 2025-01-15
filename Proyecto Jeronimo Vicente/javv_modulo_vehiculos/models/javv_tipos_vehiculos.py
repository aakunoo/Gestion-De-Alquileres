from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import random
from datetime import datetime


class javv_tipos_vehiculos(models.Model):
    _name = 'javv.tipos_vehiculos'
    _description = 'Tipos de vehículos'
    _order = "name asc"

    name = fields.Char(string="Nombre", required=True)
    clasificacion_energetica = fields.Selection([
        ('0', '0'),
        ('eco', 'Eco'),
        ('c', 'C'),
        ('b', 'B'),
        ('sin_clasificar', 'Sin clasificar')
    ], string="Clasificación energética", default='sin_clasificar')
    enganche_carro = fields.Boolean(string="Enganche para carro", default=False)

    @api.constrains('enganche_carro')
    def _check_enganche(self):
        for record in self:
            vehiculos = self.env['javv.vehiculos'].search([('tipo_vehiculo_id', '=', record.id)])
            for vehiculo in vehiculos:
                if record.enganche_carro and vehiculo.num_plazas < 4:
                    raise ValidationError('Los vehículos con enganche para carro deben tener al menos 4 plazas.')

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'El nombre del tipo de vehículo debe ser único.')
    ]

    vehiculos_ids = fields.One2many(
        'javv.vehiculos', 'tipo_vehiculo_id', string="Vehículos Relacionados"
    )

    def action_ver_alquileres(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Alquileres de Vehículos',
            'res_model': 'javv.alquileres_vehiculos',
            'view_mode': 'tree',
            'domain': [('vehiculo_id.tipo_vehiculo_id', '=', self.id)],
        }

    # Campo para contar alquileres relacionados
    alquileres_count = fields.Integer(string="Alquileres Relacionados", compute="_compute_alquileres_count")

    @api.depends('vehiculos_ids.alquileres_ids')
    def _compute_alquileres_count(self):
        for record in self:
            record.alquileres_count = sum(len(vehiculo.alquileres_ids) for vehiculo in record.vehiculos_ids)

    def action_estadisticas(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Alquileres Relacionados',
            'res_model': 'javv.alquileres_vehiculos',
            'view_mode': 'tree,form',
            'domain': [('vehiculo_id.tipo_vehiculo_id', '=', self.id)],
            'context': {'default_tipo_vehiculo_id': self.id},
        }

    kanban_clasificacion_display = fields.Char(
        string="Clasificación para Kanban",
        compute="_compute_kanban_clasificacion_display"
    )

    @api.depends('clasificacion_energetica', 'enganche_carro')
    def _compute_kanban_clasificacion_display(self):
        for record in self:
            display = []
            if record.clasificacion_energetica in ['0', 'eco']:
                display.append(f"Clasificación: {record.clasificacion_energetica}")
            if record.enganche_carro:
                display.append("Enganche para carro disponible")
            record.kanban_clasificacion_display = "\n".join(display)

    def action_open_clasificacion_wizard(self):
        self.ensure_one()
        return {
            'name': 'Elegir Clasificación',
            'type': 'ir.actions.act_window',
            'res_model': 'javv.clasificacion_energetica_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_tipo_vehiculo_id': self.id,
            }
        }

    @api.model
    def generate_tipo_vehiculo_sql(self):
        """
        Crea un nuevo registro de tipo de vehículo vía SQL,
        y luego lanza un UserError mostrando:
         - El ID, nombre y enganche_carro del registro creado.
         - Info de environment: Usuario actual (nombre e id),
           Compañía, e idioma/lenguaje.
        """
        # 1) Generar un número aleatorio entre 1 y 1000
        aleatorio = random.randint(1, 1000)
        nombre = f"tipo_ejemplo{aleatorio}"

        # 2) Insertar registro vía SQL:
        #    name, clasificacion_energetica=sin_clasificar, enganche_carro=False
        query = """
                INSERT INTO javv_tipos_vehiculos (name, clasificacion_energetica, enganche_carro, create_uid, create_date, write_uid, write_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
        vals = [
            nombre,
            'sin_clasificar',
            False,
            self.env.uid,  # create_uid
            datetime.now(),  # create_date
            self.env.uid,  # write_uid
            datetime.now()  # write_date
        ]
        self.env.cr.execute(query, vals)
        new_id = self.env.cr.fetchone()[0]  # Obtener el id retornado

        # 3) Leer el registro recién creado como un Recordset
        new_tipo = self.browse(new_id)

        # 4) Recolectar información para UserError
        usuario_actual = self.env.user
        compania = self.env.company
        msg = (f"Registro creado:\n"
               f"  - ID: {new_tipo.id}\n"
               f"  - Nombre: {new_tipo.name}\n"
               f"  - Enganche: {new_tipo.enganche_carro}\n"
               f"\n"
               f"Sobre el environment:\n"
               f"  - Usuario actual: {usuario_actual.name} (ID={usuario_actual.id})\n"
               f"  - Compañía: {compania.name}\n"
               f"  - Lenguaje: {usuario_actual.lang}\n")

        # 5) Lanzar excepción con los datos
        raise UserError(msg)