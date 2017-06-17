import graph
import random
import TSPproblem
import math
import time

def graspTSP(iters, alpha, tiempo, probgraph =None, path =None, solpath=None, key='weight',):
    
    sa = (None, math.inf)                                                                     
    bs, bv = sa
    fi=0
    ti = time.clock()
    if probgraph is not None and path is None:
        tspp = TSPproblem.TSPProblem(graph = probgraph)
    else:
        tspp = TSPproblem.TSPProblem(path=path)

    if solpath is not None:
        assign = tspp.bestsolution(solpath)
        optval = tspp.evaluate(assign,key)
    else:
        assign = None
        optval = 0
    tf = time.clock() - ti
    sl = []
    #print(tspp.graph)
    for i in range(iters):
        so = greedyconstructive(tspp, alpha, key)
        #print(so, time.clock())
        ls = localsearch(tspp,so, key)
        av = tspp.evaluate(ls, key)
        if bv >= av:
            bs = ls
            bv = av
            fi = i
            besttimesol=time.clock()-tiempo-tf
        sl.append((i, ls,av))
        #print(so, ae, ls,be)
    return bs, bv, fi, sl, besttimesol, tf, optval, assign, 

def greedyconstructive(prob, alpha, key='weight'):
    path = []
    vl = list(prob.graph.vertices.keys())
    elem = random.choice(vl)
    si = elem
    #pendiente
    pl ={elem}
    vl.remove(elem)
    while len(vl)>0:
        #print(prob.graph[elem].neighbors.keys(), pl)
        nl = list(set(prob.graph[elem].neighbors.keys()) - pl)
        if len(nl) == 0:
            break
        wnl = [(x, prob.graph[elem].neighbors[x][key]) for x in nl ]
        onl = sorted(wnl, key=lambda x:x[1])
        lim = round(alpha*len(onl)) if round(alpha*len(onl)) > 1 else 1
        rcl = onl[0:lim]
        ce = random.choice(rcl)
        #print (nl, elem, ce[0], ce[1])
        tup = (elem, ce[0], ce[1])
        path.append(tup)
        elem = ce[0]
        pl.add(ce[0])
        vl.remove(ce[0])
    if len(path) == (prob.graph.cardinal)-1:
        path.append((elem, si, prob.graph[elem].neighbors[si][key]))
    return path
    
def localsearch(prob, so, key='weight'):
    k=so.copy()
    sa=so.copy()
    mejorso=so
    menorval=valor(so)
    temp=0
    while(temp!=mejorso):
        temp=mejorso
        mejorso=vec1(prob, mejorso)
        #print("\n mejorso: ",mejorso)
        #print("value: ", valor(mejorso))
    #vec2(prob,k)
    #time.sleep(1)
            

    return mejorso

def distancia(prob,a,b):
    return prob.graph[str(a)].neighbors[str(b)]['distance']

def valor(sa):
    suma=0
    for (a,b,c) in sa:
        suma+=c
    return suma

def vec1(prob, so, bi = False): #2opt
    conjunto=list()
    k=so.copy()
    sa=so.copy()
    mejorso=so
    menorval=valor(so)
    for (i,j,c) in so: #seleccionar una arista
        k.remove((i,j,c))
        for(a,b,d) in k: #seleccionar siguientes aristas
            if(j==a):     #aristas consecutivas no cuentan
                continue
            sa[so.index((i,j,c))]=(i,a,distancia(prob,i,a))    #primera arista seleccionada
            sa[so.index((a,b,d))]=(j,b,distancia(prob,j,b))    #segunda arista modificada
            sa[so.index((i,j,c))+1:so.index((a,b,d))]=so[so.index((a,b,d))-1:so.index((i,j,c)):-1] #al reves las aristas de el segmento de enmedio
            for (m,n,o) in sa[so.index((i,j,c))+1:so.index((a,b,d))]:  #cambiar la direccion de las aristas
                sa[sa.index((m,n,o))]=(n,m,o)
            conjunto.append(sa)
            valorsol=valor(sa)
            if(valorsol<menorval):
                if not bi:
                    return sa
                else:
                    mejorso=sa
                    menorval=valorsol
            sa=so.copy()
    #print("\n valor anterior: ",valor(so))
    #print("mejorval: ",valor(mejorso))
    if(valor(so)==valor(mejorso) and False):
        while(len(conjunto)>0):
            so=conjunto.pop()
            k=so.copy()
            sa=so.copy()
            for (i,j,c) in so: #seleccionar una arista
                k.remove((i,j,c))
                for(a,b,d) in k: #seleccionar siguientes aristas
                    if(j==a):     #aristas consecutivas no cuentan
                        continue
                    sa[so.index((i,j,c))]=(i,a,distancia(prob,i,a))    #primera arista seleccionada
                    sa[so.index((a,b,d))]=(j,b,distancia(prob,j,b))    #segunda arista modificada
                    sa[so.index((i,j,c))+1:so.index((a,b,d))]=so[so.index((a,b,d))-1:so.index((i,j,c)):-1] #al reves las aristas de el segmento de enmedio
                    for (m,n,o) in sa[so.index((i,j,c))+1:so.index((a,b,d))]:  #cambiar la direccion de las aristas
                        sa[sa.index((m,n,o))]=(n,m,o)
                    valorsol=valor(sa)
                    if(valorsol<menorval):
                        mejorso=sa
                        menorval=valorsol
                    sa=so.copy()
        print("valor total: ",menorval)
    return mejorso


def convertir(prob, sa):
    so=list()
    for i in range(0,len(sa)-1):
        so.append((sa[i],sa[i+1],distancia(prob,sa[i],sa[i+1])))
    return so
