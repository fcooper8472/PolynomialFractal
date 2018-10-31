import itertools
import matplotlib.pyplot as plt
import numpy as np


def get_roots_fname(_deg):
    return 'roots/degree_%s.npy' % str(_deg).zfill(2)


def get_bins_fname(_num_bins, _radius, _max_degree):
    return 'bins/%d_%.1f_%d.npy' % (_num_bins, _radius, _max_degree)


def calculate_roots(_deg):

    # Try loading the roots from file.  If they don't exist, create them.
    try:
        np.load(get_roots_fname(_deg), allow_pickle=False)
        print('Roots for degree %s already exist.' % str(_deg).rjust(2, ' '), flush=True)
    except IOError:
        # There are deg+1 coefficients in a degree deg polynomial.
        # Each coefficient can be +-1 (except the first, or we will double-count)
        # Therefore, 2^deg polynomials, each having deg roots
        print('Calculating roots for degree %s... ' % str(_deg).rjust(2, ' '), end='', flush=True)
        all_roots = np.empty((2**_deg, _deg), np.complex64)

        # itertools.product([1., -1.], repeat=_deg) gives all 2^deg coefficient lists for polynomials of degree deg-1.
        # We prepend [1.] to each of these to generate our 2^deg coefficient lists for unique degree deg polynomials.
        for i, x in enumerate(itertools.product([1., -1.], repeat=_deg)):
            all_roots[i] = np.roots([1.] + list(x))

        np.save(get_roots_fname(_deg), all_roots.flatten(), allow_pickle=False)
        print('done.', flush=True)


def bin_roots(_num_bins, _radius):

    # Determine the maximum degree available to us
    _deg = 1
    while True:
        try:
            np.load(get_roots_fname(_deg), allow_pickle=False)
            _deg += 1
        except IOError:
            break
    _max_deg = _deg - 1

    # Try loading the pre-binned data from file.  If it doesn't exist, create it.
    try:
        _bins = np.load(get_bins_fname(_num_bins, _radius, _max_deg), allow_pickle=False)
        print('Binning already complete for these parameters.', flush=True)
        return _bins
    except IOError:
        _bins = np.zeros((_num_bins, _num_bins), dtype=np.uint32)
        _bin_size = 2. * _radius / _num_bins

        for _deg in range(1, 1 + _max_deg):
            print('Binning roots for degree %s... ' % str(_deg).rjust(2, ' '), end='', flush=True)
            roots_this_deg = np.load(get_roots_fname(_deg), allow_pickle=False)

            # Find the correct bin
            imag_bins = np.floor((roots_this_deg.imag + _radius) / _bin_size).astype(np.uint16)
            real_bins = np.floor((roots_this_deg.real + _radius) / _bin_size).astype(np.uint16)

            # Account for possible boundary issues if radius was picked too small
            imag_bins[imag_bins > _num_bins - 1] = _num_bins - 1
            real_bins[real_bins > _num_bins - 1] = _num_bins - 1
            imag_bins[imag_bins < 0] = 0
            real_bins[real_bins < 0] = 0

            for x in zip(imag_bins, real_bins):
                _bins[x] += 1

            print('done.', flush=True)

        np.save(get_bins_fname(_num_bins, _radius, _max_deg), _bins, allow_pickle=False)
        return _bins


if __name__ == '__main__':

    max_deg = 23
    for deg in range(1, 1+max_deg):
        calculate_roots(deg)

    bins = bin_roots(5600, 2.0)

    threshold = np.percentile(bins[np.nonzero(bins)], 98)
    bins[bins > threshold] = threshold

    norm = plt.Normalize(0, threshold, clip=True)
    cmap = plt.get_cmap('inferno')
    image = cmap(norm(bins))

    plt.imsave('PolynomialFractal.png', image)
