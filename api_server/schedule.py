__author__ = 'JAPeTo <jeffersonamado@gmial.com>'
import os
import sys


def alg_fifo(data=None, debug=False):
    _processes = data['jobs']
    _maxExecTime = 0
    _currentProc = None
    _doneTasks = []
    _quantomSpent = 0
    _avgWaitTime = 0
    _avgResponseTime = 0
    _avgTurnAroundTime = 0

    _taskQueue = []
    _tik = 0
    while True:
        for proc in _processes:
            if proc['arrival_time'] == _tik:
                proc['remaining_time'] = proc['execution_time']
                _taskQueue.append(proc)
                if debug: print("process ", proc['name'], " arrived")

        if _currentProc:
            _currentProc['remaining_time'] -= 1
            _quantomSpent += 1
            if _currentProc['remaining_time'] == 0: #task Done
                if debug: print ("process ", _currentProc['name']," done...")
                _currentProc['finish_time'] = _tik + 1
                _doneTasks.append(_currentProc)
                _currentProc = None
        else:
            if len(_taskQueue) > 0:
                _currentProc = _taskQueue.pop(0)
                _currentProc['start_time'] = _tik
                _currentProc['remaining_time'] -= 1
                _quantomSpent += 1
                if _currentProc['remaining_time'] == 0:
                    if debug: print ("process ", _currentProc.name, " done...")
                    _currentProc['finish_time'] = _tik + 1
                    _doneTasks.append(_currentProc)
                    _currentProc = None
            else:
                if len(_doneTasks) == len(_processes):  # all processes done
                    if debug: print("all processes done...")
                    _tik += 1
                    break

        _tik = _tik + 1

    count = len(_doneTasks)
    for proc in _doneTasks:
        temp = (proc['finish_time'] - proc['execution_time'] - proc['arrival_time'])
        _avgWaitTime += temp
        temp = proc['start_time'] - proc['arrival_time']
        _avgResponseTime += temp
        temp = proc['finish_time'] - proc['arrival_time']
        _avgTurnAroundTime += temp

    _avgTurnAroundTime = float(_avgTurnAroundTime) / float(count)
    _avgWaitTime = float(_avgWaitTime) / float(count)
    _avgResponseTime = float(_avgResponseTime) / float(count)
    if debug: print ("avg waitTime: ", _avgWaitTime)
    if debug: print ("avg Respose: ",_avgResponseTime)
    if debug: print ("avg TurnAroundTime: ",_avgTurnAroundTime)

    data['avg_wait_time']=_avgWaitTime
    data['avg_response_time']=_avgResponseTime
    data['avg_turnaround_time']=_avgTurnAroundTime

    return data
####
#Autor: Juan Calos Ballesteros Romero
def sjf(data=None):
    ###Se ordenan los trabajos de menor a mayor tiempo de ejecucion
    proceso = data['jobs']
    cola=[]
    guardar=[]
    i=0
    cola.append(proceso[0])
    proceso.pop(0)
    for proc in proceso:
        if cola[i]['execution_time']<proc['execution_time']:
            cola.append(proc)
        else:
            guardar=cola[i]
            cola[i]=proc
            cola.append(guardar)
        i+=1

    data['jobs']=cola
    ###Con los procesos ordenados se realiza el algorimo fifo
    alg_fifo(data=data, debug=None)
    

def rr(data=None):
    proceso = data['jobs']
    cola=[]
    cpu=data['quatum']
    contador=[]
    posicion=len(proceso)
    i=0

    bandera=0

    for proc in proceso:
        cola.append(proceso[i]['execution_time'])
        contador.append(proceso[i]['execution_time'])
        i+=1
    i=0
    for proc in cola:
        contador[i]=0
        if cola[i]<0:
            bandera+=1
        i+=1
    while bandera<len(cola):
        i=0
        for proc in proceso:
            if cpu > proceso[i]['execution_time']:
                proceso[i]['execution_time']=0
                posicion+=1
            elif proceso[i]['execution_time']>0:
                    proceso[i]['execution_time']-=cpu
                    cola.append(proceso[i]['execution_time'])
                    posicion+=1
                    if proceso[i]['execution_time']!=0:
                         contador[i]=posicion
    
            i+=1
            
        i=0
        for proc in proceso:
            if proceso[i]['execution_time']<=0:
               bandera+=1
               i+=1
    i=0
    for proc in proceso:
        proceso[i]['execution_time']=contador[i]
        i+=1

    _avgWaitTime = 0
    _avgResponseTime = 0
    _avgTurnAroundTime = 0
    count = len(proceso)
    for proc in proceso:
        temp = proc['execution_time']
        _avgWaitTime += temp
        _avgResponseTime += _avgWaitTime
        _avgTurnAroundTime += _avgResponseTime

    _avgTurnAroundTime = float(_avgTurnAroundTime) / float(count)
    _avgWaitTime = float(_avgWaitTime) / float(count)
    _avgResponseTime = float(_avgResponseTime) / float(count)

    data['avg_wait_time']=_avgWaitTime
    data['avg_response_time']=_avgResponseTime
    data['avg_turnaround_time']=_avgTurnAroundTime

    return data


