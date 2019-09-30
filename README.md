# Probabilistic-Models

This repository contains all my learning's about advanced topics of Machine Learning involving Statistics and Probability.



## Installations for the repo

The packages used to install for the project are:

1. Numpy, Pandas, tabulate which can be installed either by using conda or pip using the commands  

   >  conda install numpy pandas tabulate
   >
   > ​						or
   >
   > pip install numpy pandas tabulate

2. Graphviz for the visualizations of the graphs which can be installed using the same procedure as above but we need to give the Graphviz executables to the system PATH.

   1. The commands used are:

      1. > conda install python-graphviz  
         >
         > ​		    or
         >
         > ​		pip install graphviz

      2.  Then install graphviz from [Graphviz](http://www.graphviz.org/download/)

      3. Add the graphviz file extension to the system PATH.

      4. If you cannot add the extension to the system path use the code below and add it in the beginning of using the Graphviz package.

         ```python
         import os
         
         os.environ[ "PATH" ] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
         ```

         Use your systems **Graphviz** bin PATH instead :)

3. 

   