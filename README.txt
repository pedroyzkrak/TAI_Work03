O programa a correr é o program.py

O ficheiro compressor_results.py é um módulo usado para efetuar os testes selecionados no program.py

Os módulos dos compressores, onde se obtém os resultados NCD estão situados na pasta /compressor_modules/

O dataset foi carregado para a pasta /orl_faces_raw/

A pasta /results/ contém os resultados já obtidos do full test (Todos os compressores e 8 conjuntos de imagens de referência diferentes)
A pasta /results/metrics/ contém o ficheiro metrics_NCD.txt onde se pode verificar a precisão, recall e f1-measure para cada
sujeito, bem como os resultados totais para esse teste, de um compressor usando um determinado conjunto de referência

A pasta /results/conf_matrix/ contém as matrizes de confusão para cada compressor em cada conjunto de referência.
Os testes são organizados por sub-pastas, sendo uma subpasta para um determinado conjunto de referência, onde se encontram os
resultados de cada compressor para esse conjunto de referência.

No programa é também possível efetuar testes parciais, podendo-se escolher que compressor usar e que conjunto de referência para
efetuar os testes. É também possível introduzir um conjunto de referência manualmente.

No programa existe o comando "info" para disponibilizar no ecrã informação sobre cada teste, bem como os compressores disponíveis 
e conjuntos de referência pré-definidos.

