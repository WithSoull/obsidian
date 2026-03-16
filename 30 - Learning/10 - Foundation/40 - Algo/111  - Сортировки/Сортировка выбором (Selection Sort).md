[[30 - Learning/10 - Foundation/40 - Algo/Нотация О-большое| Алгоритмическая сложность]]: $O(n ^ 2)$

Для сортировки по неубыванию (возрастанию) мы находим самый маленький элемент в списке и записываем его в другой, при этом этот элемент из первого списка мы удаляем.

- Python
    
    ```python
    def findSmallest(arr):
        smallest = arr[0]
        smallest_index = 0
    
        for i in range(1, len(arr)):
            if arr[i] < smallest:
                smallest = arr[i]
                smallest_index = i
    
        return (smallest, smallest_index)
    
    def selectionSort(arr):
        sortedArr = []
        for i in range(len(arr)):
            smallest, smallest_index = findSmallest(arr)
            sortedArr.append(smallest)
            arr.pop(smallest_index)
    
        return sortedArr
    ```