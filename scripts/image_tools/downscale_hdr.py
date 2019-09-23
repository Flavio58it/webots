# Copyright 1996-2019 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Downscale an HDR image to a specified size."""

import optparse
import os

from utils.clamp import clamp_int
from images.hdr import HDR
from images.regular_image import RegularImage

optParser = optparse.OptionParser(usage='usage: %prog --input=image.hdr')
optParser.add_option(
    '--input', '-i', dest='input', default='image.hdr', type='string',
    help='specifies the input HDR image path'
)
optParser.add_option(
    '--width', dest='width', default=256, type='int',
    help='specifies the width of the target image.'
)
optParser.add_option(
    '--height', dest='height', default=256, type='int',
    help='specifies the height of the target image.'
)
options, args = optParser.parse_args()

hdr_path = options.input
result_path = hdr_path.replace('.hdr', '.' + options.format)

assert hdr_path.endswith('.hdr'), 'Invalid input extension.'
assert hdr_path != result_path, 'Identical input and output paths.'
assert os.path.isfile(hdr_path), 'Input file doest not exits.'

print('Load the HDR image...')
hdr = HDR.load_from_file(hdr_path)
assert hdr.is_valid(), 'Invalid input HDR file.'

print('Create the result image')
result = RegularImage.create_black_image(hdr.width, hdr.height)
for y in range(hdr.height):
    for x in range(hdr.width):
        pixel = hdr.get_pixel(x, y)
        pixel = (
            clamp_int(255.0 * pixel[0], 0, 255),
            clamp_int(255.0 * pixel[1], 0, 255),
            clamp_int(255.0 * pixel[2], 0, 255)
        )
        result.set_pixel(x, y, pixel)
if format == 'jpg':
    result.save(result_path, quality=options.quality)
else:
    result.save(result_path)
