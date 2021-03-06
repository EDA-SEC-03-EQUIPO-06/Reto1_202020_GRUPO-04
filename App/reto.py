"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv

from ADT import list as lt
from DataStructures import listiterator as it


from time import process_time 



def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de películas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un género")
    print("6- Crear ranking por género")
    print("0- Salir")

def printMenuRanking():
    print("\nElija el tipo de Ranking que desee: ")
    print("1- Ranking de las mejores películas por calificación")
    print("2- Ranking de las peores películas por calificación")
    print("3- Ranking de la películas más votadas")
    print("4- Ranking de las películas menos votadas")


def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1

def greater_function(element1,element2,column):
    if element1[column] > element2[column]:
        return True
    else:
        return False

def less_function(element1,element2,column):
    if element1[column] < element2[column]:
        return True
    else:
        return False


def loadCSVFile (file, cmpfunction):
    lst=lt.newList("ARRAY_LIST", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter=";"
    try:
        with open(  cf.data_dir + file, encoding="utf-8") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
    except:
        print("Hubo un error con la carga del archivo")
    return lst


def loadMovies ():
    lst = loadCSVFile("themoviesdb/AllMoviesCastingRaw.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def loadDetails():
    lst = loadCSVFile("themoviesdb/AllMoviesDetailsCleaned.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def tipoRanking(num):
    if num==1:
        column="vote_average"
        cmpfunction=greater_function
        tipo="mejores"
    elif num==2:
        column="vote_average"
        cmpfunction=less_function
        tipo="peores"
    elif num==3:
        column="vote_count"
        cmpfunction=greater_function
        tipo="mejores"
    elif num==4:
        column="vote_count"
        cmpfunction=less_function
        tipo="peores"
    else:
        print("Número icorrecto, vuélvalo a intentar")
        sys.exit(0)
    if num==1 or num==2:
        tipocalificacion= " con su respectiva calificación "
    else:
        tipocalificacion= " con su respectivo número de votos "
    return column,cmpfunction,tipo,tipocalificacion
    
"""


Requerimiento 2


"""
def Ranking(column,details,compfunction, elements):
    """
    Retorna una lista con cierta cantidad de elementos ordenados por el criterio
    """
    t1_start = process_time() #tiempo inicial
    copia = lt.subList(details,1,details["size"])
    lt.shellSort(copia,compfunction,column)
    iterator=it.newIterator(copia)
    ranking={}
    x=1
    while it.hasNext(iterator) and x<=elements:
        element=it.next(iterator)
        ranking[element.get("original_title")]= element.get(column)
        x+=1
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return ranking

"""


Requerimiento 3


"""

def conocerDirector(criteria, column, casting, details):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    t1_start = process_time() #tiempo inicial
    counter=-1
    promedio = 0
    l_pelis = []
    iterator = it.newIterator(casting)
    i_details = it.newIterator(details)
    while  it.hasNext(iterator):
        element_casting = it.next(iterator)
        element_details = it.next(i_details)
        if criteria.lower() in element_casting[column].lower(): #filtrar por palabra clave 
            l_pelis.append(element_details["title"])
            promedio += float(element_details["vote_average"]) 
            counter+=1           
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return (str(counter+1)+" pelis:\n"+ str(l_pelis)+ " \n Su calificación promedio es: "+str(round(promedio/(counter+1),2)))

"""


Requerimiento 4


"""
def conocerActor(actor_name, lc, lm):
    t1_start = process_time()
    n_pelis = []
    prom = 0
    director =[]
    d2 = []
    mayor = 0
    n_mayor = " "
    i_movies = it.newIterator(lm)
    i_casting = it.newIterator(lc)
    while it.hasNext(i_casting):
        e_movies = it.next(i_movies)
        e_casting = it.next(i_casting)
        if (actor_name.lower() == e_casting["actor1_name"].lower()) or (actor_name.lower() == e_casting["actor2_name"].lower()) or (actor_name.lower() == e_casting["actor3_name"].lower()) or (actor_name.lower() == e_casting["actor4_name"].lower()) or (actor_name.lower() == e_casting["actor5_name"].lower()):
            n_pelis.append(e_movies["title"])
            prom += float(e_movies["vote_average"])
            director.append(e_casting["director_name"])
            if (e_casting["director_name"]) not in d2:
                d2.append(e_casting["director_name"])
    for i in d2:
        if mayor< director.count(i):
            mayor = director.count(i)
            n_mayor = i
    t1_stop = process_time()
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    if len(n_pelis)!=0:
        return (len(n_pelis), n_pelis, round(prom/len(n_pelis),2), n_mayor)
    return "El Actor no está en la lista :c"
"""


Requerimiento 5


"""
def peliculasPorGenero(lst, criteria):
    t1_start = process_time()
    votos = 0
    cantidad = 0
    peliculas = []
    i_file = it.newIterator(lst)
    while it.hasNext(i_file):
        movie = it.next(i_file)
        if criteria.lower() in movie["genres"].lower():
            votos += int(movie["vote_count"])
            cantidad += 1
            peliculas.append(movie["original_title"])
    promedio = round(votos/cantidad,2)
    t1_stop = process_time()
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return (peliculas, cantidad, promedio)

def RankingGenero (genero, column, details, compfunction, elements):
    #Se crea una lista por género
    t1_start = process_time() #tiempo inicial
    lista_genero=lt.newList("ARRAY_LIST")
    iterator_details=it.newIterator(details)
    while it.hasNext(iterator_details):
        element_details=it.next(iterator_details)
        if genero.lower() in element_details.get("genres").lower() :
            lt.addLast(lista_genero,element_details)
    #Se ordena la lista por género
    lt.shellSort(lista_genero,compfunction,column)
    #Se hace el ranking
    ranking={}
    iterator_listag=it.newIterator(lista_genero)
    x=1
    while it.hasNext(iterator_listag) and x<=elements:
        element=it.next(iterator_listag)
        ranking[element.get("original_title")]= element.get(column)
        x+=1
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    
    return ranking

def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """


    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:

            if int(inputs[0])==1: #opcion 1
                casting =loadMovies()
                details=loadDetails()
            elif int(inputs[0])==2: #opcion 2
                if details==None or details['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    printMenuRanking()
                    tiporanking= int(input("Dígite su opción: "))
                    datos=tipoRanking(tiporanking)
                    column=datos[0]
                    cmpfunction= datos[1]
                    tipo=datos[2]
                    tipocalificacion=datos[3]
                    elements=int(input("Dígite el número de películas que desea ver en el ranking: "))
                    ranking=Ranking(column, details,cmpfunction,elements)
                    print("Las "+str(elements)+" "+ str(tipo) + " películas" + str(tipocalificacion)+ "son: \n" + str(ranking))

            elif int(inputs[0])==3: #opcion 3
                if casting==None or casting['size']==0 or details==None or details['size']==0: #obtener la longitud de la lista
                    print("Alguna de las listas está vacía")
                else:
                    director = input("Director a consultar: ")
                    counter=conocerDirector(director,"director_name", casting, details)
                    print("El Director", director.capitalize()," tiene "+ str(counter))

            elif int(inputs[0])==4: #opcion 4
                actor = input("Actor a consultar: ")
                r = conocerActor(actor, casting , details)
                print("El actor " + actor.capitalize() + " tiene: " + str(r[0])+" películas")
                print("la lista de sus películas es: \n"+str(r[1]))
                print("El promedio de calificación de sus películas es: "+str(r[2]))
                print("El nombre del director con más colaboraciones es: "+str(r[3]))



            elif int(inputs[0])==5: #opcion 5
                criteria = input("¿Cuál género quieres buscar?: ")
                a = peliculasPorGenero(details,criteria)
                print("Hay ", a[1], " películas del genero ", criteria)
                print("El promedio de cantidad de votos para este genero es de ", a[2])
                print("Estas son algunas de las películas del género:")
                tenpelis = []
                for i in range(10):
                    tenpelis.append(a[0][i])
                print(tenpelis)

            elif int(inputs[0])==6: #opcion 6
                if details==None or details['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    genero=input("Dígite el género por el que desee hacer el ranking: ")
                    printMenuRanking()
                    tiporanking= int(input("Dígite su opción: "))
                    datos=tipoRanking(tiporanking)
                    column=datos[0]
                    cmpfunction= datos[1]
                    elements= int(input("Dígite el número de películas que desea ver en el ranking: "))
                    ranking_genero=RankingGenero(genero,column,details,cmpfunction,elements)
                    print("Las "+str(elements)+" "+ str(datos[2]) + " películas de " + genero.capitalize() + str(datos[3])+ "son: \n" + str(ranking_genero))

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()
