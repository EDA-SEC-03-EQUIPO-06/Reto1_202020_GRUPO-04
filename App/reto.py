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
    print("6- Crear ranking")
    print("0- Salir")




def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1



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


def loadMovies (archivo):
    lst = loadCSVFile(archivo,compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def r3(dname, lc, lm):
    t1_start = process_time()
    n_pelis = []
    prom = 0
    i_movies = it.newIterator(lm)
    i_casting = it.newIterator(lc)
    while it.hasNext(i_casting):
        e_movies = it.next(i_movies)
        e_casting = it.next(i_casting)
        if dname.lower() == e_casting["director_name"].lower():
            n_pelis.append(e_movies["title"])
            prom += float(e_movies["vote_average"])
    t1_stop = process_time()
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    if len(n_pelis)!=0:
        return (len(n_pelis), n_pelis, round(prom/len(n_pelis),2))
    return "El director no esta en  lista :c"


def r4(actor_name, lc, lm):
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
        if (actor_name.lower() == e_casting["actor1_name"].lower()) or (actor_name.lower() == e_casting["actor2_name"].lower()) or (actor_name.lower() == e_casting["actor3_name"].lower()):
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
    print("Tiempo de ejecución ",t1_stop-t1_start," 1segundos")
    if len(n_pelis)!=0:
        return (len(n_pelis), n_pelis, round(prom/len(n_pelis),2), n_mayor)
    return "El Actor no esta en  lista :c"
   
def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """


    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs = input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:

            if int(inputs[0])==1: #opcion 1
                lstmovies = loadMovies("themoviesdb/SmallMoviesDetailsCleaned.csv")
                lstCasting = loadMovies("themoviesdb/MoviesCastingRaw-small.csv")                

            elif int(inputs[0])==2: #opcion 2
                pass

            elif int(inputs[0])==3: #opcion 3
                dname = input("Director: ")
                if dname != "":
                    print(r3(dname, lstCasting, lstmovies))
                print("Nombre Vacio")
                

            elif int(inputs[0])==4: #opcion 4
                actor_name = input("Actor: ")
                print(r4(actor_name,lstCasting, lstmovies))

            elif int(inputs[0])==3: #opcion 5
                pass

            elif int(inputs[0])==4: #opcion 6
                pass


            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()
