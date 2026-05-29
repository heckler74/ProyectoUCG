import math


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def validar_positivo(valor, nombre, permitir_cero=False):
    """Valida que un valor sea positivo."""
    if permitir_cero:
        if valor < 0:
            raise ValueError(f"{nombre} no puede ser negativo.")
    else:
        if valor <= 0:
            raise ValueError(f"{nombre} debe ser mayor que cero.")


def validar_porcentaje(valor, nombre):
    """Valida que un porcentaje esté entre 0 y 100."""
    if valor < 0 or valor > 100:
        raise ValueError(f"{nombre} debe estar entre 0 y 100.")


# =========================================================
# 1) ADMINISTRACIÓN / RECURSOS HUMANOS
# =========================================================

class Empleado:
    """
    Representa un empleado y permite calcular salario bruto,
    descuentos, bono y salario neto.
    """

    def __init__(self, nombre, salario_base, porcentaje_bono=0, porcentaje_descuento=0):
        self.nombre = nombre
        self.salario_base = salario_base
        self.porcentaje_bono = porcentaje_bono
        self.porcentaje_descuento = porcentaje_descuento

        validar_positivo(self.salario_base, "salario_base")
        validar_porcentaje(self.porcentaje_bono, "porcentaje_bono")
        validar_porcentaje(self.porcentaje_descuento, "porcentaje_descuento")

    def calcular_bono(self):
        return self.salario_base * (self.porcentaje_bono / 100)

    def calcular_descuento(self):
        subtotal = self.salario_base + self.calcular_bono()
        return subtotal * (self.porcentaje_descuento / 100)

    def calcular_salario_neto(self):
        return self.salario_base + self.calcular_bono() - self.calcular_descuento()

    def resumen(self):
        return {
            "nombre": self.nombre,
            "salario_base": round(self.salario_base, 2),
            "bono": round(self.calcular_bono(), 2),
            "descuento": round(self.calcular_descuento(), 2),
            "salario_neto": round(self.calcular_salario_neto(), 2)
        }


# =========================================================
# 2) FINANZAS
# =========================================================

class ProyectoInversion:
    """
    Representa un proyecto de inversión y permite calcular
    VPN, ROI y Payback simple.
    """

    def __init__(self, nombre_proyecto, inversion_inicial, flujos, tasa_descuento_pct):
        self.nombre_proyecto = nombre_proyecto
        self.inversion_inicial = inversion_inicial
        self.flujos = flujos
        self.tasa_descuento_pct = tasa_descuento_pct

        validar_positivo(self.inversion_inicial, "inversion_inicial")
        validar_porcentaje(self.tasa_descuento_pct, "tasa_descuento_pct")

        if not isinstance(self.flujos, list) or len(self.flujos) == 0:
            raise ValueError("flujos debe ser una lista con al menos un valor.")

    def calcular_vpn(self):
        tasa = self.tasa_descuento_pct / 100
        vpn = -self.inversion_inicial

        for periodo, flujo in enumerate(self.flujos, start=1):
            vpn += flujo / ((1 + tasa) ** periodo)

        return vpn

    def calcular_roi(self):
        utilidad_neta = sum(self.flujos) - self.inversion_inicial
        return (utilidad_neta / self.inversion_inicial) * 100

    def calcular_payback_simple(self):
        flujo_promedio = sum(self.flujos) / len(self.flujos)
        return self.inversion_inicial / flujo_promedio

    def resumen(self):
        vpn = self.calcular_vpn()
        return {
            "proyecto": self.nombre_proyecto,
            "vpn": round(vpn, 2),
            "roi_pct": round(self.calcular_roi(), 2),
            "payback_anios": round(self.calcular_payback_simple(), 2),
            "decision": "Viable" if vpn > 0 else "No viable"
        }


# =========================================================
# 3) CONTABILIDAD / INVENTARIO
# =========================================================

