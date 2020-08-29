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
from DataStructures import liststructure as lt
from Sorting import shellsort as ss

from time import process_time 



def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
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
    lst = loadCSVFile("Data/theMoviesdb/movies-small.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def loadDetails():
    lst = loadCSVFile("Data/themoviesdb/SmallMoviesDetailsCleaned.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def RankingGenero (genero, column, details,casting, compfunction, elements):
    #Se crea una lista por género
    t1_start = process_time() #tiempo inicial
    lista_genero=lt.newList("ARRAY_LIST", cmpfunction)
    iterator_casting=it.newIterator(casting)
    iterator_details=it.newIterator(details)
    while it.hasNext(iterator_casting):
        element_casting=it.next(iterator_casting)
        element_details=it.next(iterator_casting)
        if genero.lower() in element_casting.get("genres").lower():
            lt.addLast(lista_genero,element_details)
    #Se ordena la lista por género
    ss.shellSort(lista_genero,compfunction,column)
    #Se hace el ranking
    ranking=lt.newList("ARRAY_LIST", cmpfunction)
    iterator_listag=it.newIterator(lista_genero)
    x=1
    while it.hasNext(iterator_listag) and x<=elements:
        element=it.next(iterator_listag)
        ranking.append(element.get("original_title"))
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
                casting = loadMovies()
                details=loadDetails()
            elif int(inputs[0])==2: #opcion 2
                pass

            elif int(inputs[0])==3: #opcion 3
                pass

            elif int(inputs[0])==4: #opcion 4
                pass

            elif int(inputs[0])==5: #opcion 5
                pass

            elif int(inputs[0])==6: #opcion 6
                if details==None or details['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    genero=input("Dígite el genero por el que desee hacer el ranking: ")
                    printMenuRanking()
                    tiporanking= int(input("Dígite su opción: "))
                    elements=int(input("Dígite el número de películas que desea ver en el ranking: "))
                    if tiporanking==1:
                        column="vote_average"
                        cmpfunction=greater_function
                        tipo="mejores"
                    elif tiporanking==2:
                        column="vote_average"
                        cmpfunction=less_function
                        tipo="peores"
                    elif tiporanking==3:
                        column="vote_count"
                        cmpfunction=greater_function
                        tipo="mejores"
                    elif tiporanking==4:
                        column="vote_count"
                        cmpfunction=less_function
                        tipo="peores"
                    ranking_genero=RankingGenero(genero,column,details,casting,cmpfunction,elements)
                    print("Las "+str(elements)+ tipo + "películas de" + genero + "son: \n" + str(ranking))

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()