# Copyright (c) 2020, Xilinx
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of FINN nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy as np

from finn.custom_op.multithreshold import multithreshold


def test_execute_multi_thresholding():

    inputs = np.ndarray(
        shape=(6, 3, 2, 2),
        buffer=np.array(
            [
                4.8,
                3.2,
                1.2,
                4.9,
                7.8,
                2.4,
                3.1,
                4.7,
                6.2,
                5.1,
                4.9,
                2.2,
                6.2,
                0.0,
                0.8,
                4.7,
                0.2,
                5.6,
                8.9,
                9.2,
                9.1,
                4.0,
                3.3,
                4.9,
                2.3,
                1.7,
                1.3,
                2.2,
                4.6,
                3.4,
                3.7,
                9.8,
                4.7,
                4.9,
                2.8,
                2.7,
                8.3,
                6.7,
                4.2,
                7.1,
                2.8,
                3.1,
                0.8,
                0.6,
                4.4,
                2.7,
                6.3,
                6.1,
                1.4,
                5.3,
                2.3,
                1.9,
                4.7,
                8.1,
                9.3,
                3.7,
                2.7,
                5.1,
                4.2,
                1.8,
                4.1,
                7.3,
                7.1,
                0.4,
                0.2,
                1.3,
                4.3,
                8.9,
                1.4,
                1.6,
                8.3,
                9.4,
            ]
        ),
    )

    thresholds = np.ndarray(
        shape=(3, 7),
        buffer=np.array(
            [
                0.8,
                1.4,
                1.7,
                3.5,
                5.2,
                6.8,
                8.2,
                0.2,
                2.2,
                3.5,
                4.5,
                6.6,
                8.6,
                9.2,
                1.3,
                4.1,
                4.5,
                6.5,
                7.8,
                8.1,
                8.9,
            ]
        ),
    )

    outputs = np.ndarray(
        shape=(6, 3, 2, 2),
        buffer=np.array(
            [
                4.0,
                3.0,
                1.0,
                4.0,
                5.0,
                2.0,
                2.0,
                4.0,
                3.0,
                3.0,
                3.0,
                1.0,
                5.0,
                0.0,
                1.0,
                4.0,
                1.0,
                4.0,
                6.0,
                7.0,
                7.0,
                1.0,
                1.0,
                3.0,
                3.0,
                3.0,
                1.0,
                3.0,
                4.0,
                2.0,
                3.0,
                7.0,
                3.0,
                3.0,
                1.0,
                1.0,
                7.0,
                5.0,
                4.0,
                6.0,
                2.0,
                2.0,
                1.0,
                1.0,
                2.0,
                1.0,
                3.0,
                3.0,
                2.0,
                5.0,
                3.0,
                3.0,
                4.0,
                5.0,
                7.0,
                3.0,
                1.0,
                3.0,
                2.0,
                1.0,
                4.0,
                6.0,
                6.0,
                0.0,
                1.0,
                1.0,
                3.0,
                6.0,
                1.0,
                1.0,
                6.0,
                7.0,
            ]
        ),
    )

    results = multithreshold(inputs, thresholds)

    assert (results == outputs).all()

    results_scaled = multithreshold(inputs, thresholds, 2.0, -1.0)
    outputs_scaled = 2.0 * outputs - 1.0
    assert (results_scaled == outputs_scaled).all()
