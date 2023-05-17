COUNTRY_AREAS = {
    'ar': {
        'ar-caba': 'Ciudad Autónoma de Buenos Aires',
        'ar-buenos_aires': 'Buenos Aires (Provincia)',
        'ar-catamarca': 'Catamarca',
        'ar-chaco': 'Chaco',
        'ar-chubut': 'Chubut',
        'ar-cordoba': 'Córdoba',
        'ar-corrientes': 'Corrientes',
        'ar-entre_rios': 'Entre Ríos',
        'ar-formosa': 'Formosa',
        'ar-jujuy': 'Jujuy',
        'ar-la_pampa': 'La Pampa',
        'ar-la_rioja': 'La Rioja',
        'ar-mendoza': 'Mendoza',
        'ar-misiones': 'Misiones',
        'ar-neuquen': 'Neuquén',
        'ar-rio_negro': 'Río Negro',
        'ar-salta': 'Salta',
        'ar-san_juan': 'San Juan',
        'ar-san_luis': 'San Luis',
        'ar-santa_cruz': 'Santa Cruz',
        'ar-santa_fe': 'Santa Fe',
        'ar-santiago_del_estero': 'Santiago del Estero',
        'ar-tierra_del_fuego': 'Tierra del Fuego',
        'ar-tucuman': 'Tucumán'
    },
    'cl': {
        'cl-ai': 'Aisén del General Carlos Ibañez del Campo',
        'cl-an': 'Antofagasta',
        'cl-ap': 'Arica y Parinacota',
        'cl-ar': 'La Araucanía',
        'cl-at': 'Atacama',
        'cl-bi': 'Biobío',
        'cl-co': 'Coquimbo',
        'cl-li': 'Libertador General Bernardo O\'Higgins',
        'cl-ll': 'Los Lagos',
        'cl-lr': 'Los Ríos',
        'cl-ma': 'Magallanes',
        'cl-ml': 'Maule',
        'cl-nb': 'Ñuble',
        'cl-rm': 'Región Metropolitana de Santiago',
        'cl-ta': 'Tarapacá',
        'cl-vs': 'Valparaíso',
    }
}

def get_country_area_name(country, area_code):
    return COUNTRY_AREAS[country][area_code]
