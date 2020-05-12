#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:05:37 2020
solution to hw1
@author: liwenouyang
"""

import puzz, queue , heapq, os, time ,sys 

def BFS(init,goal):
    Frontier = queue.Queue(0)
    Frontier.put(('start',init,''.join(init._board)))
    Fsize = 1
    numE = 0
    visited={}
    sol =[]
    while not Frontier.empty():
        c = Frontier.get()
        b = c[1]
        bstr = ''.join(b._board)
        visited[bstr] = (c[0],c[2]) ##Keep track of the solution  TODO
        numE += 1
        for item in b.successors().items():
            if (not item[1] is None) and (not ''.join(item[1]._board) in visited):
                if b._board == goal._board:
                    g = bstr
                    sol.insert(0,('Goal',g))
                    p = visited[g][1]
                    while not g == p:
                        sol.insert(0,(visited[p][0],visited[g][1]))
                        g = visited[g][1]
                        p = visited[g][1]
                    return [sol,Fsize,numE]
                Frontier.put(item+(bstr,))
                Fsize+= 1
    return None,Fsize,numE
        



def GenericHeuristic(init,goal,H):  ##Figure out the generic heuristic funtion's parameter 
    Frontier = []
    heapq.heappush(Frontier,(0,1,('start',init),''.join(init._board),0))
    visited = {}
    sol = []
    Fsize = 1
    numE = 0
    while not len(Frontier) == 0:
        c = heapq.heappop(Frontier)
        b = c[2][1]
        bstr = ''.join(b._board)
        visited[bstr] = (c[2][0],c[3])
        if b._board == goal._board:
            g = bstr
            sol.insert(0,('Goal',g))
            p = visited[g][1]
            while not g == p:
                sol.insert(0, (visited[p][0],visited[g][1]))
                g = visited[g][1]
                p = visited[g][1]
            return [sol,Fsize,numE]
        else:
            numE += 1
            for item in b.successors().items():
                if (not item[1] is None) and (not ''.join(item[1]._board) in visited):
                    heapq.heappush(Frontier,(H(c[4],item[1],goal),Fsize,item,bstr,c[4]+1))
                    Fsize += 1
    return None,Fsize,numE
                    
def Uniform(init,goal):
    def H(a,b,c):
        return a 
    return GenericHeuristic(init, goal, H)
    

def Manhattan(current,goal):
    count = 0
    for i in range(1,9):
        c = current._board.index(str(i)) % 3 ,  current._board.index(str(i)) //3
        g = goal._board.index(str(i)) % 3 ,  goal._board.index(str(i)) //3
        count += abs(c[0]-g[0]) + abs(c[1]-g[1])
    return count

def MissTile(current,goal):
    count = 0
    for i in range(1,9):
        if not current._board.index(str(i)) == goal._board.index(str(i)):
            count += 1
    return count 


def GreedyManhat(init,goal):
    def H(c,a,b):
        return Manhattan(a, b)
    return GenericHeuristic(init, goal, H)


def AManhat(init,goal):
    def H(c,a,b):
        return c + Manhattan(a,b)
    return GenericHeuristic(init, goal, H)

def GreedyCount(init,goal):
    def H(c,a,b):
        return MissTile(a,b)
    return GenericHeuristic(init, goal, H)

def ACount(init,goal):
    def H(c,a,b):
        return c + MissTile(a,b)
    return GenericHeuristic(init, goal, H)



if __name__ == '__main__':
    method = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]
    i = puzz.EightPuzzleBoard(start)
    g = puzz.EightPuzzleBoard(end)
    if method == 'bfs':
        sol = BFS(i,g)
    elif method == 'ucost':
        sol = Uniform(i, g)
    elif method == 'greedy-manhat':
        sol = GreedyManhat(i, g)
    elif method == 'greedy-count':
        sol = GreedyCount(i, g)
    elif method == 'astar-manhat':
        sol = AManhat(i, g)
    elif method == 'astar-count':
        sol = ACount(i,g)
    if sol[0] is None:
        print('No solution')
        print('Frontier:' + repr(sol[1])+'\n'+'expanded'+ repr(sol[2]))
    else:
        for i in sol[0]:
            print(i[0]+ '\t'+i[1]+'\n')
        print("Path cost:"+ repr(len(sol[0])-1) +'\n'+ 'Frontier:' + repr(sol[1])+'\n'+'expanded'+ repr(sol[2]))
   ##Yeet, implement user IO bS

"""
    for state in sol:
     os.system("clear")
     print(puzz.EightPuzzleBoard(state[1]).pretty())
     time.sleep(0.5)
"""