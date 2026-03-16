![[99 - Meta/02 - Медиа/Pasted image 20231126085658.png]]

Структура данных - в которой базовые операции(вставка, удаление, чтение) выполняется за $O(lg (n))$ в лучшем случае. Все зависит от высоты, на рисунке слева сбалансированное дерево, а справа - нет.

# Реализация BST на Python:
``` python
class BSTNode:  
    def __init__(self, val=0):  
        self.val = val  
        self.right = None  
        self.left = None  
        self.parent = None
```
# Алгоритмы 
## Центрированный (симметричный) обход дерева
``` python
def inorder_tree_walk(self, node):  
    if node is not None:  
        self.inorder_tree_walk(node.left)  
        print(node.val)  
        self.inorder_tree_walk(node.right)
```
## Поиск
``` python
def tree_search(root, val):  
    if root is None or root.val == val:  
        return root  
  
    if val < root.val:  
        return tree_search(root.left, val)  
    else:  
        return tree_search(root.right, val)
```
## Минимум и максимум
``` python
def tree_minumum(root):  
    if root is None:  
        return None  
    while root.left is not None:  
        root = root.left  
  
    return root  
  
def tree_maximum(root):  
    if root is None:  
        return None  
    while root.right is not None:  
        root = root.right  
  
    return root
```

## Вставка 
``` python
def tree_insert(root, node):  
    if node.val < root.val:  
        if root.left is None:  
            root.left = node  
        else:  
            tree_insert(root.left, node)  
    else:  
        if root.right is None:  
            root.right = node  
        else:  
            tree_insert(root.right, node)  
```
