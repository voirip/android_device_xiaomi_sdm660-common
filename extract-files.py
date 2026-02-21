#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/sdm660-common',
    'hardware/qcom-caf/msm8998',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/data-ipa-cfg-mgr-legacy-um',
    'vendor/qcom/opensource/dataservices',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.dsi.ant@1.0',
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.hardware.fm@1.0',
    ): lib_fixup_vendor_suffix,
    (
        'libOmxCore',
        'libllvd_smore',
        'libloc_core',
        'liblocation_api',
        'libwifi-hal-ctrl',
        'libwpa_client',
    ): lib_fixup_remove,
}


blob_fixups: blob_fixups_user_type = {
    'system_ext/bin/dpmd': blob_fixup()
        .replace_needed('com.qualcomm.qti.dpm.api@1.0.so', 'com.qualcomm.qti.dpm.api@1.0_vendor.so'),

    'vendor/bin/hw/android.hardware.bluetooth@1.0-service-qti': blob_fixup()
        .remove_needed('vendor.qti.hardware.bluetooth_sar@1.1.so'),

    'vendor/lib/libadsprpc.so': blob_fixup()
        .remove_needed('vendor.qti.hardware.dsp@1.0.so'),
    'vendor/lib64/libadsprpc.so': blob_fixup()
        .remove_needed('vendor.qti.hardware.dsp@1.0.so'),
    'vendor/lib/libcdsprpc.so': blob_fixup()
        .remove_needed('vendor.qti.hardware.dsp@1.0.so'),
    'vendor/lib64/libcdsprpc.so': blob_fixup()
        .remove_needed('vendor.qti.hardware.dsp@1.0.so'),
    'vendor/lib/libmdsprpc.so': blob_fixup()
        .remove_needed('vendor.qti.hardware.dsp@1.0.so'),
    'vendor/lib64/libmdsprpc.so': blob_fixup()
        .remove_needed('vendor.qti.hardware.dsp@1.0.so'),
    'vendor/lib/libsdsprpc.so': blob_fixup()
        .remove_needed('vendor.qti.hardware.dsp@1.0.so'),
    'vendor/lib64/libsdsprpc.so': blob_fixup()
        .remove_needed('vendor.qti.hardware.dsp@1.0.so'),

    'system_ext/lib64/libdpmframework.so': blob_fixup()
        .replace_needed('com.qualcomm.qti.dpm.api@1.0.so', 'com.qualcomm.qti.dpm.api@1.0_vendor.so'),
    'system_ext/lib64/libdpmctmgr.so': blob_fixup()
        .replace_needed('com.qualcomm.qti.dpm.api@1.0.so', 'com.qualcomm.qti.dpm.api@1.0_vendor.so'),
    'system_ext/lib64/libdpmfdmgr.so': blob_fixup()
        .replace_needed('com.qualcomm.qti.dpm.api@1.0.so', 'com.qualcomm.qti.dpm.api@1.0_vendor.so'),
    'system_ext/lib64/libdpmtcm.so': blob_fixup()
        .replace_needed('com.qualcomm.qti.dpm.api@1.0.so', 'com.qualcomm.qti.dpm.api@1.0_vendor.so'),

    'system_ext/lib64/libfm-hci.so': blob_fixup()
        .replace_needed('vendor.qti.hardware.fm@1.0.so', 'vendor.qti.hardware.fm@1.0_vendor.so'),
    'system_ext/lib64/fm_helium.so': blob_fixup()
        .replace_needed('vendor.qti.hardware.fm@1.0.so', 'vendor.qti.hardware.fm@1.0_vendor.so'),

    (
        'vendor/bin/mlipayd@1.1',
    ): blob_fixup()
        .remove_needed('vendor.xiaomi.hardware.mtdservice@1.0.so'),
    (
        'vendor/lib64/libmlipay.so',
        'vendor/lib64/libmlipay@1.1.so',
    ): blob_fixup()
        .remove_needed('vendor.xiaomi.hardware.mtdservice@1.0.so')
        .binary_regex_replace(b'/system/etc/firmware', b'/vendor/firmware\x00\x00\x00\x00'),
    (
        'vendor/bin/pm-service',
    ): blob_fixup()
        .add_needed('libutils-v33.so'),
    (
        'vendor/lib64/libwvhidl.so',
    ): blob_fixup()
        .add_needed('libcrypto_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sdm660-common',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
