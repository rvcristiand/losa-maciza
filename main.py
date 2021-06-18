import numpy as np
from docxtpl import DocxTemplate


doc = DocxTemplate("DISEÑO DE LA LOSA MACIZA DEL PUENTE.docx")

def design(params):
    context = {}
    # datos de entrada

    fc = params.get('fc', 28)
    fy = 420
    L = params.get('L', 10)
    ancho_de_carril = 3.6
    ancho_de_berma = 1
    ancho_de_anden = 0
    espesor_de_carpeta_asfaltica = 0.08
    ancho_inferior_de_barrera = 0.38
    ancho_superior_de_barrera = 0.15
    altura_de_barrera = 0.865
    
    num_carriles = 2
    # TODO: agregar num_carriles context

    ancho_total = round((((ancho_de_carril *num_carriles / 2 )+ ancho_de_berma + ancho_de_anden + ancho_inferior_de_barrera) * 2),2)

    #Altura de la losa
    h_min = ((1.2 * ( L + 3)) / 30)
    h = round(h_min,1)

    # apoyo minimo
    N = (0.200 + 0.0017 * L)
    context['N'] = N

    #ancho de franja equivalente
    if ancho_total < 9 :
        anchofreq_uncarril = ancho_total
    else:
        anchofreq_uncarril = 9 
    
    if L < 18 :
        luzfreq_uncarril = L
    else:
        luzfreq_uncarril = 18 

    E_un_carril = round((0.25 + 0.42 * ( anchofreq_uncarril * luzfreq_uncarril ) ** 0.5),2)

    if E_un_carril > (ancho_total/num_carriles):
        E_un_carril = (ancho_total/num_carriles)
    
    if ancho_total < 18:
        anchofreq_doscarriles = ancho_total
        
    else:
        anchofreq_doscarriles = 18

    E_dos_carriles = round((2.1 + 0.12 * ( anchofreq_doscarriles * luzfreq_uncarril ) ** 0.5),2)
    
    if E_dos_carriles > (ancho_total/num_carriles):
        E_dos_carriles = (ancho_total/num_carriles)
    
    if E_un_carril < E_dos_carriles:
        E_tomado = E_un_carril
        
    else:
        E_tomado = E_dos_carriles
    
    #Solicitaciones
    #Por carga muerta
    # pesos especificos en kN/m3
    pespecifico_concreto = 2.4 * 10
    pespecifico_carpeta_asfaltica = 2.2 * 9.81

    # Cargas distrbuidas muertas
    DC = round (pespecifico_concreto * h, 2)
    DW = round ((pespecifico_carpeta_asfaltica * espesor_de_carpeta_asfaltica),2)

    #Momentos máximos
    # Cargas Permanentes
    # Unidades en kN/m
    MDC = round(((DC * L ** 2 / 8) ))
    MDW = round(((DW * L ** 2 / 8) ))

    # información del puente
    context['nombre'] = "Puente El Portillo"

    context['departamento'] = "Cesar"
    context['municipio'] = "San Martín"
    context['coordenadas'] = "7°59'57.2\"N 73°30'57.6\"W"
    
    context['fc'] = fc 
    context['fy'] = fy

    context['L'] = L
    context['ancho_de_carril'] = ancho_de_carril
    context['ancho_de_berma'] = ancho_de_berma
    context['ancho_de_anden'] = ancho_de_anden
    context['espesor_carpeta_asfaltica'] = espesor_de_carpeta_asfaltica
    context['ancho_inferior_de_barrera'] = ancho_inferior_de_barrera
    context['ancho_superior_de_barrera'] = ancho_superior_de_barrera
    context['altura_de_barrera'] = altura_de_barrera

    context['ancho_total'] = ancho_total

    context['h_min'] = h_min
    context['h'] = h

    context['E_un_carril'] = E_un_carril
    context['E_dos_carriles'] = E_dos_carriles
    context['E_tomado'] = E_tomado
 
    context['pespecifico_carpeta_asfaltica'] = round(pespecifico_carpeta_asfaltica)
    context['pespecifico_concreto'] = round(pespecifico_concreto)
    context['DC'] = DC
    context['DW'] = DW
    
    context['MDC'] = MDC
    context['MDW'] = MDW
    
    
    #Momento máximo debido al camión de diseño (360 kN)

    MAcamion = round(360 / L * (L / 2 + 0.717) ** 2 - 688) # Ecuación válida para luces mayores de 10.04 m
    context['MAcamion'] = MAcamion
    # Momento máximo debido al tandem de diseño (250 kN) # Ecuación válida para luces mayores de 1.8 m 
    Mtandem = round(250 / L * ( L / 2 + 0.3) ** 2 - 150)
    context['Mtandem'] = Mtandem

    if Mtandem > MAcamion:
        Mcviva = Mtandem
    else : Mcviva = MAcamion
    
    #Nota: Para luces menores que 12,43 m gobierna el tandem de diseño. 
    #Momento máximo debido al carril de diseño (10.33 kN/m)
    Mcarril = round(10.3 * L **2 / 8)
    context['Mcarril'] = Mcarril
    #Momento maximo debido a la carga vehicular de diseño con amplificación dinámica

    MLLIM = round(1.33 * Mcviva + Mcarril)
    context['MLLIM'] = MLLIM
    
    #Momento por carga viva por metro de ancho de franja equivalente

    MLLIMafequiv = round(MLLIM / E_tomado)
    context['MLLIMafequiv'] = MLLIMafequiv
    
    #Diseño a Flexión
    #Factores de modificación de carga 1.3.2
    #Factor relacionado cola ductilidad
    factor_ductilidad = 1

    #Factor relacionado con la redundancia
    factor_redundancia = 1

    #Factor relacionado con la importancia operativa
    factor_imp_operativa = 1

    factor_mod_carga = factor_ductilidad *  factor_imp_operativa * factor_redundancia
    context['factor_mod_carga'] = factor_mod_carga

    # Momento ultimo
    Mu = factor_mod_carga * ( 1.25 * MDC + 1.5 * MDW + 1.75 * MLLIMafequiv )
    Mu_tonm = Mu / 9.81
    context['Mu'] = Mu

    # Recubrimiento de armadura principal no protegida TAbla 5.12.3.1
    recub = 0.05
    # factor phi para diseño a flexión
    phi = 0.9
    d = round(h - recub,3)
    context['d'] = d 

    K = round (Mu_tonm / (1 * d ** 2),1)
    context['K'] = K

    #cuantía de acero
    cuantia = round(0.0567 * (1 - ( 1- (35.3 * K / 37800)) ** 0.5 ), 5)
    context['cuantia'] = cuantia 

    cuantia_kN = round(( 1 - ( 1 - ( 2 * Mu / ( phi * 1 * d ** 2 * 0.85 * fc * 1000 ) ) ) ** 0.5 ) * 0.85 * fc /  fy, 5)  
    context['cuantia_kN'] = cuantia_kN
    #Area de refuerzo de la losa en cm2
    As_flexion = round(cuantia_kN * d * 100 * 100, 2)
    context['As_flexion'] = As_flexion

    #Para barras #8 As = 5.1 cm2
    As_8 = 5.1 # definir al inicio
    No_barras_8_flexion = round(As_flexion / As_8)
    context['No_barras_8_flexion'] = No_barras_8_flexion
    context['As_8'] = As_8

    #Espaciamiento Armadura a flexión
    espac_arm_prin_flexion = round (100 / No_barras_8_flexion)
    context['espac_arm_prin_flexion'] = espac_arm_prin_flexion

    # Revisión del factor phi = 0.9 para el diseño a flexión

    a_f = round(cuantia * d * fy /( 0.85 * fc), 4)
    context['a_f'] = a_f
    #profundidad eje neutro

    betha_1 = 0.85
    c_f = round(a_f / betha_1 , 4) 
    context['c_f'] = c_f
    #Relacion de  deformaciones en la sección de concreto reforzado

    defor_total = round((d - c_f) * (0.003 / c_f), 4)  
    context['defor_total'] = defor_total
    #Armadura dedistribución para losas con armadura principal paralela a la dirección del trafico (9.7.3.2)

    Armadura_de_distribucion = round(55 / (L) ** 0.5 / 100, 2 )
    context['Armadura_de_distribucion'] = Armadura_de_distribucion

    As_4 = 1.29
    As_Armadura_de_distribucion = round ( Armadura_de_distribucion * As_flexion , 2)
    context['As_Armadura_de_distribucion'] = As_Armadura_de_distribucion

    No_barras_4_dist =  round( As_Armadura_de_distribucion / As_4 )
    context['No_barras_4_dist'] = No_barras_4_dist

    espac_arm_dist = round( 100 / No_barras_4_dist )
    context['espac_arm_dist'] = espac_arm_dist

    #Armadura minima
    #Modulo de rotura del concreto
    fr = round(0.62 * fc ** 0.5, 2)
    context['fr'] = fr 
    # factor de variacion de l afisuracion por flexion 5.7.3.3.2 
    gamma_1 = 1.6

    #relacion entre la reistencia especificada a fluencia y la resistencia ultima atracción del refuerzo
    #refuerzo a706, Grado 60
    gamma_3 = 0.75

    #Modulo elastico de la seccion

    Sc = round(1 * h ** 2 / 6, 4 )
    context['Sc'] = Sc

    Mcr = round (gamma_1 ** 2 * gamma_3 * fr * Sc * 1000)
    context['Mcr'] = Mcr

    if Mcr > Mu :
        print ('No cumple Armadura mínima')
    
    # Control de fisuración
    # Factor de exposición clase 1. 5.7.3.4 
    gamma_e = 1.0

    #De acuerdo con 5.12.3-1, el espesor de recubrimiento de concreto medido desde la fibra extrema a tracción hasta el centro del refuerzo de flexión mas cercano, para losas vaciadas in situ 25 mm

    d_c = 0.025 + 0.0254 / 2

    if d_c < 0.050 : 
        d_c = 0.050

    #De acuerdo con el Art 5.7.3.4, el coeficiente beta s 
    beta_s = round (1 + d_c / (0.7 * (h - d_c)), 3)
    context['beta_s'] = beta_s

    #Calculo de fss: Esfuerzo actuante a tracción en el acero para estado limite de servicio I
    
    #Combinación para el estado limite de servicio tabla 3.4.1
    Msi = 1 * (MDC + MDW + MLLIMafequiv)
    context['Msi'] = Msi

    # Modulo de elasticidad del concreto - densidad normal MPa

    E_concreto = round(0.043 * 2320 ** 1.5 * (fc) ** 0.5, 2)
    context['E_concreto'] = E_concreto

    # Modulo de elasticidad del acero MPa
    
    E_acero = 200000

    #Relación modular

    rel_mod = round(E_acero / E_concreto)
    context['rel_mod'] = rel_mod

    #Momento de primer orden de la sección  fisurada, de 1m de ancho, con respecto al eje neutro

    #Tomando momentos con respecto al eje neutro de la sección:

    X_cf = round (( -(2 * rel_mod * As_flexion * 10 ** -4) + ((2 * rel_mod * As_flexion * 10 ** -4 ) ** 2 - (4 * 1 * -2 * rel_mod * As_flexion * 10 ** -4 * d )) ** 0.5 ) / (2 * 1), 2)
    context['X_cf'] = X_cf

    # Momento de inercia de la seccion fisurada

    I_c = round(X_cf ** 3 / 3 + rel_mod * As_flexion * 10 ** -4 * (d - X_cf) ** 2, 8)
    context['I_c'] = I_c

    fss = round (rel_mod * Msi * (d - X_cf) / I_c / 1000, 2)
    context['fss'] = fss

    # Reemplazando en la ecuación 5.7.3.4.1
    
    espac_control_fisuracion = round((123000 * gamma_e / (beta_s * fss) ) - (2 * d_c * 1000))
    context['espac_control_fisuracion'] = espac_control_fisuracion /10

    if espac_control_fisuracion / 100 > espac_arm_prin_flexion :
        print ('No cumple control de fisuración')

    # Separacion centro a centro de barras 
    diametro_barra_8 = 2.54
    espac_libre = espac_arm_prin_flexion - diametro_barra_8 
    context['espac_libre'] = espac_libre

    # Espaciamiento minimo de la armadura vaciada in situ 5.10.3 
    
    #tamaño agregado 3/4in en cm
    tamaño_agregado = 1.905

    if espac_libre < 1.5 * diametro_barra_8 :
        print ('No cumple espaciamineto minimo 5.10.3')
    if espac_libre < 1.5 * tamaño_agregado :
        print ('No cumple espaciamineto minimo 5.10.3')
    if espac_libre < 3.8 :
        print ('No cumple espaciamineto minimo 5.10.3')

    #Armadura por retraccion de fraguado y temperatura
    As_retytemp = round(750 * ancho_total * h / (2 * (ancho_total + h) * fy) * 1000)

    if 234 > As_retytemp :
        print ('No cumple Retraccion y Temperatura')
    if  As_retytemp > 1278:
        print ('No cumple Retraccion y Temperatura') 
    context['As_retytemp'] = As_retytemp
    
    No_barras_4_retytemp = round (As_retytemp /100 / As_4, 2) 
    context ['No_barras_4_retytemp'] = No_barras_4_retytemp

    espa_arm_retytemp = round(100 / No_barras_4_retytemp)
    context['espa_arm_retytemp'] = espa_arm_retytemp
    h3 = round(3 * h)
    context['h3'] = h3 
    

    ##Verificación por fatiga
    # De acuerdo con 3.6.1.4.1 la carga de fatiga debe ser el camion de diseño 360 kN con un espaciamiento constante de 9 m entre ejes

    # Factor de carga especificado en 3.4.1-1 para la combinacion de carga de fatiga
    gamma_fatiga = 1.5
    context['gamma_fatiga'] = gamma_fatiga

    #MLL+IM Fatiga, camion de diseño kN
    if L > 14.48 :
        MLLIM_fatiga = round(1.15 * (360/L * (L/2 + 1.76) ** 2) - 1440, 2)
    else :
        print('ingrese valor de MLLIM_fatiga')
        MLLIM_fatiga = round(1.15 * (91.4 * 4.57), 2)

    anchofreq_uncarril_fatiga = round(E_un_carril / 1.2, 2)
    MLLIM_fatiga_fraequiv = round(MLLIM_fatiga / anchofreq_uncarril_fatiga)

    context['MLLIM_fatiga'] = MLLIM_fatiga
    context['anchofreq_uncarril_fatiga'] = anchofreq_uncarril_fatiga
    context['MLLIM_fatiga_fraequiv'] = MLLIM_fatiga_fraequiv

    #Momento seccion no fisurada
    Mseccion_fisurada = round(MDC + MDW + 1.5 * MLLIM_fatiga_fraequiv)
    context['Mseccion_fisurada'] = Mseccion_fisurada

    # esfuerzo actuante seccion no fisurada

    Y_inf = h / 2
    I_seccion = 1 * h ** 3 / 12
    f_c_nofisurado = round(Mseccion_fisurada * Y_inf / (I_seccion) /1000)
    context['f_c_nofisurado'] = f_c_nofisurado

    jd = d - X_cf/3
    
    condicion_esf_seccion_fisurada = round(0.25 * (fc) ** 0.5,1)
    if f_c_nofisurado > condicion_esf_seccion_fisurada :
        deltaf = MLLIM_fatiga_fraequiv / ( As_flexion * 10 ** -4 * jd)
    context['condicion_esf_seccion_fisurada'] = condicion_esf_seccion_fisurada

    #verificacion de esfuerzos sobre la seccion fisurada

    f_seccion_fisurada = round(gamma_fatiga * deltaf /1000)
    context['f_seccion_fisurada'] = f_seccion_fisurada

    #Esfuerzo minimo debido a la carga viva que resulta de la combinacion de carga de fatiga I,combinado con el esfuerzo mas severo de cargas permanentes
    #El minmo esfuerzo sobre el acero de refuerzo se produce cuando no actua carga viva
    f_min = round((MDC + MDW) / (As_flexion * 10 ** -4 *jd) /1000)
    context['f_min'] = f_min

    deltaF_TH = round(166 - 0.33 * f_min)
    context['deltaF_TH'] = deltaF_TH

    if f_seccion_fisurada > deltaF_TH :
        print ('No cumple verificación por fatiga')
    
    

    #Franja exterior del puente 
    #De acuerdo con 4.6.2.1.4b 
    if ancho_inferior_de_barrera + 0.3 + E_un_carril/4 < 1.8 and ancho_inferior_de_barrera + 0.3 + E_un_carril/4 < E_un_carril / 2  :
        E_borde = ancho_inferior_de_barrera + 0.3 + E_un_carril/4
    elif ancho_inferior_de_barrera + 0.3 + E_un_carril/4 > 1.8 and E_un_carril/2 < 1.8 and ancho_inferior_de_barrera + 0.3 + E_un_carril/4 > E_un_carril/2:
        E_borde = E_un_carril / 2
    else :
        E_borde = 1.8
    context['Eborde1'] = ancho_inferior_de_barrera + 0.3 + E_un_carril/4
    context['Eborde2'] = E_un_carril / 2
    context['E_borde'] = E_borde

    #Avaluo de crgas permanentes para la franja exterior
    DC_barrera = round(0.47 / E_borde * 9.81, 2)
    context['DC_barrera'] = DC_barrera

    DW_ext = round(pespecifico_carpeta_asfaltica * espesor_de_carpeta_asfaltica * (E_borde - ancho_inferior_de_barrera) / E_borde , 2) 
    context['DW_ext'] = DW_ext

    #Momentos maximos debidos a cargas permanentes

    MDC_ext = round((DC + DC_barrera) * L ** 2 / 8 , 2)
    context['MDC_ext'] = MDC_ext

    MDW_ext = round(DW_ext * L ** 2 / 8 , 2)
    context['MDW_ext'] = MDW_ext

    #Momento debido a carga viva
    # Debido a que sobre la franja exterior actua una rueda y no un eje, se dividen las solicitaciones en 2 y en el ancho de la franja exterior
    MLLIM_ext = round(MLLIM / 2 / E_borde, 2)
    context['MLLIM_ext'] = MLLIM_ext

    #Determinacion de armadura a flexion de franja exterior
    
    Mu_ext = round((1.25 * MDC_ext + 1.5 * MDW_ext + 1.75 * MLLIM_ext), 2)
    context['Mu_ext'] = Mu_ext
    #cuantia franja exterior 
    
    cuantia_ext = round(( 1 - ( 1 - ( 2 * Mu_ext / ( phi * 1 * d ** 2 * 0.85 * fc * 1000 ) ) ) ** 0.5 ) * 0.85 * fc /  fy, 4)
    context['cuantia_ext'] = cuantia_ext

    As_flexion_ext = round(cuantia_ext * d * 100 * 100)
    context['As_flexion_ext'] = As_flexion_ext

    #Numero de barras #8 flexion franja exterior

    No_barras_8_flexion_ext = round (As_flexion_ext / As_8) 
    context['No_barras_8_flexion_ext'] = No_barras_8_flexion_ext

    #Separacion de barras a flexion franja exterior

    espac_arm_prin_flexion_ext = round (100 / No_barras_8_flexion_ext)
    context['espac_arm_prin_flexion_ext'] = espac_arm_prin_flexion_ext

    return context


def report(dict):
    string = ''

    def add(key):
        return "{}: {}".format(key, dict[key])

    string += add('nombre') + '\n'
    string += add('L')

    
    return string


if __name__ == "__main__":
    params = {}

    params = design(params)

    doc.render(params)
    doc.save('Memoria de cálculos de la losa maciza.docx')

