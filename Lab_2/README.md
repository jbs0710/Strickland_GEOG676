# Part 1 - Take the following list and multiply all list items together.

# To answer Part 1, I used the simple abbreviated assignment " *= "
# The for loop will then move through the list of values and multiple each until the end of the list

>
```python
part1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
result1 = 1

for a in part1:
    result1 *= a

print ("The answer to Part 1: ", result1)
```
# Part 2 - Take the following list and add all list items together.

# Just like in Part 1, I again used a simple abbreviated assignment " += "
# The for loop will then move through the list of values and add each until the end of the list


```python
part2 = [-1, 23, 483, 8573, -13847, -381569, 1652337, 718522177]
result2 = 0

for b in part2:
    result2 += b

print ("The answer to Part 2: ", result2)
```
# Part 3                                                                                                        

# isEven = num1 % 2 == 0                                                                                        

>
```python
part3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21]                                  
result3 = 0
                                                                                                                

for c in part3:                                                                                                 
    if c % 2 == 0:
       result3 += c                                                                                             
                                                                                                                
print("The answer to Part 3: ", result3)
```