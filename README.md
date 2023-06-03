# FP_DAS
Proyecto final para la materia de diseño y arquitectura de software

Proyecto estructurado basado en domain driven design

 5 SOLID practices:
S - Single-responsiblity Principle
Podemos ver este principio en la clase server_connection en TR_server, donde la clase padre solo hace la conección al servidor de la base de datos y define las funciones más basicas: getData, postData y updateData, todo lo demás responsabilidad del servidor es expandido con las clases necesarias para ello: server_connection_client para el cliente y server_connection_dash para dashboard de eventos, de esta forma no sobrecargamos a una sola clase los metodos para la aplicacion del cliente y los que son para el dashboard de eventos

O - Open-closed Principle
Este principio es aplicado en la clase server_connection_client donde mantenemos cerrado a modificación o un exceso de carga el constructor de la clase server_connection pero lo extendemos con el constructor de server_connection_client donde agregamos la función logIn para registar el uso de la aplicación, algo que no es necesario para la clase padre


L - Liskov Substitution Principle
Implementamos esto en la clase screenPrinter donde establecemos la misma función (printTweet) para las clases herederas dashPrinter y TwitterPrinter pero con diferente funcionalidad dados los requerimientos de cada caso


I - Interface Segregation Principle


D - Dependency Inversion Principle
Instead of using one function to look for both tweets and comments we invert the dependency and make one independent function for retrieving the comments based on a tweet ID
 
 3 design patterns:
 Abstract Factory (GetTodayValues en TR_server)

 Singleton:

 En TR_client la clase screenPrinter usa el patron singleton para solo utilizar una instancia de esa clase

 Decorator (We add extra functions to the GetTodayValues with each "GetToday" function)

Unit tests en la carpeta [tests](/tests)