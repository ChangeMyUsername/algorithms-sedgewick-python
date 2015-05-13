# def find_the_point(lst):
#     low, high = 0, len(lst) - 1
#     while low < high:
#         mid = (low + high) / 2
#         if lst[mid] < lst[mid + 1]:
#             low = mid + 1
#         elif lst[mid] > lst[mid + 1]:
#             high = mid
#     return lst[high]


# def reverse_binary_search(key, lst):
#     start, end = 0, len(lst) - 1
#     while start < end:
#         mid = (start + end) / 2
#         if lst[mid] < key:
#             end = mid - 1
#         elif lst[mid] > key:
#             start = mid + 1
#         else:
#             return mid
#     return -1


# print(find_the_point([1, 2, 3, 9, 8, 7, 6, 5, 4, -1]))
# print(reverse_binary_search(5, [9, 8, 7, 6, 5, 4, 3, 2, 1]))

# def find_right(key, start, end, lst):
#     while start <= end:
#         mid = (start + end) / 2
#         if lst[mid] < key:
#             end = mid - 1
#         elif lst[mid] > key:
#             start = mid + 1
#         else:
#             return mid
#     return -1

# print(find_right(7, 3, 9, [1, 2, 3, 9, 8, 7, 6, 5, 4, -1]))
