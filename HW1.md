# Answers

Put any answers to questions in the assignment in this file, or any commentary you don't include in the code.

This is a markdown file (the `.md` extension gives it away). If you have never used markdown before, check out [this short guide](https://guides.github.com/features/mastering-markdown/).

## Problem 0

Part B
The graph is showing as follows:

![Solving Ax=b: Cholesky vs LU](https://github.com/caam37830-2021/homework-2-sadjv/blob/main/problem%200%20b.png)

In practice, the Cholesky factorization is faster.

Part C
This algorithm should be faster than the approach we used in homework 0. SInce we only need to perform vector multiplication n times instead of doing matrix multiplication n times. The complexity should be O(n) for this algorithm, which is not reachable for general matrix multiplication. For Fibonacci computation, the overflow problem should be minded.


## Problem 1

Part A
The graph is showing as follows:

![Matrix mul with 3 for loop](https://github.com/caam37830-2021/homework-2-sadjv/blob/main/problem%201%20a.png)

The computer have several levels of caches that is much faster than the main memory. If we keep accessing memory cache for values, we can have a better performance. Some of the matmul_*** function achieve this and the others keep losing cache. The fastest function is matmul_ikj and the slowest one is matmul_kji. Notice that the matrix is stored in row-major order. Let's look at the innermost for loop for both function. For matmul_kji, in each iteration of the loop we need to change the value of i, which leads to skip over an entire row of the matrix and jumping much further into memory. This may far past the values of the cached memory. Therefore, we will loss around 2 caches when loading the value of A[i, j], B[i,k]. This make it the slowest. For the matmul_ikj, the inner most loop is changing the column number j, so we may not lose any caches in this function. This make the function the fastest.

Part B
The graph is showing as follows:

![Matrix mul with blocks](https://github.com/caam37830-2021/homework-2-sadjv/blob/main/problem%201%20b.png)

Part C

![Matrix mul with strassen](https://github.com/caam37830-2021/homework-2-sadjv/blob/main/problem%201%20c.png)



## Problem 2

(2). See the graph below:

![Markov chain](https://github.com/caam37830-2021/homework-2-sadjv/blob/main/problem%202.png)

(3). At t=1000, the 2-norm between eigenvector with largest eigenvalue and p is 0.19065277078978227.
At t=2000, the 2-norm between eigenvector with largest eigenvalue and p is 0.0038492383304298337

## Feedback
