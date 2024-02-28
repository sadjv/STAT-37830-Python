# Answers

Put any answers to questions in the assignment in this file, or any commentary you don't include in the code.

This is a markdown file (the `.md` extension gives it away). If you have never used markdown before, check out [this short guide](https://guides.github.com/features/mastering-markdown/).

## Problem 0

# Part A

For the S[i,j] entry of the given numpy array, we compute k by k=n*i+j and get s[k]=S[k], where S is an m*n matrix and s is a vector with dim(s)=mn.

For the s[k] entry of the given numpy array, we compute i by i=k//n and j by j=k-i*n, where S[i,j]=s[k].

To turn the array s into a m*n numpy array, let A be an m*n empty array and let its row 0 be s[:n] and its i-th row by s[i*n+1, (i+1)*n+1], for i=1,2 ,..., m-1.

# Part B
I choose the diagonal sparse matrix, since the outputing matrices always only have 8 diagonals and are banded matrices.

# Part C
My running result for n=100 and n=1000 for 3 different sparse matrices is showing as follows:
![Adjacent matrix running result](https://github.com/caam37830-2021/homework-3-sadjv/blob/main/C.png)

According to my running result, count_alive_neighbors_matmul is much faster than the count_alive_neighbors algorithm whether the sparse matrix type used. This is obvious, since in my code of count_alive_neighbors_matmul we use no for loop. 

# Part D
By my testing, slicing function is faster than the original count_alive_neighbors method, but slower than the matmul method.

# Running times for 3 different methods
I run the 3 methods of counting neighbors for n=100 and n=500. The result shows as follows:
![Time for counting neighbors](https://github.com/caam37830-2021/homework-3-sadjv/blob/main/CD.png)

# Part E
![Game of life](https://github.com/caam37830-2021/homework-3-sadjv/blob/main/life.gif)



 
## Feedback