class InventarioProducto:
    """
    Representa un producto en inventario con cálculos de
    valor total, margen y punto de pedido.
    """

    def __init__(self, nombre, costo_unitario, precio_unitario, stock_actual, stock_minimo):
        self.nombre = nombre
        self.costo_unitario = costo_unitario
        self.precio_unitario = precio_unitario
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo

        validar_positivo(self.costo_unitario, "costo_unitario")
        validar_positivo(self.precio_unitario, "precio_unitario")
        validar_positivo(self.stock_actual, "stock_actual", permitir_cero=True)
        validar_positivo(self.stock_minimo, "stock_minimo", permitir_cero=True)

    def valor_inventario(self):
        return self.costo_unitario * self.stock_actual

    def margen_unitario(self):
        return self.precio_unitario - self.costo_unitario

    def margen_porcentaje(self):
        return (self.margen_unitario() / self.precio_unitario) * 100

    def necesita_reposicion(self):
        return self.stock_actual <= self.stock_minimo

    def resumen(self):
        return {
            "producto": self.nombre,
            "stock_actual": self.stock_actual,
            "valor_inventario": round(self.valor_inventario(), 2),
            "margen_unitario": round(self.margen_unitario(), 2),
            "margen_pct": round(self.margen_porcentaje(), 2),
            "necesita_reposicion": self.necesita_reposicion()
        }


# =========================================================
# 4) TECNOLOGÍA / INFORMÁTICA
# =========================================================

class Servidor:
    """
    Representa un servidor y calcula disponibilidad,
    uso de almacenamiento y estado general.
    """

    def __init__(self, nombre, tiempo_total_h, tiempo_caida_h, almacenamiento_total_gb, almacenamiento_usado_gb):
        self.nombre = nombre
        self.tiempo_total_h = tiempo_total_h
        self.tiempo_caida_h = tiempo_caida_h
        self.almacenamiento_total_gb = almacenamiento_total_gb
        self.almacenamiento_usado_gb = almacenamiento_usado_gb

        validar_positivo(self.tiempo_total_h, "tiempo_total_h")
        validar_positivo(self.tiempo_caida_h, "tiempo_caida_h", permitir_cero=True)
        validar_positivo(self.almacenamiento_total_gb, "almacenamiento_total_gb")
        validar_positivo(self.almacenamiento_usado_gb, "almacenamiento_usado_gb", permitir_cero=True)

        if self.tiempo_caida_h > self.tiempo_total_h:
            raise ValueError("tiempo_caida_h no puede ser mayor que tiempo_total_h.")

        if self.almacenamiento_usado_gb > self.almacenamiento_total_gb:
            raise ValueError("almacenamiento_usado_gb no puede ser mayor que almacenamiento_total_gb.")

    def calcular_disponibilidad(self):
        return ((self.tiempo_total_h - self.tiempo_caida_h) / self.tiempo_total_h) * 100

    def calcular_uso_almacenamiento(self):
        return (self.almacenamiento_usado_gb / self.almacenamiento_total_gb) * 100

    def estado_servidor(self):
        disponibilidad = self.calcular_disponibilidad()
        uso = self.calcular_uso_almacenamiento()

        if disponibilidad < 95 or uso > 90:
            return "Crítico"
        elif disponibilidad < 98 or uso > 75:
            return "Advertencia"
        return "Óptimo"

    def resumen(self):
        return {
            "servidor": self.nombre,
            "disponibilidad_pct": round(self.calcular_disponibilidad(), 2),
            "uso_almacenamiento_pct": round(self.calcular_uso_almacenamiento(), 2),
            "estado": self.estado_servidor()
        }


# =========================================================
# 5) MANTENIMIENTO
# =========================================================

class EquipoMantenimiento:
    """
    Representa un equipo industrial y calcula MTBF,
    MTTR y disponibilidad.
    """

    def __init__(self, nombre_equipo, horas_operacion, numero_fallas, horas_reparacion):
        self.nombre_equipo = nombre_equipo
        self.horas_operacion = horas_operacion
        self.numero_fallas = numero_fallas
        self.horas_reparacion = horas_reparacion

        validar_positivo(self.horas_operacion, "horas_operacion")
        validar_positivo(self.numero_fallas, "numero_fallas")
        validar_positivo(self.horas_reparacion, "horas_reparacion", permitir_cero=True)

    def calcular_mtbf(self):
        return self.horas_operacion / self.numero_fallas

    def calcular_mttr(self):
        return self.horas_reparacion / self.numero_fallas

    def calcular_disponibilidad(self):
        mtbf = self.calcular_mtbf()
        mttr = self.calcular_mttr()
        return (mtbf / (mtbf + mttr)) * 100

    def resumen(self):
        return {
            "equipo": self.nombre_equipo,
            "mtbf_h": round(self.calcular_mtbf(), 2),
            "mttr_h": round(self.calcular_mttr(), 2),
            "disponibilidad_pct": round(self.calcular_disponibilidad(), 2)
        }


