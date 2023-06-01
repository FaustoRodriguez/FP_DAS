# FP_DAS
Proyecto final para la materia de diseño y arquitectura de software


 5 SOLID practices:
S - Single-responsiblity Principle
Cada funcion del servidor tiene una responsabilidad en particular, como ejemplo está la función getTodayValues que solo se dedica a obtener la lista de un evento en particular para hacer los reportes diarios

O - Open-closed Principle
La función que mejor lo ejemplifica es printTweet de TR_client, donde se encuentra abierta a ser extendida de acuerdo al tipo de tweet pero cerrada a cualquier modificación de su funcionamiento

L - Liskov Substitution Principle
La función GetTodayValues puede ser sustituida por función GetTodayUsers de ser necesario

I - Interface Segregation Principle
Las funciones del cliente solo conocen y llaman las funciones del servidor que necesitan

D - Dependency Inversion Principle
Instead of using one function to look for both tweets and comments we invert the dependency and make one independent function for retrieving the comments based on a tweet ID
 
 3 design patterns:
 Abstract Factory (GetTodayValues en TR_server)

 Singleton (Every function of TR_server is basically a singleton since we're )
 
 Decorator (We add extra functions to the GetTodayValues with each "GetToday" function)

Unit tests in TR_server.py