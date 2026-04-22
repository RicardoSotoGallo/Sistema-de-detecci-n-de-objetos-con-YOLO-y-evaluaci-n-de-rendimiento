import os
import math

direccionNuestroValidacion = "datasetP/labels/val"
direccionNuestroPredicciones = "datasetP/predict"

ficherosValidacion = os.listdir(direccionNuestroValidacion)
ficheroPrediccion = os.listdir( direccionNuestroPredicciones )

"""
1,2 (x,y) -> primer punto son el centro de la imagen
3,4 (w,h) -> anchura altura
"""
def calcularArea(cuadrado:"list"):
    return float(cuadrado[3]) * float(cuadrado[4])

def errorArea( cuadradoVal:"list",cuadradoPrediccion:"list" ):
    return abs( calcularArea(cuadradoPrediccion) - calcularArea(cuadradoVal) )

def errorLocalizacion( cuadradoVal:"list",cuadradoPrediccion:"list" ):
    return math.sqrt( ( float(cuadradoVal[1]) - float(cuadradoPrediccion[1]) )**2 
                    + ( float(cuadradoVal[2]) - float(cuadradoPrediccion[2]) )**2 ) 

def cumpleEjeW(cuadradoVal:"list",cuadradoPrediccion:"list"):
    distancia = abs( float( cuadradoVal[1] ) - float(cuadradoPrediccion[1]) )
    distaniciaMaxima = (float( cuadradoVal[3] ) + float( cuadradoPrediccion[3] ))/2
    return distancia <= distaniciaMaxima

def cumpleEjeH(cuadradoVal:"list",cuadradoPrediccion:"list"):
    distancia = abs( float( cuadradoVal[2] ) - float(cuadradoPrediccion[2]) )
    distaniciaMaxima = (float( cuadradoVal[4] ) + float( cuadradoPrediccion[4] ))/2
    return distancia <= distaniciaMaxima

def estaDentro(cuadradoVal:"list",cuadradoPrediccion:"list"):
    return cumpleEjeH(cuadradoVal,cuadradoPrediccion) and cumpleEjeW(cuadradoVal,cuadradoPrediccion)


diccionarioResultados = {}

listaCurposPrediccion = []
listaCurposValidacion = []
parte = []
for archivo in ficheroPrediccion:
    listaCurposPrediccion = []
    listaCurposValidacion = []

    with open(f"{direccionNuestroPredicciones}/{archivo}", "r", encoding="utf-8") as f:
        id = 0
        for linea in f:
            parte = linea.replace("\n","").split(" ")
            if(parte[0] == "0"):
                parte[0] = id
                id += 1
                listaCurposPrediccion.append( parte )

    with open(f"{direccionNuestroValidacion}/{archivo}", "r", encoding="utf-8") as f:
        id = 0
        for linea in f:
            parte = linea.replace("\n","").split(" ")
            if(parte[0] == "0"):
                parte[0] = id
                id += 1
                listaCurposValidacion.append( parte )
    
    """print("validacion ->")
    print( listaCurposValidacion )
    print("===================")
    print("prediccion ->")
    print( listaCurposPrediccion)"""
    diccionarioResultados[ archivo ] = []
    diccionarioResultados[ f"{archivo}|Resultado" ] = []
    validacionMenor = ""
    distanciaMenor = 100.0
    for predic in listaCurposPrediccion:
        validacionMenor = ""
        distanciaMenor = 100.0
        for valid in listaCurposValidacion:
            bueno = estaDentro(valid,predic)
            dist = errorLocalizacion(valid,predic)
            #print(f"val {valid[0]} - predic {predic[0]} -> {bueno} distacia -> {dist}")

            if(bueno):
                diccionarioResultados[archivo].append( [ valid , predic ,  dist] )
                if( dist < distanciaMenor ):
                    distanciaMenor = dist
                    validacionMenor = valid
        
        if(validacionMenor != "" ):
            diccionarioResultados[f"{archivo}|Resultado"].append( [ validacionMenor , predic ,  distanciaMenor] )


with open( f"resultados.txt","w",encoding="utf-8" ) as f:
    for k in diccionarioResultados.keys():

        f.writelines( f"{k}:{diccionarioResultados[k]}\n" )

    


#print(diccionarioResultados)