# =========================================================
# 6) EDUCACIÓN
# =========================================================

class EstudianteCurso:
    """
    Representa a un estudiante y calcula nota final
    y asistencia mínima.
    """

    def __init__(
        self,
        nombre,
        actividades,
        proyecto,
        examen_final,
        peso_actividades,
        peso_proyecto,
        peso_examen_final,
        total_clases,
        clases_asistidas
    ):
        self.nombre = nombre
        self.actividades = actividades
        self.proyecto = proyecto
        self.examen_final = examen_final
        self.peso_actividades = peso_actividades
        self.peso_proyecto = peso_proyecto
        self.peso_examen_final = peso_examen_final
        self.total_clases = total_clases
        self.clases_asistidas = clases_asistidas

        validar_porcentaje(self.peso_actividades, "peso_actividades")
        validar_porcentaje(self.peso_proyecto, "peso_proyecto")
        validar_porcentaje(self.peso_examen_final, "peso_examen_final")
        validar_positivo(self.total_clases, "total_clases")
        validar_positivo(self.clases_asistidas, "clases_asistidas", permitir_cero=True)

        if round(self.peso_actividades + self.peso_proyecto + self.peso_examen_final, 6) != 100:
            raise ValueError("La suma de los pesos debe ser 100.")

        if self.clases_asistidas > self.total_clases:
            raise ValueError("clases_asistidas no puede ser mayor que total_clases.")

    def calcular_nota_final(self):
        return (
            self.actividades * (self.peso_actividades / 100) +
            self.proyecto * (self.peso_proyecto / 100) +
            self.examen_final * (self.peso_examen_final / 100)
        )

    def calcular_asistencia(self):
        return (self.clases_asistidas / self.total_clases) * 100

    def estado_academico(self, nota_minima=7.0, asistencia_minima=75.0):
        nota = self.calcular_nota_final()
        asistencia = self.calcular_asistencia()

        if nota >= nota_minima and asistencia >= asistencia_minima:
            return "Aprueba"
        return "No aprueba"

    def resumen(self):
        return {
            "estudiante": self.nombre,
            "nota_final": round(self.calcular_nota_final(), 2),
            "asistencia_pct": round(self.calcular_asistencia(), 2),
            "estado": self.estado_academico()
        }


# =========================================================
# 7) SALUD
# =========================================================

class Paciente:
    """
    Representa un paciente para cálculos básicos educativos
    como IMC y superficie corporal.
    """

    def __init__(self, nombre, peso_kg, altura_m):
        self.nombre = nombre
        self.peso_kg = peso_kg
        self.altura_m = altura_m

        validar_positivo(self.peso_kg, "peso_kg")
        validar_positivo(self.altura_m, "altura_m")

    def calcular_imc(self):
        return self.peso_kg / (self.altura_m ** 2)

    def clasificacion_imc(self):
        imc = self.calcular_imc()

        if imc < 18.5:
            return "Bajo peso"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        return "Obesidad"

    def calcular_superficie_corporal(self):
        altura_cm = self.altura_m * 100
        return math.sqrt((self.peso_kg * altura_cm) / 3600)

    def resumen(self):
        return {
            "paciente": self.nombre,
            "imc": round(self.calcular_imc(), 2),
            "clasificacion_imc": self.clasificacion_imc(),
            "superficie_corporal_m2": round(self.calcular_superficie_corporal(), 3)
        }


# =========================================================
# 8) INGENIERÍA CIVIL
# =========================================================

