{
    'name': 'Alquiler de Vehiculos',
    'summary': 'Gestión básica de vehículos.',
    'description': 'Módulo de prueba con el modelo principal de vehículos.',
    'author': 'Jerónimo Álvaro Vicente Vidal',
    'license': 'LGPL-3',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/javv_caracteristicas_vehiculos_views.xml',
        'views/javv_tipos_vehiculos_views.xml',
        'views/javv_vehiculos_views.xml',
        'views/javv_alquileres_vehiculos_views.xml',
        'views/javv_menus.xml',
        'views/javv_herencia_views.xml',
        'data/javv_neumaticos_data.xml',
        'reports/javv_informes_vehiculos.xml',
        'reports/javv_informes_alquileres_usuarios.xml',
        'reports/javv_informe_vehiculos_heredado.xml',
        'wizards/javv_generar_matricula_wizard_views.xml',
        'wizards/javv_clasificacion_energetica_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'javv_modulo_vehiculos/static/src/css/alquileres.css',
            'javv_modulo_vehiculos/static/src/css/custom_styles.css',

        ],
    },
    'application': True,
}
