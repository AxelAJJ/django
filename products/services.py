import unicodedata


class EstrategiaDescuento:
    def calcular(self, precio):
        raise NotImplementedError


class DescuentoElectronica(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * 0.90


class DescuentoRopa(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * 0.80


class SinDescuento(EstrategiaDescuento):
    def calcular(self, precio):
        return precio


def normalizar_nombre_categoria(categoria_nombre):
    if categoria_nombre is None:
        return ''

    texto = unicodedata.normalize('NFKD', str(categoria_nombre))
    texto = ''.join(ch for ch in texto if not unicodedata.combining(ch))
    texto = texto.strip().lower().replace('_', ' ').replace('-', ' ')
    return ' '.join(texto.split())


def obtener_estrategia(categoria_nombre):
    nombre = normalizar_nombre_categoria(categoria_nombre)
    estrategias = {
        'electronica': DescuentoElectronica(),
        'electrodomesticos': DescuentoElectronica(),
        'tecnologia': DescuentoElectronica(),
        'ropa': DescuentoRopa(),
        'vestimenta': DescuentoRopa(),
    }
    return estrategias.get(nombre, SinDescuento())
