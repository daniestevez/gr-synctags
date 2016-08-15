#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 Daniel Estevez <daniel@destevez.net>.
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>

import numpy
from gnuradio import gr
import pmt

import collections

class fixedlen_tagger(gr.basic_block):
    """
    docstring for block fixedlen_tagger
    """
    def __init__(self, syncword_tag, packetlen_tag, packet_len, stream_type):
        gr.basic_block.__init__(self,
            name="fixedlen_tagger",
            in_sig=[stream_type],
            out_sig=[stream_type])
        self.syncword_tag = pmt.string_to_symbol(syncword_tag)
        self.packetlen_tag = pmt.string_to_symbol(packetlen_tag)
        self.packet_len = packet_len
        self.stream = collections.deque(maxlen=packet_len - 1)
        self.maxtag = 0
        self.data = []
        self.tags = []
        self.written = 0

    def general_work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        window = list(self.stream) + inp.tolist()
        
        alltags = self.get_tags_in_range(0, self.maxtag, self.nitems_read(0) + len(inp), self.syncword_tag)
        for tag in alltags:
            if tag.offset not in self.tags:
                self.maxtag = max(self.maxtag, tag.offset)
                self.tags.append(tag.offset)
        for tag in self.tags:
            if (tag >= self.nitems_read(0) - len(self.stream)) and (tag < self.nitems_read(0) + len(inp) - self.packet_len + 1):
                self.tags.remove(tag)
                start = tag - self.nitems_read(0) + len(self.stream)
                packet = window[start : start + self.packet_len]
                self.data += packet
                self.add_item_tag(0, self.written, self.packetlen_tag, pmt.from_long(self.packet_len))
                self.written += self.packet_len

        self.stream.extend(inp.tolist())

        len_write = min(len(self.data), len(output_items[0]))
        output_items[0][:len_write] = self.data[:len_write]
        self.data = self.data[len_write:]
        self.consume(0, len(inp))
        return len_write
