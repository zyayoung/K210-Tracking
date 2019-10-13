/* Copyright 2018 Canaan Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <stdlib.h>
#include "image_process.h"

int min(int a, int b){return a<b?a:b;}

int image_init(image_t *image)
{
    image->addr = calloc(image->width * image->height * image->pixel, 1);
    if (image->addr == NULL)
        return -1;
    return 0;
}

void image_deinit(image_t *image)
{
    free(image->addr);
}

int image_crop(image_t *src, image_t *dst, int x, int y, int w, int h, int stride){
    int wh_dst = dst->width * dst->height;
    int wh_src = src->width * src->height;
    int channel = min(src->pixel, dst->pixel);
    if(channel==2){
        for(int j=y, dst_j=0; dst_j<h; j+=stride, dst_j++)
            for(int i=x, dst_i=0; dst_i<w; i+=stride, dst_i++)
                    ((uint16_t*)dst->addr)[dst_j * dst->width + dst_i] = ((uint16_t*)src->addr)[j * src->width + i];
        return 0;
    }
    for(int c=0; c < channel; c++)
        for(int j=y, dst_j=0; dst_j<h; j+=stride, dst_j++)
            for(int i=x, dst_i=0; dst_i<w; i+=stride, dst_i++)
                    dst->addr[c * wh_dst + dst_j * dst->width + dst_i] = src->addr[c * wh_src + j * src->width + i];
    return 0;
}
