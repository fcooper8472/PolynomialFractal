# PolynomialFractal

![](images/logo.png)

## Background

This repository contains a python script for visualising an interesting mathematical object.

Consider a degree $n$ polynomial

$$\sum_{k=0}^n\left(a_k\;x^k\right),$$

where $a_k\;\in\;\{-1,1\}$.  Let us call such a polynomial

$$P_n^{\{\pm1\}}.$$

There are $n+1$ coefficients in $P_n^{\{\pm1\}}$, each of which can take the value $-1$ or $1$, and we are interested in the roots of *all* such polynomials.
For a fixed $n$ there are $2^{n+1}/2 = 2^n$ possible unique polynomials $P_n^{\{\pm1\}}$, each of which has $n$ roots.

Here, we calculate all of the roots of every possible $P_n^{\{\pm1\}}$, up to some fixed $n$, and plot a heat map of the locations of those roots on the complex plane.

This object requires the calculation of $\sum_{k=0}^n\left(n\;2^n\right) = 2 + 2^{n+1}(n-1)$ roots.
Not only does this number scale very poorly with $n$, but as $n$ increases the cost of calculating polynomial roots increases (roughly) as $n^3$.
This puts a fairly low bound on a maximum value of $n$, of around $n=22$ on a modest laptop, or up to $n=24$ on a bigger machine.

## Usage
The script `polynomial_fractal.py` produces a PNG image in the script directory entitled `PolynomialFractal.png` and, along the way, caches all polynomial roots for each degree up to the chosen maximum degree.

In addition, the binned values will be cached based on the number of bins requested, the radius around $0$ in the complex plane that is being binned, and the maximum degree of $P_n^{\{\pm1\}}$ that has been calculated.

## Parameters

There are 4 parameters that can be changed at the top of the script:

1. `max_deg`: the maximum polynomial degree. Don't set above 20 unless you're willing to wait!
1. `num_bins`: the number of bins in x and y, which directly relates to the resolution of the output image.
1. `radius`: the radius about 0 in the complex plane that is binned. A radius >= 2 will guarantee all roots are in the image.
1. `percentile`: the percentile above which bin values are clipped, improving the dynamic range of the image.

## Sample images

`images/PolynomialFractal4k.png` and `images/PolynomialFractal8k.png` are 4k and 8k images produced with this script, using `max_deg=23`, `radius=2.0`, `percentil=98`, and `num_bins=2800` and `5600`, respectively.
