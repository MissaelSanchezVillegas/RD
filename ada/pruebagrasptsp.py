import grasptsp
import graph
import InstanciesGenerator
import TSPproblem
import os
import time 
import string
#dd = InstanciesGenerator.Distribution(InstanciesGenerator.DistributionsTypes.uniform, 10, 2)
#dw = InstanciesGenerator.Distribution(InstanciesGenerator.DistributionsTypes.uniform, 1, 10)
#generador = InstanciesGenerator.GraphInstancesGenerator(graphtype = InstanciesGenerator.GraphTypes.complete,distribution_weight = dw,distribution_degree = dd, directed = False )
#g = generador.generateInstance('Test', 5, 20)

#prob = TSPproblem.TSPProblem()
#print(prob.graph.to_string())
f=open('resultados.txt', 'w')
listaalpha=[0.4]
listaitergrasp=[8]
replicas=1
listatext=os.listdir('Instancies')
listasol=list()
f.write("instancia, alpha, numeroiteracionesgrasp, valoroptimo, valorobjetivo, iteracionmejorsolucion, tiempohallarmejorsolucion, tiempototal \n")
for i in listatext:
	for alpha in listaalpha:
		for a in range(0,replicas):
			for itergrasp in listaitergrasp:
				path='instancies/' + i
				nam = i.split('.')
				spath='optimo/' + nam[0] +'.opt.tour'
				tiemposol=time.clock()
				s = grasptsp.graspTSP( itergrasp, alpha, tiemposol, path=path, solpath=spath, key='distance')
				tiempotot=time.clock()-tiemposol-s[5]
				f.write(str(i)+str(" ")+str(alpha)+str(" ")+str(itergrasp)+str(" ")+str(s[6])+str(" ")+str(s[1])+str(" ")+str(s[2]+1)+str(" ")+str(s[4])+str(" ")+str(tiempotot)) #(nombre de la instancia, valor alpha, num iter grasp, numero de replica, valor objetivo, iteracion que hallo la mejor, tiempo en hallar la mejor sol, tiempo en ejecutar)
				f.write("\n")
				#listasol.append((s,tiempotot, i))
	print("instancia: ",i)
f.close()
#for x in listasol:
#	print(x[2],x[0][1], x[0][2], x[0][4], x[1]) #(nombre de la instancia, valor objetivo, iteracion que hallo la mejor, tiempo en hallar la mejor sol, tiempo en ejecutar)
