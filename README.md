**Welcome to Unit Commitment App!**

Hi, nice of you to drop by here!

This application was created entirely in Python language to showcase the capabilities of two powerful libraries: dash and pyomo.

My name is Łukasz. I studied power engineering and have been working in the energy sector for many years. On a daily basis, I am responsible for creating software in Python for data visualization, optimization of electricity production processes and support for electricity trading. In these tasks, I widely use, among others: dash and pyomo packages.

Thanks to this, I got familiarized with their powerful possibilities, which can be used in many other processes not only in power sector, namely: finance, health care, fuel sector, agriculture and logistics etc.

Together, these tools provide amazing possibilities: dash as a tool for fast creation of analytical web applications and pyomo to support making optimal business decisions. In the application you, I used a wide variety of functionalities provided by these libraries to prove this thesis.

About unit commitment (source: Wikipedia): The unit commitment problem (UC) in electrical power production is a large family of mathematical optimization problems where the production of a set of electrical generators is coordinated in order to achieve some common target, usually either matching the energy demand at minimum cost or maximizing revenue from electricity production. This is necessary because it is difficult to store electrical energy on a scale comparable with normal consumption; hence, each (substantial) variation in the consumption must be matched by a corresponding variation of the production.

In this application, production costs are minimized to provide a given daily demand profile. You can add, remove and modify the parameters of subsequent types of units: utility power plants (coal, gas and nuclear), batteries, renewable sources (wind and photovoltaic farms) and demand sources. Then you can check the daily cost of electricity production and the energy production profile of individual units, ranked according to their variable cost of energy production.