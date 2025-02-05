#!/usr/bin/env python
#
# Copyright (C) 2018 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
import sys
import importlib

def main(argv):
    importlib.reload(sys)
    original_file = 'vendor/devolution/prebuilt/common/etc/apns-conf.xml'

    if len(argv) == 3:
        output_file_path = argv[1]
        custom_override_file = argv[2]
    else:
        raise ValueError("Wrong number of arguments %s" % len(argv))

    custom_apn_names = set()
    with open(custom_override_file, 'r', encoding='utf-8') as f:
        for line in f:
            name = re.search(r'carrier="[^"]+"', line).group(0)
            mcc = re.search(r'mcc="[^"]+"', line).group(0)
            mnc = re.search(r'mnc="[^"]+"', line).group(0)
            custom_apns.append({'name': name, 'mcc': mcc, 'mnc': mnc})

    with open(original_file, 'r', encoding='utf-8') as input_file:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in input_file:
                found_custom_apns = set()
                for apn in custom_apn_names:
                    if apn in line:
                        with open(custom_override_file, 'r', encoding='utf-8') as custom_file:
                            for override_line in custom_file:
                                if all(item in override_line for item in apn.values()):
                                    output_file.write(override_line)
                                    found_custom_apns.append(apn)
                if found_custom_apns:
                    for found in found_custom_apns:
                        custom_apns.remove(found)
                else:
                    if "</apns>" in line:
                        if custom_apn_names:
                            for apn in custom_apn_names:
                                with open(custom_override_file, 'r', encoding='utf-8') as custom_file:
                                    for override_line in custom_file:
                                        if all(item in override_line for item in apn.values()):
                                            output_file.write(override_line)
                    output_file.write(line)

if __name__ == '__main__':
    main(sys.argv)
