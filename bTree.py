import csv
from math import *
import time

class Node:
    def __init__(self, isLeaf):
        self.key =  []
        self.value =  []
        self.isLeaf = isLeaf
        self.child = []
        self.parent = object()
        self.childIdx = 0


class Tree:
    def __init__(self, order=3):
        self.order = order
        self.maxKey = order -2 # 0 부터 시작해서 2 뺴기
        self.root = Node(True) # 최초에는 루트노드가 leaf
        self.returnValue = []
        self.maxChilds = order
        self.maxKeys = order -1
        self.minKeys = round(order/2) - 1 #  except root node
        self.count = 0


    def searchKey(self, key, node, idx):
        currNode = node # 현재 순회하고 있는 노드
        i = idx # 순회해야할 key idx

        # print("CURRENT KEY:",currNode.key[i],'| VALUE:',currNode.value[i],'| ISLEAF:',currNode.isLeaf, '| NEED TO FIND:',key, '| MAXKEY: ', self.maxKey)

        while(i <= self.maxKey):
            if currNode.key[i] < key and i == len(currNode.key) -1 and currNode.isLeaf == False: # 찾으려는 key 값이 더 크고 끝자락일 경우
                self.searchKey(key, currNode.child[i+1],0)
            elif currNode.key[i] < key and i < len(currNode.key) -1: # 찾으려는 key 값이 더 크고 끝자락이 아닐 경우
                self.searchKey(key, currNode, i+1)
            elif currNode.key[i] < key and i == self.maxKey and currNode.isLeaf == False : # 찾으려는 key 값이 더 크고 끝자락에 닿았을 경우
                self.searchKey(key, currNode.child[i+1], 0)
            elif currNode.key[i] > key and currNode.isLeaf == False: # 찾으려는 key 값이 더 작을 경우
                self.searchKey(key, currNode.child[i], 0)
            elif currNode.key[i] == key: # 찾으려는 키값의 경우
                self.returnValue.append([])
                appendValue = str(currNode.key[i]) + ' ' + str(currNode.value[i])
                self.returnValue[len(self.returnValue) - 1].append(appendValue)
            else:
                self.returnValue.append([])
                appendValue = str(key) + ' ' + 'N/A'
                self.returnValue[len(self.returnValue) - 1].append(appendValue)
            return

    def divideNode(self, node, idx):

        if (len(node.key) >= self.order ):
            # 위로 올릴 key, value
            pushIdx = len(node.key) // 2
            pushKey = node.key[pushIdx]
            pushValue = node.value[pushIdx]


            # 오른쪽에 붙일 새로운 child
            newChildNode = Node(node.isLeaf)

            # 새로운 child 와  key, value  분할
            newChildNode.key = node.key[pushIdx+1:]
            node.key = node.key[:pushIdx]
            newChildNode.value = node.value[pushIdx+1:]
            node.value = node.value[:pushIdx]

            # 새로운 child 는 기존 node 의 childIdx+1 번째 자식인된다
            newChildNode.childIdx = node.childIdx + 1

            # 루트를 분할해야할 경우 해당 부모가 root 가 된다
            if(self.root.key == node.key):
                newRootNode = Node(False)
                self.root = newRootNode
                self.root.child.append(node)
                node.parent = self.root
                # idx += 1
            newChildNode.parent = node.parent

            # 부모노드에 key, value insert
            parentNode = node.parent
            parentNode.key.insert(idx, pushKey)
            parentNode.value.insert(idx, pushValue)

            # leaf 노드가 아니면 그 아래 자식들도 이동
            if node.isLeaf == False:
                newChildNode.child = node.child[pushIdx+1:]
                for i in range(pushIdx+1, len(node.child)): # 새로운 부모 지정
                    node.child[i].parent = newChildNode
                    node.child[i].childIdx = i - (pushIdx+1)
                node.child = node.child[:pushIdx+1]

            # 부모노드에 새 child insert
            parentNode.child.insert(idx+1, newChildNode)

            # newChildNode 오른쪽으로 기존에 있던 자식들 childIdx update
            for i in range(newChildNode.childIdx+1, len(parentNode.child)):
                parentNode.child[i].childIdx = i

            # print()
            # print("divideNode Finish")
            # self.printTree(self.root)

            # 부모노드도 분할 해야하는지 확인
            self.divideNode(parentNode, parentNode.childIdx)

    def divideNodeAfterRearrange(self, node, idx):

        if (len(node.key) >= self.order ):
            # 위로 올릴 key, value
            pushIdx = len(node.key) // 2
            pushKey = node.key[pushIdx]
            pushValue = node.value[pushIdx]


            # 오른쪽에 붙일 새로운 child
            newChildNode = Node(node.isLeaf)

            # 새로운 child 와  key, value  분할
            newChildNode.key = node.key[pushIdx+1:]
            node.key = node.key[:pushIdx]
            newChildNode.value = node.value[pushIdx+1:]
            node.value = node.value[:pushIdx]

            # 새로운 child 는 기존 node 의 childIdx+1 번째 자식인된다
            newChildNode.childIdx = node.childIdx + 1

            # 루트를 분할해야할 경우 해당 부모가 root 가 된다
            if(self.root.key == node.key):
                newRootNode = Node(False)
                self.root = newRootNode
                self.root.child.append(node)
                node.parent = self.root
                # idx += 1
            newChildNode.parent = node.parent

            # 부모노드에 key, value insert
            parentNode = node.parent
            parentNode.key.insert(idx, pushKey)
            parentNode.value.insert(idx, pushValue)

            # leaf 노드가 아니면 그 아래 자식들도 이동
            if node.isLeaf == False:
                newChildNode.child = node.child[pushIdx+1:]
                for i in range(pushIdx+1, len(node.child)): # 새로운 부모 지정
                    node.child[i].parent = newChildNode
                    node.child[i].childIdx = i - (pushIdx+1)
                node.child = node.child[:pushIdx+1]

            # 부모노드에 새 child insert
            parentNode.child.insert(idx+1, newChildNode)

            # newChildNode 오른쪽으로 기존에 있던 자식들 childIdx update
            for i in range(newChildNode.childIdx+1, len(parentNode.child)):
                parentNode.child[i].childIdx = i

            # 부모노드도 분할 해야하는지 확인
            self.divideNode(parentNode, parentNode.childIdx)
        else:
            if(node != self.root):
                self.divideNode(node.parent, node.parent.childIdx)

    def searchLeaf(self, node):
        if(len(node.child)>0):
            for i in range(0, len(node.child)):
                self.searchLeaf(node.child[i])
                return
        elif node.isLeaf == True:
            print("CHECK")
            self.divideNodeAfterRearrange(node, node.childIdx)

    def searchInsertNode(self, key, value, node, prevNode, keyIdx, childIdx):

        currNode = node  # 현재 순회하고 있는 노드
        i = keyIdx  # 순회해야할 key idx
        ci = childIdx # 내가 몇번쨰 자식인지 idx

        while (i <= self.maxKey):
            if currNode.key[i] < key and i == len(currNode.key) - 1 and currNode.isLeaf == False:  # 찾으려는 key 값이 더 크고 끝자락일 경우 (내려갈게있음)
                self.searchInsertNode(key, value, currNode.child[i + 1], currNode, 0, i+1)
            elif currNode.key[i] < key and i < len(currNode.key) - 1 and currNode.isLeaf == False:  # 찾으려는 key 값이 더 크고 끝자락이 아닐 경우 (오른쪽으로갈게있음)
                self.searchInsertNode(key, value, currNode, currNode, i + 1, i)
            elif currNode.key[i] > key and currNode.isLeaf == False:  # 찾으려는 key 값이 더 작을 경우 (내려갈게있음)
                self.searchInsertNode(key, value, currNode.child[i], currNode,  0, i)
            elif currNode.key[i] < key and i < len(currNode.key) - 1 and currNode.isLeaf == True:  # 찾으려는 key 값이 더 크고 끝자락이 아닐 경우 (오른쪽으로갈게있음)
                self.searchInsertNode(key, value, currNode, prevNode, i + 1, i)
            elif currNode.key[i] > key and currNode.isLeaf == True: # leaf 노드이고 좌측에 insert  해야하는 경우
                if (i-1 == -1):
                    currNode.key.insert(0, key)
                    currNode.value.insert(0, value)
                else:
                    currNode.key.insert(i, key)
                    currNode.value.insert(i, value)
                currNode.parent = prevNode
                self.divideNode(currNode, currNode.childIdx)


            elif currNode.key[i] < key and currNode.isLeaf == True: # leaf 노드이고 우측에 insert 해야하는 경우
                currNode.key.insert(i+1, key)
                currNode.value.insert(i+1, value)

                currNode.parent = prevNode
                self.divideNode(currNode, currNode.childIdx)

            elif currNode.key[i] == key:  # 찾으려는 키값의 경우
                print("KEY:",currNode.key[i]," ALREADY EXISTS!")
            else:
                print("NOT FOUND")

            return

    def insert(self, key, value):
        # 루트노드의 키값이 없으면 insert
        if (len(self.root.key) == 0 and self.root.isLeaf == True):
            self.root.key.append(key)
            self.root.value.append(value)
        else:
            # 삽입이 필요한 leaf 노드 Search & Insert
            self.searchInsertNode(key, value, self.root, None, 0,0)

    def printTree(self, x, level=0):
        print("[Level]", level, "[Key Length]", len(x.key), "[MAXKEY OVER]",len(x.key) > self.maxKeys, "[isLeaf]", x.isLeaf, "[Child Length]", len(x.child), "[Child Idx]", x.childIdx)
        if(level != 0):
            print( "[PARENT KEY]", x.parent.key, end=">>")
        else:
            print(end=">>")
        for i in (x.key):
            self.count += 1
            print(format(i,','), end=" ")
        print()
        level += 1
        if len(x.child) > 0:
            for i in x.child:
                self.printTree(i, level)

    def borrowKeySibiling(self, parent, siblingIdx):

        didBorrow = False

        if(siblingIdx > 0): # 현재 노드의 인덱스가 0 보다 크면 왼쪽에 sibling 이 있다는 의미
            leftSibling = parent.child[siblingIdx-1]
            if(len(leftSibling.key) > self.minKeys):
                # print("borrow from left sibling")
                borrowKey = leftSibling.key[len(leftSibling.key)-1]
                borrowValue = leftSibling.value[len(leftSibling.value)-1]

                # 왼쪽 sibling 한테 빌릴 key, value 삭제
                leftSibling.key.pop(len(leftSibling.key)-1)
                leftSibling.value.pop(len(leftSibling.value)-1)

                # 부모 key, value  저장
                parentKey = parent.key[siblingIdx-1]
                parentValue = parent.value[siblingIdx-1]

                # 왼쪽 sibling 한테 빌린 key, value 부모에 저장
                parent.key[siblingIdx-1] = borrowKey
                parent.value[siblingIdx-1]= borrowValue

                # 현재 노드의 삭제해야하는 키 자리에 parentKey, parentValue 로 replace
                if (parent.child[siblingIdx].key == []):
                    parent.child[siblingIdx].key.append(parentKey)
                    parent.child[siblingIdx].value.append(parentValue)
                else:
                    parent.child[siblingIdx].key.insert(0, parentKey)
                    parent.child[siblingIdx].value.insert(0, parentValue)
                didBorrow = True

        if(siblingIdx < len(parent.child)-1 and didBorrow == False): # 현재 노드 인덱스가 전체 자식개수-1 보다 작으면 오른쪽에 sibling 존재
            rightSibling = parent.child[siblingIdx+1]
            if(len(rightSibling.key) > self.minKeys):

                borrowKey = rightSibling.key[0]
                borrowValue = rightSibling.value[0]

                # print("borrow from right sibling", siblingIdx)

                # 오른쪽 sibling 한테 빌릴 key, value 삭제
                rightSibling.key.pop(0)
                rightSibling.value.pop(0)

                # 부모 key, value  저장
                parentKey = parent.key[siblingIdx]
                parentValue = parent.value[siblingIdx]

                # 오른쪽 sibling 한테 빌린 key, value 부모에 저장
                parent.key[siblingIdx] = borrowKey
                parent.value[siblingIdx] = borrowValue

                # 현재 노드의 삭제한 키 자리에 parentKey, parentValue 로 replace
                if (parent.child[siblingIdx].key == []):
                    parent.child[siblingIdx].key.append(parentKey)
                    parent.child[siblingIdx].value.append(parentValue)
                else:
                    parent.child[siblingIdx].key.append(parentKey)
                    parent.child[siblingIdx].value.append(parentValue)

                didBorrow = True

        return didBorrow


    def combineSibling(self, parent, siblingIdx): # LEAF 일때만 진행 !!!
        # print("CASE3")
        didCombine = False

        # 왼쪽이랑 합칠지 오른쪽이랑 합칠지 결정
        if (siblingIdx > 0):  # 현재 노드의 인덱스가 0 보다 크면 왼쪽에 sibling 이 있다는 의미
            leftSibling = parent.child[siblingIdx - 1]
            # 왼쪽 노드를 합칠 수 있다면 (현재 왼쪽 노드 키 개수가 maxKeys보다 적고 가져와야할 부모 키 개수가 최소개수보다 많아야함)
            if(len(leftSibling.key) < self.maxKeys and len(parent.key) > self.minKeys):
                # print("combine with left Sibling")

                # 합칠 부모 key, value 저장
                parentKey = parent.key[siblingIdx-1]
                parentValue = parent.value[siblingIdx-1]

                # 합쳐야하는 부모 key, value 삭제
                parent.key.pop(siblingIdx-1)
                parent.value.pop(siblingIdx-1)

                # 왼쪽 sibling 에 부모 key, value 합치기
                leftSibling.key.append(parentKey)
                leftSibling.value.append(parentValue)

                didCombine = True

                # 만약 키를 삭제한 노드가 안비었다면 --> 최소키이기 때문에 sibling 에 부착하기 2021.12.27
                if (len(parent.child[siblingIdx].key) >= 0):
                    for i in range(0, len(parent.child[siblingIdx].key)):
                        leftSibling.key.append(parent.child[siblingIdx].key[i])
                        leftSibling.value.append(parent.child[siblingIdx].value[i])
                    parent.child.pop(siblingIdx)

        if (siblingIdx < len(parent.child) - 1 and didCombine == False):  # 현재 노드 인덱스가 전체 자식개수-1 보다 작으면 오른쪽에 sibling 존재
            rightSibling = parent.child[siblingIdx + 1]

            # (현재 오른쪽 노드 키 개수가 maxKeys보다 적고 가져와야할 부모 키 개수가 최소개수보다 많아야함)
            if (len(rightSibling.key) < self.maxKeys and len(parent.key) > self.minKeys):
                # print("combine with right Sibling")

                # 합칠 부모 key, value 저장
                parentKey = parent.key[siblingIdx]
                parentValue = parent.value[siblingIdx]

                # 합쳐야하는 부모 key, value 삭제
                parent.key.pop(siblingIdx)
                parent.value.pop(siblingIdx)

                # 오른쪽  sibling 에 부모 key, value 합치기
                rightSibling.key.insert(0,parentKey)
                rightSibling.value.insert(0,parentValue)

                didCombine = True

                # 만약 키를 삭제한 노드가 안비었다면 --> 최소키이기 때문에 sibling 에 부착하기 2021.12.27
                if(len(parent.child[siblingIdx].key) >= 0):
                    for i in range(0,len(parent.child[siblingIdx].key)):
                        rightSibling.key.insert(i,parent.child[siblingIdx].key[i])
                        rightSibling.value.insert(i, parent.child[siblingIdx].value[i])
                    parent.child.pop(siblingIdx)



        if(didCombine == True):
            # 키를 삭제한 노드가 빈 경우를 대비해 -> 그 노드를 삭제하고 & 오른쪽에 있던 childIdx 업데이트 해주기
            for i in range(0, len(parent.child)):
                parent.child[i].childIdx = i





        return didCombine



    def searchDeleteKey(self, key, node, idx):
        currNode = node # 현재 순회하고 있는 노드
        i = idx # 순회해야할 key idx

        while(i <= self.maxKey):
            if currNode.key[i] < key and i == len(currNode.key) -1 and currNode.isLeaf == False: # 찾으려는 key 값이 더 크고 끝자락일 경우
                self.searchDeleteKey(key, currNode.child[i+1],0)
            elif currNode.key[i] < key and i < len(currNode.key) -1: # 찾으려는 key 값이 더 크고 끝자락이 아닐 경우
                self.searchDeleteKey(key, currNode, i+1)
            elif currNode.key[i] < key and i == self.maxKey and currNode.isLeaf == False : # 찾으려는 key 값이 더 크고 끝자락에 닿았을 경우
                self.searchDeleteKey(key, currNode.child[i+1], 0)
            elif currNode.key[i] > key and currNode.isLeaf == False: # 찾으려는 key 값이 더 작을 경우
                self.searchDeleteKey(key, currNode.child[i], 0)
            elif currNode.key[i] == key: # 찾으려는 키값의 경우
                self.deleteKey(currNode, i)
            else:
                print("NOT FOUND")
            return

    def inorder_precessor(self, childNode, currNode, keyIdx):
        # 왼쪽 노드들 중 최대값 return
        if len(childNode.child) > 0:
            return self.inorder_precessor(childNode.child[len(childNode.child)-1], currNode, keyIdx)

        else:
            # 현재 삭제해야하는 노드나 자식의 키 개수가 최소 키보다 많아야 실행 가능
            # 키 삭제
            currNode.key.pop(keyIdx)
            currNode.value.pop(keyIdx)

            childIdx = len(childNode.key)-1
            # 리프노드의 key, value 저장
            tmpKey = childNode.key[childIdx]
            tmpValue = childNode.value[childIdx]

            # print(currNode.key)
            currNode.key.insert(keyIdx, tmpKey)
            currNode.value.insert(keyIdx, tmpValue)

            # 리프노드를 삭제한거나 마찬가지기 때문에 다시 deleteKey 함수 시작
            self.deleteKey(childNode, childIdx)


    def inorder_successor(self, childNode, currNode, keyIdx):
        # 오른쪽 노드들 중 최소값 return
        # print("CASE6")
        # didDelete = False

        if(len(childNode.child) > 0):
            self.inorder_successor(childNode.child[0], currNode, keyIdx)
        else:
            # 현재 삭제해야하는 노드나 자식의 키 개수가 최소 키보다 많아야 실행 가능
            # if (len(currNode.key) > self.minKeys or len(childNode.key) > self.minKeys):
            # 키 삭제
            currNode.key.pop(keyIdx)
            currNode.value.pop(keyIdx)

            # 리프노드의 key, value 저장
            tmpKey = childNode.key[0]
            tmpValue = childNode.value[0]

            currNode.key.insert(keyIdx, tmpKey)
            currNode.value.insert(keyIdx, tmpValue)

            # 리프노드를 삭제한거나 마찬가지기 때문에 다시 deleteKey 함수 시작
            self.deleteKey(childNode, 0)

    def combineChild(self, currNode):
        childList = currNode.child
        currKeyIdx = 0
        currMaxKey = len(currNode.key) -1

        for i in range(0, len(childList)):
            newNode = Node(childList[0].isLeaf)
            for j in range(i, len(childList[i].key)):
                if(currNode.key[currKeyIdx] > childList[i].key[j]):
                    newNode.key.insert(i, childList[i].key[j])
                    newNode.value.insert(i, childList[i].value[j])
                else:
                    break
            for j in range(0, len(childList[i].child)):
                childList[i].child[j].childIdx = (i*2)+j
                childList[i].child[j].parent = newNode
                newNode.child.append(childList[i].child[j])
        newNode.childIdx = childList[0].childIdx
        currNode.child = []
        currNode.child.append(newNode)
        return newNode

    def rebuildTree(self, parentNode, currNode, isLeaf):

        #############################################################################################
        # 자식노드 하나로 합치기
        #############################################################################################
        newChildNode = Node(False)
        if(isLeaf == False):
            childNode = currNode.child
            newChildNode = Node(childNode[0].isLeaf)

            for i in range(0, len(childNode)):

                for j in range(0, len(childNode[i].key)):
                    newChildNode.key.append(childNode[i].key[j])
                    newChildNode.value.append(childNode[i].value[j])
                for j in range(0, len(childNode[i].child)):
                    newChildNode.child.append(childNode[i].child[j])
                    childNode[i].child[j].parent = newChildNode
            for i in range(0, len(newChildNode.child)):
                newChildNode.child[i].childIdx = i


        #############################################################################################

        currIdx = currNode.childIdx

        if (currIdx < len(parentNode.child) - 1):
            # 부모 키 오른쪽 형재에 붙이기
            parentKey = parentNode.key[currIdx]
            parentValue = parentNode.value[currIdx]
            rightSibling = parentNode.child[currIdx+1]
            rightSibling.key.insert(0, parentKey)
            rightSibling.value.insert(0, parentValue)

            # 새로운 자식노드 추가
            if (isLeaf == False):
                for i in range(0,len(rightSibling.child)):
                    rightSibling.child[i].childIdx = rightSibling.child[i].childIdx+1
                rightSibling.child.insert(0,newChildNode)
                newChildNode.parent = rightSibling

            # 삭제한 노드에 키가 최소키보다 작다면 2021.12.27 from here
            if(len(currNode.key) < self.minKeys):
                for i in range(0,len(currNode.key)):
                    # sibling 에 남은 key, value 다 이관 --> newChildNode 사이로 이관 2021.12.27(2)
                    if(isLeaf == False):
                        for j in range(0,len(newChildNode.key)):
                            if(newChildNode.key[j] > currNode.key[i]):
                                rightSibling.child[0].key.insert(j, currNode.key[i])
                                rightSibling.child[0].value.insert(j, currNode.value[i])
                                break
                    else:
                        rightSibling.key.insert(i, currNode.key[i])
                        rightSibling.value.insert(i, currNode.value[i])

                for i in range(0, len(currNode.key)):
                    currNode.key.pop(0)
                parentNode.child.pop(currIdx)

            # 부모 키 삭제
            parentNode.key.pop(currIdx)
            parentNode.value.pop(currIdx)

            # sibling 들 childIdx 갱신
            for i in range(0, len(parentNode.child)):
                parentNode.child[i].childIdx = i

            if (len(rightSibling.key) > self.order - 1): #### 2021.12.29 주석처리
                self.divideNode(rightSibling, rightSibling.childIdx)

            # 부모노드가 루트노드였다면 rightSibling 이 새로운 루트노드
            if(parentNode == self.root and len(parentNode.key) == 0):
                self.root = rightSibling
                self.root.childIdx = 0

                # 다 끝나고나서 sibling에 붙인 child  > key 개수 +1 보다 자식수가 더 많으면 2021.12.29
                if(isLeaf == False):
                    if (len(newChildNode.key) + 1 < len(newChildNode.child)):
                        self.reArrangeChilds(newChildNode)


                    # newChildNode divide 필요한지 확인 2021.12.29
                    if (len(rightSibling.child[0].key) > self.maxKeys):
                        self.divideNode(rightSibling.child[0], rightSibling.child[0].childIdx)
                        return

                # 최대 key 수를 넘아갔다면 divdeNode 수행
                if (len(self.root.key) > self.order - 1):
                    self.divideNode(self.root, self.root.childIdx)


            else:
                if (isLeaf == False):
                    # 다 끝나고나서 sibling에 붙인 child  > key 개수 +1 보다 자식수가 더 많으면 2021.12.29
                    if (len(newChildNode.key) + 1 < len(newChildNode.child)):
                        self.reArrangeChilds(newChildNode)
                    if (len(newChildNode.key) > self.maxKeys):
                        self.divideNode(newChildNode, newChildNode.childIdx)
                        return

                # 다 끝나고나서 부모(루트제외)키 조차 최소키를 만족하지 못하면, 부모노드에 대해 다시한번 rebuildTree 실행
                if (len(parentNode.key) < self.minKeys and parentNode != self.root):
                    self.rebuildTree(parentNode.parent, parentNode, False)
                if (len(parentNode.key) > self.order -1):
                    self.divideNode(parentNode, parentNode.childIdx)
                    return

        elif(currIdx > 0):
            # 부모키 왼쪽 형재에 붙이기
            parentKey = parentNode.key[currIdx-1]
            parentValue = parentNode.value[currIdx-1]
            leftSibling = parentNode.child[currIdx-1]
            leftSibling.key.append(parentKey)
            leftSibling.value.append(parentValue)


            # 새로운 자식노드 추가
            if (isLeaf == False):
                newChildNode.childIdx = len(leftSibling.child)
                leftSibling.child.append(newChildNode)
                newChildNode.parent = leftSibling

            # 삭제한 노드에 키가 최소키보다 작다면 2021.12.27
            if (len(currNode.key) < self.minKeys):
                for i in range(0, len(currNode.key)):
                    # sibling 에 남은 key, value 다 이관 --> 2021.12.27(2) newChildNode 가운데로 이관

                    if(isLeaf == False):
                        for j in range(0,len(newChildNode.key)):
                            if(newChildNode.key[j] > currNode.key[i]):
                                leftSibling.child[-1].key.insert(j, currNode.key[i])
                                leftSibling.child[-1].value.insert(j, currNode.value[i])
                                break
                    else:
                        leftSibling.key.append(currNode.key[i])
                        leftSibling.value.append(currNode.value[i])

                for i in range(0, len(currNode.key)):
                    currNode.key.pop(0)
                parentNode.child.pop(currIdx)

            # 부모 키 삭제
            parentNode.key.pop(currIdx - 1)
            parentNode.value.pop(currIdx - 1)

            # sibling 들 childIdx 갱신
            for i in range(0, len(parentNode.child)):
                parentNode.child[i].childIdx = i

            if (len(leftSibling.key) > self.order - 1): ##2021.12.29 주석처리
                self.divideNode(leftSibling, leftSibling.childIdx)

            # 부모노드가 루트노드였다면 leftSibling 이 새로운 루트노드
            if(parentNode == self.root and len(parentNode.key) == 0):
                self.root = leftSibling
                self.root.childIdx = 0

                # 다 끝나고나서 sibling에 붙인 child  > key 개수 +1 보다 자식수가 더 많으면 2021.12.29
                if(isLeaf == False):
                    if (len(newChildNode.key) + 1 < len(newChildNode.child)):
                        self.reArrangeChilds(newChildNode)


                    # newChildNode divide 필요한지 확인 2021.12.29
                    if(len(leftSibling.child[-1].key) > self.maxKeys):
                        self.divideNode(leftSibling.child[-1], leftSibling.child[-1].childIdx)
                        return

                # 최대 key 수를 넘아갔다면 divdeNode 수행
                if (len(self.root.key) > self.order - 1):
                    self.divideNode(self.root, self.root.childIdx)
            else:
                if (isLeaf == False):
                    # 다 끝나고나서 sibling에 붙인 child  > key 개수 +1 보다 자식수가 더 많으면 2021.12.29
                    if (len(newChildNode.key) + 1 < len(newChildNode.child)):
                        self.reArrangeChilds(newChildNode)
                    if (len(newChildNode.key) > self.maxKeys):
                        self.divideNode(newChildNode, newChildNode.childIdx)
                        return

                # 다 끝나고나서 부모키 조차 최소키를 만족하지 못하면, 부모노드에 대해 다시한번 rebuildTree 실행
                if (len(parentNode.key) < self.minKeys and parentNode != self.root):
                    self.rebuildTree(parentNode.parent, parentNode, False)

                if (len(parentNode.key) > self.order -1):
                    self.divideNode(self.root, parentNode.childIdx)
                    return

        # 다 끝나고나서 sibling에 붙인 child  > key 개수 +1 보다 자식수가 더 많으면 2021.12.27
        if (len(newChildNode.key) + 1 < len(newChildNode.child) and isLeaf == False):
            self.reArrangeChilds(newChildNode)
        # newChildNode 키 개수가 최대키 개수를 넘으면 2021.12.27(2)
        if(len(newChildNode.key) > self.maxKeys):
            self.divideNode(newChildNode, newChildNode.childIdx)
            return

        return

    def reArrangeChilds(self, node):

        if(node.isLeaf == False):
            # 자식의 수가 키 수보다 많을 경우
            if(len(node.key) + 1 < len(node.child)):
                isLeafParam = node.child[0].isLeaf
                nodeKey = []
                nodeChildKey = []
                nodeChildValue = []

                for i in range(0,len(node.key)):
                    nodeKey.append(node.key[i])

                for i in range(0,len(node.child)):
                    for j in range(0,len(node.child[i].key)):
                        nodeChildKey.append(node.child[i].key[j])
                        nodeChildValue.append(node.child[i].value[j])

                idx = 0
                tmpChildList = node.child
                originLength = len(tmpChildList)

                for i in range(0,len(nodeKey)):
                    # 자식노드 재생성 위한 temp 노드
                    tmpNode = Node(isLeafParam)
                    for j in range(idx, originLength):
                        if(nodeKey[i] > node.child[j].key[0]): # 첫번째 원소만 검사

                            for k in range(0, len(node.child[j].key)):
                                tmpNode.key.append(node.child[j].key[k])
                                tmpNode.value.append(node.child[j].value[k])
                            for k in range(0,len(node.child[j].child)):
                                tmpNode.child.append(node.child[j].child[k])
                            idx += 1
                        else:
                            tmpNode.childIdx = i
                            tmpNode.parent = node
                            node.child.append(tmpNode)

                            break

                # 맨끝child
                tmpNode = Node(isLeafParam)
                for i in range(0,len(node.child[idx].key)):
                    tmpNode.key.append(node.child[idx].key[i])
                    tmpNode.value.append(node.child[idx].value[i])

                for k in range(0, len(node.child[j].child)):
                    tmpNode.child.append(node.child[idx].child[k])

                tmpNode.childIdx = len(node.child)
                tmpNode.parent = node
                node.child.append(tmpNode)

                # 기존 child 날리기
                for i in range(0, originLength):
                    node.child.pop(0)

                # childIdx 재점검
                for j in range(0, len(node.child)):
                    node.child[j].childIdx = j
                    node.child[j].parent = node

                for i in range(0, len(node.child)):
                    for j in range(0, len(node.child[i].child)):
                        node.child[i].child[j].parent = node.child[i]
                        node.child[i].child[j].childIdx = j

                for i in range(0, len(node.child)):
                    if(len(node.child[i].key) +1 < len(node.child[i].child)):
                        self.reArrangeChilds(node.child[i])

                        if (len(node.child[i].key) > self.maxKeys):
                            self.divideNode(node.child[i], node.child[i].childIdx)
                            return
                        return


                for i in range(0, len(node.child)):
                    if(len(node.child[i].key) > self.maxKeys):
                        self.divideNode(node.child[i],node.child[i].childIdx)
                        return
                # # 2021.12.29 (2)
                if(len(node.key) >  self.maxKeys):
                    self.divideNode(node, node.childIdx)
                    return




        else:
            if(len(node.key) > self.order-1):
                self.divideNode(node, node.childIdx)


    def reArrangeChilds2(self, node): # 자식의 수가 키 수보다 많을 경우 다시 자식분배

        if(node.isLeaf == False):
            # 자식의 수가 키 수보다 많을 경우
            if(len(node.key) + 1 < len(node.child)):

                # 자식노드 재생성 위한 temp 노드
                tmpNode = Node(node.child[0].isLeaf)
                # 이 'sz' index 를 기점으로 key, value 분배
                sz = ceil(len(node.key) / 2)
                for j in range(0, len(node.child[sz].key)):
                    tmpNode.key.append(node.child[sz].key[j])
                    tmpNode.value.append(node.child[sz].value[j])
                for j in range(0, len(node.child[sz+1].key)):
                    tmpNode.key.append(node.child[sz+1].key[j])
                    tmpNode.value.append(node.child[sz + 1].value[j])

                tmpNode.parent = node
                tmpNode.childIdx = sz

                # 이 'sz' index 를 기점으로 child 도 다시 append
                for j in range(0, len(node.child[sz].child)):
                    tmpNode.child.append(node.child[sz].child[j])
                for j in range(0, len(node.child[sz+1].child)):
                    tmpNode.child.append(node.child[sz+1].child[j])

                node.child.insert(sz, tmpNode)
                # 합친 child 들 삭제
                node.child.pop(sz+1)
                node.child.pop(sz+1)

                for j in range(0, len(node.child)):
                    node.child[j].childIdx = j
                    node.child[j].parent = node
                self.reArrangeChilds(node.child[sz]) # node 2021.12.27

                ## ????
                if (len(node.key) > self.order - 1):
                    self.divideNode(node, node.childIdx)

        else:
            if(len(node.key) > self.order-1):
                self.divideNode(node, node.childIdx)


    def deleteKey(self, deleteNode, deleteKeyIdx):

        didExecute = False

        # CASE 1 리프노드인지 확인
        if(deleteNode.isLeaf == True):
            # 키 삭제
            deleteNode.key.pop(deleteKeyIdx)
            deleteNode.value.pop(deleteKeyIdx)


            # 삭제한 노드의 키 개수가 최소 키 개수를 위반하는지 확인 (루트는 검사할필요 없음)
            if(len(deleteNode.key) < self.minKeys and deleteNode != self.root):

                # 형재 노드로부터 키 빌리기
                didExecute = self.borrowKeySibiling(deleteNode.parent, deleteNode.childIdx)

                # 형재 노드로부터 키를 빌려오지 못했다면 병합
                if(didExecute == False):
                    didExecute = self.combineSibling(deleteNode.parent, deleteNode.childIdx)

                    if(didExecute == False):
                        self.rebuildTree(deleteNode.parent, deleteNode, True)


        # CASE 2 internal 노드
        else:
            # print("----- INTERNAL NODE -----")
            if(len(deleteNode.key) > self.minKeys or len(deleteNode.child[deleteKeyIdx].key) > self.minKeys):
                self.inorder_precessor(deleteNode.child[deleteKeyIdx], deleteNode, deleteKeyIdx)
            elif(len(deleteNode.key) > self.minKeys or len(deleteNode.child[deleteKeyIdx+1].key) > self.minKeys):
                self.inorder_successor(deleteNode.child[deleteKeyIdx+1], deleteNode, deleteKeyIdx)
            else:
                # 키 삭제
                # print("ELSE")
                deleteNode.key.pop(deleteKeyIdx)
                deleteNode.value.pop(deleteKeyIdx)

                if(deleteNode == self.root and len(deleteNode.key) == 0):
                    # print("----- ROOT IS ERASED -----")
                    # 루트노드가 지워졌을 경우 왼쪽 자식과 오른쪽자식을 병합 후
                    childNode = deleteNode.child
                    newChildNode = Node(childNode[0].isLeaf)

                    for i in range(0, len(childNode)):
                        for j in range(0, len(childNode[i].key)):
                            newChildNode.key.append(childNode[i].key[j])
                            newChildNode.value.append(childNode[i].value[j])
                        for j in range(0, len(childNode[i].child)):
                            newChildNode.child.append(childNode[i].child[j])
                            childNode[i].child[j].parent = newChildNode
                    for i in range(0, len(newChildNode.child)):
                        newChildNode.child[i].childIdx = i

                    self.root = newChildNode
                    # 자식들 재배치
                    self.reArrangeChilds(self.root)

                    for k in range(0, len(newChildNode.child)):
                        if len(newChildNode.child[k].key) > self.order-1:
                            self.divideNode(newChildNode.child[k], newChildNode.child[k].childIdx)
                            break
                else:
                    self.rebuildTree(deleteNode.parent, deleteNode, False)


    def delete(self, key):
        # print('DELETE KEY:',key)
        self.searchDeleteKey(key, self.root, 0)



