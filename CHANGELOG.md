# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [2.0.0](https://github.com/FlorentinTh/MyoRatio-API/compare/v1.2.0...v2.0.0) (2023-05-09)


### Bug Fixes

* **project:** rename project from EMG Trigno to MyoRatio ([27bc63e](https://github.com/FlorentinTh/MyoRatio-API/commit/27bc63e63999f0b9ae7415ed5e824833e1d16930))

## [2.0.0](https://github.com/FlorentinTh/MyoRatio-API/compare/v1.2.0...v2.0.0) (2023-05-09)


### Bug Fixes

* **project:** rename project from EMG Trigno to MyoRatio ([27bc63e](https://github.com/FlorentinTh/MyoRatio-API/commit/27bc63e63999f0b9ae7415ed5e824833e1d16930))

## [1.2.0](https://github.com/FlorentinTh/EMG-Trigno-API/compare/v1.0.0...v1.2.0) (2023-05-09)


### ⚠ BREAKING CHANGES

* **project:** several features have been either moved or removed

### Features

* **api:** add ping route for api to allow GUI check if it is correctly started ([c674ba1](https://github.com/FlorentinTh/EMG-Trigno-API/commit/c674ba1613aadff322c226d0b8e995c383f77ab5))
* **imu:** add generation of filtered imu data ([c2285d4](https://github.com/FlorentinTh/EMG-Trigno-API/commit/c2285d41dcc826a903763da31e8c6f47e73eb1b4))
* **points:** add skeleton code for points auto-selection ([9716a09](https://github.com/FlorentinTh/EMG-Trigno-API/commit/9716a09d0e3dfc2dc639aceddcd841d17587b22d))
* **points:** complete real dynamic points retrieval for the auto-angles feature ([4c81b7e](https://github.com/FlorentinTh/EMG-Trigno-API/commit/4c81b7e3f8873b5e5b3c829147ee300f4b36341c))
* **report:** add xlsx report creation feature ([7d9b00e](https://github.com/FlorentinTh/EMG-Trigno-API/commit/7d9b00eea6da0fd4d1ec553dd24773f2c8825eaf))
* **report:** change pdf creation process, now use html template directly in the API ([c7584b2](https://github.com/FlorentinTh/EMG-Trigno-API/commit/c7584b290be338242a5eae94e33df6c00cecada4))
* **server:** port is now provided as argv parameter to allow multiple app instances to be launched ([433d8a2](https://github.com/FlorentinTh/EMG-Trigno-API/commit/433d8a26e26e95ca3d2371808b8a859acdb9d118))


### Bug Fixes

* **.gitignore:** add a missing .gitignore entry ([b7ef244](https://github.com/FlorentinTh/EMG-Trigno-API/commit/b7ef2441cab73eee4d093cdb8e892517274194ed))
* **analysis:** add missing analysis value ([6b8abae](https://github.com/FlorentinTh/EMG-Trigno-API/commit/6b8abaee62051309208aefbe07b4ebd4c30e6d51))
* **app:** add missing error handling ([9e6aed1](https://github.com/FlorentinTh/EMG-Trigno-API/commit/9e6aed12ca1e6bfa1020cef0e4751aa03a43d7ab))
* **app:** fix issue with body verification return when body is empty ([08e750e](https://github.com/FlorentinTh/EMG-Trigno-API/commit/08e750ec5f49f2c1d2bfa07e4399d8d162923cd8))
* **data:** fix a bug related to type in data csv file read ([efed8fb](https://github.com/FlorentinTh/EMG-Trigno-API/commit/efed8fb662723941712625705a37c2086a740ca6))
* **deps:** update dependencies ([7cb91d2](https://github.com/FlorentinTh/EMG-Trigno-API/commit/7cb91d270799fb08be1a7b49f5269806874373c3))
* **points:** fix severe issue related to floating point ([bbbd199](https://github.com/FlorentinTh/EMG-Trigno-API/commit/bbbd1996ae0b143000778e298018b9b4ce3a8150))
* **report:** move report HTML template to assets directory and replace its path in report module ([1db2170](https://github.com/FlorentinTh/EMG-Trigno-API/commit/1db2170bcac3c46b09a58e5197a33c95b1aa89c4))
* **report:** move report template to GUI ([e13850a](https://github.com/FlorentinTh/EMG-Trigno-API/commit/e13850a3f51dbab3e0c88f6e616a55b84fcb3810))


* **project:** huge refactor of the whole project to handle missing data required for xlsx reports ([ebb9a0a](https://github.com/FlorentinTh/EMG-Trigno-API/commit/ebb9a0a64b8ed9fd32fe0dd8c023d1bd5135ac5a))

## 1.0.0 (2023-02-13)


### Features

* **results:** add results class moved from GUI ([40b8ea4](https://github.com/FlorentinTh/EMG-Trigno-API/commit/40b8ea4c7594fff31f52c4ba5683faee30fa1a94))


### Bug Fixes

* **app:** error handling, optimizations & file management ([00d7456](https://github.com/FlorentinTh/EMG-Trigno-API/commit/00d7456a5f0e33543d48e385b9ff1a24ce2c716f))
* **app:** minor fix ([6b01b3d](https://github.com/FlorentinTh/EMG-Trigno-API/commit/6b01b3dd374b2aaa75c0044e013fc171038252d7))
* **app:** server close properly & accept concurrency ([787ac49](https://github.com/FlorentinTh/EMG-Trigno-API/commit/787ac491eec153692d9388b5b8bc52a6d42a49ba))
* **imu:** filter acc data based on the analysis ([7b0d786](https://github.com/FlorentinTh/EMG-Trigno-API/commit/7b0d7862a9be624ecd52e5878b951e4678305408))