class MezclaConcreto:
    """
    Calcula volumen de concreto, desperdicio y cemento requerido.
    """

    def __init__(self, largo_m, ancho_m, espesor_m, desperdicio_pct, dosificacion_cemento_kg_m3):
        self.largo_m = largo_m
        self.ancho_m = ancho_m
        self.espesor_m = espesor_m
        self.desperdicio_pct = desperdicio_pct
        self.dosificacion_cemento_kg_m3 = dosificacion_cemento_kg_m3

        validar_positivo(self.largo_m, "largo_m")
        validar_positivo(self.ancho_m, "ancho_m")
        validar_positivo(self.espesor_m, "espesor_m")
        validar_porcentaje(self.desperdicio_pct, "desperdicio_pct")
        validar_positivo(self.dosificacion_cemento_kg_m3, "dosificacion_cemento_kg_m3")

    def calcular_volumen(self):
        return self.largo_m * self.ancho_m * self.espesor_m

    def calcular_volumen_ajustado(self):
        return self.calcular_volumen() * (1 + self.desperdicio_pct / 100)

    def calcular_cemento_kg(self):
        return self.calcular_volumen_ajustado() * self.dosificacion_cemento_kg_m3

    def calcular_sacos_50kg(self):
        return self.calcular_cemento_kg() / 50

    def resumen(self):
        return {
            "volumen_m3": round(self.calcular_volumen(), 3),
            "volumen_ajustado_m3": round(self.calcular_volumen_ajustado(), 3),
            "cemento_kg": round(self.calcular_cemento_kg(), 2),
            "sacos_50kg": round(self.calcular_sacos_50kg(), 2)
        }


# =========================================================
# 9) ARQUITECTURA
# =========================================================

class EspacioIluminacion:
    """
    Calcula lúmenes requeridos y número de luminarias.
    """

    def __init__(self, area_m2, nivel_lux, factor_utilizacion, factor_mantenimiento, flujo_luminaria_lm):
        self.area_m2 = area_m2
        self.nivel_lux = nivel_lux
        self.factor_utilizacion = factor_utilizacion
        self.factor_mantenimiento = factor_mantenimiento
        self.flujo_luminaria_lm = flujo_luminaria_lm

        validar_positivo(self.area_m2, "area_m2")
        validar_positivo(self.nivel_lux, "nivel_lux")
        validar_positivo(self.flujo_luminaria_lm, "flujo_luminaria_lm")

        if not (0 < self.factor_utilizacion <= 1):
            raise ValueError("factor_utilizacion debe estar entre 0 y 1.")

        if not (0 < self.factor_mantenimiento <= 1):
            raise ValueError("factor_mantenimiento debe estar entre 0 y 1.")

    def calcular_lumenes_totales(self):
        return (self.nivel_lux * self.area_m2) / (self.factor_utilizacion * self.factor_mantenimiento)

    def calcular_numero_luminarias(self):
        return math.ceil(self.calcular_lumenes_totales() / self.flujo_luminaria_lm)

    def resumen(self):
        return {
            "area_m2": self.area_m2,
            "lumenes_totales": round(self.calcular_lumenes_totales(), 2),
            "numero_luminarias": self.calcular_numero_luminarias()
        }


# =========================================================
# 10) AGRONOMÍA
# =========================================================

