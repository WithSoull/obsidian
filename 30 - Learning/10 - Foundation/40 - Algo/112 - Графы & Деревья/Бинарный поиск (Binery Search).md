### [[30 - Learning/10 - Foundation/40 - Algo/Нотация О-большое| Алгоритмическая сложность]]: $O(log (n))$

> Бинарный поиск работает в отсортированном массиве данных. Он позволяет найти число, которое загадал человек, задавая минимальное количество вопросов с ответами "Да" и "Нет" (например, вопрос "Число n больше загаданного тобой?"). Алгоритм бинарного поиска основан на постоянном сужении границ поиска в зависимости от полученного ответа.

# Реализация
- С++
    ```cpp
    #include <iostream>
    #include <vector>
    
    int binarySearch(std::vector<int>& arr, int target) {
        int left = 0;
        int right = arr.size() - 1;
    
        while (left <= right) {
            int mid = left + (right - left) / 2;
    
            if (arr[mid] == target) {
                return mid;
            }
            else if (arr[mid] < target) {
                left = mid + 1;
            }
            else {
                right = mid - 1;
            }
        }
    
        return -1;
    }
    
    int main() {
        std::vector<int> arr = {1, 3, 5, 7, 9};
        int target = 5;
    
        int result = binarySearch(arr, target);
        if (result != -1) {
            std::cout << "Element found at index " << result << std::endl;
        }
        else {
            std::cout << "Element not found" << std::endl;
        }
    
        return 0;
    }
    
    ```
    
- Python
    ```python
    def binary_search(list, target):
        left = 0
        right = len(list) - 1
        while left <= right:
            mid = (left + right) // 2
            guess = list[mid]
            if guess == target:
                return mid
            elif guess > target:
                right = mid - 1
            else:
                left = mid + 1
    
        return -1
    
    my_list = [1, 2, 4, 7, 8, 9, 11, 15]
    
    print(binary_search(my_list, 1))
    print(binary_search(my_list, 11))
    	
    ```


