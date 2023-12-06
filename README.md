# mogpl_project
Algorithme de Bellman-Ford et amélioration

L’algorithme de Bellman-Ford est une méthode de base pour calculer les plus courts chemins à
source unique dans les graphes avec des poids d’arête à la fois positifs et négatifs. Sa durée
d’exécution dépend de l’ordre dans lequel l’algorithme sélectionne les sommets pour les mises à
jour itératives de la valeur de leur plus court chemin.
Notre objectif principal est d’améliorer le temps d’exécution de l’algorithme de Bellman-Ford dans le
cas où les exemples ne sont pas les pires. Pour ce faire, nous introduisons une étape de prétraitement
à l’algorithme de Bellman-Ford qui, étant donné une collection d’instances typiques, sélectionne un
bon ordre pour examiner les sommets. Ce faisant, nous autorisons un coût de prétraitement plus
important (mais toujours polynomial) afin de réduire le temps d’exécution par instance.