if __name__ == '__main__':

    isTrue = True # compare 연산이 잘 끝났는지 확인

    tree = Tree()

    while True:
        print("----------------------------------")
        executeInput = int(input('Q: 실행할 연산을 입력해주세요 (1.insertion 2.deletion 3.quit)'))
        print("----------------------------------")
        print()

        if executeInput == 3:
            print("----------------------------------")
            print("BYE")
            print("----------------------------------")
            break


        if executeInput == 1: # INSERT
            tree = Tree() # init
            print("----------------------------------")
            fileName = input('Q: INSERT할 파일명을 입력해주세요.')
            print("----------------------------------")

            file = open('data/'+fileName+'.csv', 'r', encoding='utf-8')
            data = csv.reader(file)
            readData = csv.reader(file)

            key = []
            value = []
            searchValue = []

            for idx, line in enumerate(data):
                key.append(int(line[0].split('\t')[0]))
                value.append(int(line[0].split('\t')[1]))

            file.close()
            print()
            print("----------------------------------")
            print("---------- INSERT START ----------")
            print("----------------------------------")
            for i in range(0,len(key)):
                tree.insert(key[i], value[i])
            print()
            print("----------------------------------")
            print("---------- SEARCH START ----------")
            print("----------------------------------")
            # returnValue 초기화
            tree.returnValue = []

            for i in range(0, len(key)):
                    tree.searchKey(key[i], tree.root, 0)
            writeFile = open('data/'+fileName+'Result.csv','w', newline="",encoding='utf-8')
            writer = csv.writer(writeFile)
            writer.writerows(tree.returnValue)

            writeFile.close()
            print()
            print("----------------------------------")
            print("---------- COMPARE START ----------")
            print("----------------------------------")
            for i in range(0,len(tree.returnValue)):
                 if(int(tree.returnValue[i][0].split()[1]) != int(value[i])):
                    print("DIFFERENT!", i, '-',value[i],'-',tree.returnValue[i][0].split()[1])
                    isTrue = False
                    break
            if(isTrue):
                print("COMPARE DONE!")
                print()

        elif executeInput == 2: # DELETE
            # print(tree.root.key,'here')
            if(tree.root.key == []):
                print("INSERT 먼저 진행해주세요.")
            else:
                print("----------------------------------")
                fileName = input('Q: DELETE할 파일명을 입력해주세요.')
                print("----------------------------------")

                print()
                print("----------------------------------")
                compareFileName = input('Q: DELETE 후 비교할 파일명을 입력해주세요.')
                print("----------------------------------")

                deleteFile = open('data/' + fileName + '.csv', 'r', encoding='utf-8')
                deleteData = csv.reader(deleteFile)

                deleteKey = []
                deleteValue = []
                searchValue = []

                for idx, line in enumerate(deleteData):
                    deleteKey.append(int(line[0].split('\t')[0]))
                    deleteValue.append(int(line[0].split('\t')[1]))

                deleteFile.close()

                print()
                print("----------------------------------")
                print("---------- DELETE START ----------")
                print("----------------------------------")
                for i in range(0,len(deleteKey)):
                    tree.delete(deleteKey[i])

                print()
                print("----------------------------------")
                print("---------- SEARCH START ----------")
                print("----------------------------------")
                # returnValue 초기화
                tree.returnValue = []

                compareFile = open('data/' + compareFileName + '.csv', 'r', encoding='utf-8')
                compareData = csv.reader(compareFile)

                compareKey = []
                compareValue = []
                searchValue = []

                for idx, line in enumerate(compareData):
                    compareKey.append(int(line[0].split('\t')[0]))
                    compareValue.append(line[0].split('\t')[1])

                compareFile.close()

                for i in range(0, len(compareKey)):
                    # print("SEARCH:",compareKey[i])
                    tree.searchKey(compareKey[i], tree.root, 0)

                writeFile = open('data/' + fileName + 'Result.csv', 'w', newline="", encoding='utf-8')
                writer = csv.writer(writeFile)
                writer.writerows(tree.returnValue)

                writeFile.close()
                # print("RETURN VALUE:", len(tree.returnValue))

                print()
                print("----------------------------------")
                print("---------- COMPARE START ----------")
                print("----------------------------------")
                for i in range(0, len(tree.returnValue)):
                    if (str(tree.returnValue[i][0].split()[1]) != str(compareValue[i])):
                        print("DIFFERENT!", i, '-', compareValue[i], '-', tree.returnValue[i][0].split()[1])
                        isTrue = False

                if (isTrue):
                    print("COMPARE DONE!")
                    print()

                tree.root.key = []
