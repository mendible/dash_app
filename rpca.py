'''
Module containing RPCA code.
'''

import math
import numpy as np
import scipy.sparse.linalg

def rpca(image_mat, lambda_scale):
    """
    Performs Robust Principle Component Analysis on image_mat.
    :returns: Low-rank, sparse parts of image_mat
    """

    if len(image_mat.shape) == 3:
        shape_flag = 1
        x_size, y_size, t_size = image_mat.shape
        image_mat = np.reshape(image_mat, (x_size*y_size, t_size))

    space_dim = image_mat.shape[0]
    lam = lambda_scale*1 / math.sqrt(space_dim)
    tol = 1e-7
    max_iter = 40
    norm_two = np.linalg.norm(image_mat, 2)
    norm_inf = np.linalg.norm(image_mat.flatten(), np.inf) / lam
    norm_fro = np.linalg.norm(image_mat, 'fro')
    dual_norm = max(norm_two, norm_inf)
    normalized_data = image_mat / dual_norm

    a_hat = np.empty(image_mat.shape)
    e_hat = np.empty(image_mat.shape)
    mu_ = 1.25 / norm_two
    mu_bar = mu_ * 1e7
    rho = 1.5

    for _ in range(max_iter):
        temp = image_mat - a_hat + 1 / mu_ * normalized_data
        e_hat = (np.maximum(temp - lam / mu_, 0) +
                 np.minimum(temp + lam / mu_, 0))

        u_mat, sigma, vt_mat = (scipy.sparse.linalg.svds(
            np.asarray(image_mat - e_hat + 1 / mu_ * normalized_data),
            min(6, image_mat.shape[1]-2)))
        svp = (sigma > 1 / mu_).sum()

        a_hat = (u_mat[:, -svp:].dot(np.diag(sigma[-svp:] - 1 / mu_)).dot(
            vt_mat[-svp:, :]))

        residual = image_mat - a_hat - e_hat
        normalized_data += mu_ * residual
        mu_ = min(mu_ * rho, mu_bar)

        if (np.linalg.norm(residual, 'fro') / norm_fro) < tol:
            break

    if shape_flag:
        a_hat = np.reshape(a_hat, (x_size, y_size, t_size))
        e_hat = np.reshape(e_hat, (x_size, y_size, t_size))

    return a_hat, e_hat
