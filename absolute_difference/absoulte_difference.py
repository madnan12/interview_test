def findMinDiff(arr, n):
    diff = 10**20
    for i in range(n-1):
        for j in range(i+1,n):
            if abs(arr[i]-arr[j]) < diff:
                diff = abs(arr[i] - arr[j]) 
    return diff
 
arr = [1, 5, 3, 35, 45, 25]
n = len(arr)
print("Minimum difference is " + str(findMinDiff(arr, n)))