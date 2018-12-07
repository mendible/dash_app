"""This file contains the helper RPCA function which calculate the rank and
sparsity of the outputs."""

import numpy as np

def get_rank(matrix, sigma):

    """This function returns the rank of the input matrix, D using its
    singular values D_sigma."""
    if not (matrix.ndim == 2):
        raise Exception('Input is not 2D. Check dimensions of imput matrix')
    elif not (sigma.ndim == 1):
        raise Exception('Input sigma is not 1D. Check dimensions of imput matrix')
    elif np.isnan(matrix).any():
        raise Exception('There are NaNs in the matrix')
    elif np.isnan(sigma).any():
        raise Exception('There are NaNs in the sigma values')
    dim_one, dim_two = matrix.shape
    beta = min(dim_one, dim_two)/max(dim_one, dim_two)
    win = (8*beta)/(beta + 1 + (beta**2 +14*beta + 1)**(1/2))
    tau = (2*(beta + 1) + win)**(1/2)
    ind = sigma > tau
    rank = ind.sum()
    if isinstance(rank, np.int64) is not True:
        raise Exception('Value returned is not of type int')

    return rank


def get_sparsity(matrix, tolerance=0.001):

    """This function returns the fraction of elements
    that are zero in D with the tolerance, tol."""

    if not (matrix.ndim == 2):
        raise Exception('Input is not 2D. Check dimensions of imput matrix')
    elif np.isnan(matrix).any():
        raise Exception('There are NaNs in your matrix')

    percent_sparse = int(np.round(100*(abs(matrix) < tolerance).sum()/matrix.size))

    if isinstance(percent_sparse, int) is not True:
        raise Exception('Value returned is not of type int')

    return percent_sparse

def magnitude(U,V):
    if not (U.shape == V.shape):
        raise Exception('The velocities must have the same shape')
    # test if the two are the same size
    mag = (U**2 + V**2)**(.5)
    return mag

def vorticity(U,V):
    if not (U.shape == V.shape):
        raise Exception('The velocities must have the same shape')
    m,n,k = V.shape
    vort = np.empty([m,n,k])
    for frames in range(k):
        # take derivative with respect to y axis (1)
        du_dy = np.gradient(U[:,:,frames], axis = 1)
        # take derivative with respect to x axis (0)
        dv_dx = np.gradient(V[:,:,frames], axis = 0)
        vort[:,:,frames] = dv_dx-du_dy
    return vort

def convert_lambda(slider_value):
    return 10**(slider_value-1)