class ParcelaAgricola:
    """
    Calcula densidad de siembra y requerimiento de fertilizante.
    """

    def __init__(
        self,
        area_hectareas,
        distancia_surcos_m,
        distancia_plantas_m,
        germinacion_pct,
        dosis_nutriente_kg_ha,
        pureza_fertilizante_pct,
        eficiencia_aplicacion_pct
    ):
        self.area_hectareas = area_hectareas
        self.distancia_surcos_m = distancia_surcos_m
        self.distancia_plantas_m = distancia_plantas_m
        self.germinacion_pct = germinacion_pct
        self.dosis_nutriente_kg_ha = dosis_nutriente_kg_ha
        self.pureza_fertilizante_pct = pureza_fertilizante_pct
        self.eficiencia_aplicacion_pct = eficiencia_aplicacion_pct

        validar_positivo(self.area_hectareas, "area_hectareas")
        validar_positivo(self.distancia_surcos_m, "distancia_surcos_m")
        validar_positivo(self.distancia_plantas_m, "distancia_plantas_m")
        validar_porcentaje(self.germinacion_pct, "germinacion_pct")
        validar_positivo(self.dosis_nutriente_kg_ha, "dosis_nutriente_kg_ha")
        validar_porcentaje(self.pureza_fertilizante_pct, "pureza_fertilizante_pct")
        validar_porcentaje(self.eficiencia_aplicacion_pct, "eficiencia_aplicacion_pct")

        if self.germinacion_pct == 0:
            raise ValueError("germinacion_pct no puede ser cero.")

    def calcular_plantas_teoricas(self):
        area_m2 = self.area_hectareas * 10000
        return area_m2 / (self.distancia_surcos_m * self.distancia_plantas_m)

    def calcular_semillas_ajustadas(self):
        return self.calcular_plantas_teoricas() / (self.germinacion_pct / 100)

    def calcular_fertilizante_kg(self):
        pureza = self.pureza_fertilizante_pct / 100
        eficiencia = self.eficiencia_aplicacion_pct / 100

        if pureza == 0 or eficiencia == 0:
            raise ValueError("La pureza y la eficiencia deben ser mayores que cero.")

        return (self.area_hectareas * self.dosis_nutriente_kg_ha) / (pureza * eficiencia)

    def resumen(self):
        return {
            "plantas_teoricas": round(self.calcular_plantas_teoricas(), 2),
            "semillas_ajustadas": round(self.calcular_semillas_ajustadas(), 2),
            "fertilizante_kg": round(self.calcular_fertilizante_kg(), 2),
            "sacos_50kg": round(self.calcular_fertilizante_kg() / 50, 2)
        }



# =========================================================
# 11) SECTOR CAMARONERO / ACUICULTURA
# =========================================================

class MuestraPiscina:
    """
    Representa una muestra de producción tomada en una piscina camaronera.
    """

    def __init__(self, fecha, peso_gramos, consumo_balanceado_kg, num_animales):
        self.fecha = fecha
        self.peso_gramos = peso_gramos
        self.consumo_balanceado_kg = consumo_balanceado_kg
        self.num_animales = num_animales

        validar_positivo(self.peso_gramos, "peso_gramos")
        validar_positivo(self.consumo_balanceado_kg, "consumo_balanceado_kg", permitir_cero=True)
        validar_positivo(self.num_animales, "num_animales")

    def calcular_biomasa_kg(self):
        """Calcula la biomasa total en kg a partir del peso y el número de animales."""
        return (self.num_animales * self.peso_gramos) / 1000.0


class PiscinaCamaronera:
    """
    Representa una piscina en una camaronera, gestionando su historial
    de muestras, crecimiento y alimentación.
    """

    def __init__(self, cod_piscina, poblacion_inicial=None):
        self.cod_piscina = cod_piscina
        self.muestras = []
        self.poblacion_inicial = poblacion_inicial

    def agregar_muestra(self, muestra):
        """Agrega una muestra al historial de la piscina."""
        if not isinstance(muestra, MuestraPiscina):
            raise TypeError("La muestra debe ser una instancia de MuestraPiscina.")
        
        # Si no se ha definido población inicial, se define con la primera muestra
        if self.poblacion_inicial is None or self.poblacion_inicial == 0:
            self.poblacion_inicial = muestra.num_animales
            
        self.muestras.append(muestra)
        # Ordenar las muestras por fecha para asegurar consistencia en los cálculos
        self.muestras.sort(key=lambda m: m.fecha)

    def total_alimento_consumido(self):
        """Calcula la cantidad acumulada de alimento consumido en kg."""
        return sum(m.consumo_balanceado_kg for m in self.muestras)

    def fcr_actual(self):
        """
        Calcula el Factor de Conversión Alimenticia (FCR) actual de la piscina.
        FCR = Alimento total consumido / (Biomasa actual - Biomasa inicial)
        """
        if len(self.muestras) < 2:
            return 0.0
        
        biomasa_inicial = self.muestras[0].calcular_biomasa_kg()
        biomasa_actual = self.muestras[-1].calcular_biomasa_kg()
        biomasa_ganada = biomasa_actual - biomasa_inicial
        
        if biomasa_ganada <= 0:
            return 0.0
            
        return self.total_alimento_consumido() / biomasa_ganada

    def supervivencia_actual(self):
        """Calcula el porcentaje de supervivencia actual basado en la población inicial."""
        if not self.muestras or not self.poblacion_inicial:
            return 0.0
        
        poblacion_actual = self.muestras[-1].num_animales
        return (poblacion_actual / self.poblacion_inicial) * 100.0

    def adg_promedio(self):
        """
        Calcula el Incremento de Peso Diario (ADG) promedio a lo largo de toda la corrida.
        """
        if len(self.muestras) < 2:
            return 0.0
        
        import datetime
        
        # Convertir fechas a objetos datetime para calcular la diferencia de días
        try:
            d_inicio = datetime.datetime.strptime(self.muestras[0].fecha, "%Y-%m-%d")
            d_fin = datetime.datetime.strptime(self.muestras[-1].fecha, "%Y-%m-%d")
            diferencia_dias = (d_fin - d_inicio).days
        except Exception:
            # Fallback en caso de que las fechas tengan un formato diferente
            diferencia_dias = len(self.muestras)
            
        if diferencia_dias <= 0:
            return 0.0
            
        peso_inicial = self.muestras[0].peso_gramos
        peso_actual = self.muestras[-1].peso_gramos
        
        return (peso_actual - peso_inicial) / diferencia_dias

    def obtener_resumen(self):
        """Retorna un diccionario resumido con los KPIs actuales de la piscina."""
        if not self.muestras:
            return {
                "cod_piscina": self.cod_piscina,
                "estado": "Sin muestras registradas"
            }
            
        muestra_actual = self.muestras[-1]
        
        return {
            "cod_piscina": self.cod_piscina,
            "dias_cultivo": len(self.muestras),
            "peso_actual_g": round(muestra_actual.peso_gramos, 2),
            "poblacion_estimada": muestra_actual.num_animales,
            "biomasa_actual_kg": round(muestra_actual.calcular_biomasa_kg(), 2),
            "alimento_acumulado_kg": round(self.total_alimento_consumido(), 2),
            "fcr_actual": round(self.fcr_actual(), 2),
            "supervivencia_pct": round(self.supervivencia_actual(), 2),
            "adg_promedio_g_dia": round(self.adg_promedio(), 3)
        }


class Camaronera:
    """
    Representa una empresa camaronera que agrupa y gestiona múltiples piscinas.
    """

    def __init__(self, codigo_camaronera):
        self.codigo_camaronera = codigo_camaronera
        self.piscinas = {}

    def obtener_piscina(self, cod_piscina):
        """Retorna una piscina por su código, creándola si no existe."""
        if cod_piscina not in self.piscinas:
            self.piscinas[cod_piscina] = PiscinaCamaronera(cod_piscina)
        return self.piscinas[cod_piscina]

    def agregar_datos_desde_dataframe(self, df):
        """
        Carga datos desde un DataFrame de Pandas (filtrado para esta camaronera)
        e instancia los objetos correspondientes.
        """
        # Filtrar registros de esta camaronera específica
        df_filtrado = df[df["codigo_camaronera"] == self.codigo_camaronera]
        
        for _, row in df_filtrado.iterrows():
            cod_p = row["cod_piscina"]
            piscina = self.obtener_piscina(cod_p)
            
            muestra = MuestraPiscina(
                fecha=str(row["fecha_muestra"]),
                peso_gramos=float(row["peso_gramos"]),
                consumo_balanceado_kg=float(row["consumo_balanceado_kg"]),
                num_animales=int(row["num_animales"])
            )
            piscina.agregar_muestra(muestra)

    def obtener_resumen_general(self):
        """Retorna una lista de diccionarios con el resumen de cada piscina activa."""
        return [piscina.obtener_resumen() for piscina in self.piscinas.values() if piscina.muestras]