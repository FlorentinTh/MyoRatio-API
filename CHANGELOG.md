# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### [3.4.1](https://github.com/FlorentinTh/MyoRatio-API/compare/v3.4.0...v3.4.1) (2023-10-27)


### Bug Fixes

* **app:** fix several security issues related to path sanitization ([16ef5cf](https://github.com/FlorentinTh/MyoRatio-API/commit/16ef5cf079c16ad5b47ac69db96fa7110af7b125))
* **pandas:** fix few issues with latest update of pandas dependency ([0df6e64](https://github.com/FlorentinTh/MyoRatio-API/commit/0df6e6465aa43cd81604a73b83b1beb0e49bfbe7))
* **project:** add missing entries for macOs platform in .gitignore file ([25b8b59](https://github.com/FlorentinTh/MyoRatio-API/commit/25b8b59c200cc80344c0a9a26f23fdb603a6700b))


### Documentation

* **README:** fix issue in README related to the path for CodeQL badge ([538c740](https://github.com/FlorentinTh/MyoRatio-API/commit/538c740ca9146da28ad1ad67a62833a642746873))
* **README:** update README to add CodeQL badge ([8f5dccb](https://github.com/FlorentinTh/MyoRatio-API/commit/8f5dccb06d9b099fb882c4055ca814c6dff593bc))
* **readme:** update readme.md file ([ebebdc9](https://github.com/FlorentinTh/MyoRatio-API/commit/ebebdc9ff0bd646ef4b5bfd53fede4f7a1715a38))
* **readme:** update README.md file ([1c58057](https://github.com/FlorentinTh/MyoRatio-API/commit/1c5805794b5c6aa8730db671c2343c4d37719f11))
* **readme:** yet another fix in README related to the path for CodeQL badge ([7719f48](https://github.com/FlorentinTh/MyoRatio-API/commit/7719f4894772c2953cdb37cf3036e00185e51af4))


### Build System

* **dependencies:** update dask and xlsxwriter to their latest versions ([0dc12e1](https://github.com/FlorentinTh/MyoRatio-API/commit/0dc12e1293905240740bb98206dd22d81f215227))
* **dependencies:** update dependencies ([f55827f](https://github.com/FlorentinTh/MyoRatio-API/commit/f55827f71bb063850556cf7905f431d6f99d963b))
* **dependencies:** update pandas dependency to latest version ([2ada5ee](https://github.com/FlorentinTh/MyoRatio-API/commit/2ada5ee2086efeef32730dbff8decad297d3310d))
* **dependencies:** update project dependencies ([a2a57cf](https://github.com/FlorentinTh/MyoRatio-API/commit/a2a57cf9855d6ebffac94d8eefc8c1f047ab6c02))
* **dependencies:** update pyinstaller to the latest version ([2090fbe](https://github.com/FlorentinTh/MyoRatio-API/commit/2090fbe4493f0252c1ad41ff48c7fd7f5fd825cf))
* **dependencies:** update scipy to new version and revert pandas to previous version since ^2.1.0 introduced breaking changes ([c2dd6c0](https://github.com/FlorentinTh/MyoRatio-API/commit/c2dd6c05d0a805558dbad10f3827f5e885711689))
* **dependencies:** update xlsxwriter to latest version ([c188273](https://github.com/FlorentinTh/MyoRatio-API/commit/c188273ddf637d117bc064dfbb98d488797779d3))
* **poetry:** fix potential issue with poetry make commands for both platforms ([ebe5da1](https://github.com/FlorentinTh/MyoRatio-API/commit/ebe5da115d59f4b7116a7e70b2dc2ba34270b040))
* **poetry:** yet another potential fix to resolve issue with poetry make commands for both platforms ([07736d0](https://github.com/FlorentinTh/MyoRatio-API/commit/07736d0e6aa95b6e0a43efa86351adb4bbd1d0eb))
* **poetry:** yet another potential fix to resolve issue with poetry make commands for both platforms ([a38d4fc](https://github.com/FlorentinTh/MyoRatio-API/commit/a38d4fc5557f4fa861f7a7d9076fc26041908f91))
* **project:** add code of conduct and contributing guidelines ([c97e464](https://github.com/FlorentinTh/MyoRatio-API/commit/c97e464511d107efc977308dc72d049ab518f5bc))
* **project:** add security guidelines in SECURITY.md ([f95b7aa](https://github.com/FlorentinTh/MyoRatio-API/commit/f95b7aa1c0ee6631d4343b93ed14c2e6fbe42641))
* **project:** dependabot ([3d6eb32](https://github.com/FlorentinTh/MyoRatio-API/commit/3d6eb32551208446898d023051b331e5c0ff0887))
* **project:** dependencies ([da79f61](https://github.com/FlorentinTh/MyoRatio-API/commit/da79f6170d238fa93e220aeec8b952f26e492afa))
* **project:** dependencies ([3ea0f37](https://github.com/FlorentinTh/MyoRatio-API/commit/3ea0f376d5eb722e80a2b79517981b25224c8b5d))

## [3.4.0](https://github.com/FlorentinTh/MyoRatio-API/compare/v3.3.0...v3.4.0) (2023-10-04)


### Bug Fixes

* **summmary:** force lower case of stage name for summary output filename ([7ba78c1](https://github.com/FlorentinTh/MyoRatio-API/commit/7ba78c1540a2bdbd4c51fe9963dbf6e4cb5a363d))


### Styling

* **readme:** clean readme ([d3de324](https://github.com/FlorentinTh/MyoRatio-API/commit/d3de3244a9858b4a0b0a6d2db0546972a2ee17ef))
* **readme:** update main title ([55bf530](https://github.com/FlorentinTh/MyoRatio-API/commit/55bf530636851aac5c2e064b5fa33711018ab339))


### Documentation

* **readme:** update readme ([918a7a6](https://github.com/FlorentinTh/MyoRatio-API/commit/918a7a655931796cbbefa49051ff328cc81b6770))
* **README:** update README ([d80b540](https://github.com/FlorentinTh/MyoRatio-API/commit/d80b540ba01da6458eb97de6b729af9e328e491a))

## [3.3.0](https://github.com/FlorentinTh/MyoRatio-API/compare/v3.2.0...v3.3.0) (2023-09-18)


### Bug Fixes

* **plot_helper:** move from IMU plot outputed in SVG to PNG for fixing laggy DOM issue in GUI ([3796e99](https://github.com/FlorentinTh/MyoRatio-API/commit/3796e994f4990432b6c1a21e8e876904e50cf516))


### Build System

* **pyproject.toml:** change build command to remove collection of packages that are no longer required ([12c89cb](https://github.com/FlorentinTh/MyoRatio-API/commit/12c89cb6bd2801e31c9def67f67677492a2d714a))

## [3.2.0](https://github.com/FlorentinTh/MyoRatio-API/compare/v3.1.1...v3.2.0) (2023-09-10)


### Bug Fixes

* **summary:** fix issue with summray generation sort data by type of participants ([0b63803](https://github.com/FlorentinTh/MyoRatio-API/commit/0b63803c73839ac0b411f18b69909ab3d62cafd9))

### [3.1.1](https://github.com/FlorentinTh/MyoRatio-API/compare/v3.1.0...v3.1.1) (2023-08-10)


### Bug Fixes

* **dependencies:** update dependency tree ([f8df39d](https://github.com/FlorentinTh/MyoRatio-API/commit/f8df39d1446da56965c2c58678f2a08a167622a7))

## [3.1.0](https://github.com/FlorentinTh/MyoRatio-API/compare/v3.0.3...v3.1.0) (2023-08-09)


### Bug Fixes

* **configuration:** move configuration from python-dotenv to environs ([46a0d58](https://github.com/FlorentinTh/MyoRatio-API/commit/46a0d5811bdcf863d2cd57db36ceebf84bffa9d8))
* **dependencies:** change and update required dependencies ([1311169](https://github.com/FlorentinTh/MyoRatio-API/commit/13111694997138b690a651e98d451b29de14b95c))

### [3.0.3](https://github.com/FlorentinTh/MyoRatio-API/compare/v3.0.2...v3.0.3) (2023-08-08)

### [3.0.2](https://github.com/FlorentinTh/MyoRatio-API/compare/v3.0.1...v3.0.2) (2023-08-08)

### [3.0.1](https://github.com/FlorentinTh/MyoRatio-API/compare/v3.0.0...v3.0.1) (2023-08-04)

## [3.0.0](https://github.com/FlorentinTh/MyoRatio-API/compare/v2.6.2...v3.0.0) (2023-08-03)


### ⚠ BREAKING CHANGES

* **application:** endpoints body parameters have changed

### Features

* **application:** add support for dynamic configuration related to changes in GUI ([48d2e32](https://github.com/FlorentinTh/MyoRatio-API/commit/48d2e32522f0204bdff9a0067cee33b8f327a997))


### Bug Fixes

* **report:** fix issue with order of area charts ([45900a3](https://github.com/FlorentinTh/MyoRatio-API/commit/45900a32ca580072ab3ab2acb14a0ba500352b80))
* **string_helper:** fix issue with analysis label containing "-" characters ([bf8bed3](https://github.com/FlorentinTh/MyoRatio-API/commit/bf8bed3760721c10a87cb889c3a900019953acc3))

### [2.6.2](https://github.com/FlorentinTh/MyoRatio-API/compare/v2.6.1...v2.6.2) (2023-07-14)


### Build System

* **standard-version:** add missing .versionrc configuration to better handle changelog generation ([23e1b94](https://github.com/FlorentinTh/MyoRatio-API/commit/23e1b947c8bd4aa7a09e5e9a55e62a666702faca))

### [2.6.1](https://github.com/FlorentinTh/MyoRatio-API/compare/v2.6.0...v2.6.1) (2023-07-14)


### Build System

* **deps:** update dependencies ([8c0825c](https://github.com/FlorentinTh/MyoRatio-API/commit/8c0825ce45214da9cfa6beaa60f967743587c8fc))

## [2.6.0](https://github.com/FlorentinTh/MyoRatio-API/compare/v2.5.0...v2.6.0) (2023-07-14)


### Features

* **auth:** override handler for 401 errors ([948be15](https://github.com/FlorentinTh/MyoRatio-API/commit/948be15c1a2d2e31ae905ec6244429c6fc462796))


### Bug Fixes

* **configuration:** fix some issues with configuration validation ([4bf97b2](https://github.com/FlorentinTh/MyoRatio-API/commit/4bf97b28f22a786118b6298ee7755d2c23169755))
* **configuration:** move to proper environment file for sensitive configuration data and refactor server.py ([52e3cb8](https://github.com/FlorentinTh/MyoRatio-API/commit/52e3cb8ee0d1c27c2c622ea0804923a8c458e2c6))
* **pyproject:** fix macos build command ([69a2319](https://github.com/FlorentinTh/MyoRatio-API/commit/69a231989f7d60f67d92a4f03603533fdbe9bd5a))

## [2.5.0](https://github.com/FlorentinTh/MyoRatio-API/compare/v2.4.0...v2.5.0) (2023-07-09)


### Features

* **summary:** add report summary feature ([869c6c6](https://github.com/FlorentinTh/MyoRatio-API/commit/869c6c65cd2096769d75c28a5dca80ca4639a6d1))
* **xlsx_helper:** move xlsx formats defined in report to a dedicated helper ([b075207](https://github.com/FlorentinTh/MyoRatio-API/commit/b075207a8d59fb8e7ccb783128f85ffad473cbac))


### Bug Fixes

* **ratio:** add verification on tuple muscles return type ([99b3f23](https://github.com/FlorentinTh/MyoRatio-API/commit/99b3f23edd008c484720cd2b95e483e319bf29ba))
* **summary:** add an error handler when there are no report files ([89a6d97](https://github.com/FlorentinTh/MyoRatio-API/commit/89a6d97db2440e2b8509579ff97c7da697f2b04f))

## [2.4.0](https://github.com/FlorentinTh/MyoRatio-API/compare/v2.3.0...v2.4.0) (2023-06-19)


### ⚠ BREAKING CHANGES

* **results:**
* **emg:**

### Features

* **imu:** remove unrelated data when sensor is cut ([caa5e61](https://github.com/FlorentinTh/MyoRatio-API/commit/caa5e61c483a0e7a50cd0b833171865648b1040a))
* **ratio:** add enum for all muscles that may be part of the ratio computation ([acf57cf](https://github.com/FlorentinTh/MyoRatio-API/commit/acf57cfd0373b93333e0b0e6a68264fb3f0f0acd))
* **results:** add sit-stand analysis computation of ratios ([4c1135a](https://github.com/FlorentinTh/MyoRatio-API/commit/4c1135a927d8b5d5db97a11a8bcc0ad0e549dbd1))


### Bug Fixes

* **imu:** add missing check on by 0 division ([43c7f53](https://github.com/FlorentinTh/MyoRatio-API/commit/43c7f538cb9e099d9883aede3e7e0ce0d0a62587))
* **ratio:** add missing analysis muscles combinations ([5f424cf](https://github.com/FlorentinTh/MyoRatio-API/commit/5f424cf6f4f4995e5213b74cb03d6f95c69e85e4))
* **report:** fix issue with area charts generation ([faa5043](https://github.com/FlorentinTh/MyoRatio-API/commit/faa50433d3f574862ef984febc8b2863eeb7548f))
* **report:** remove area chart stacked subtype ([ba00d07](https://github.com/FlorentinTh/MyoRatio-API/commit/ba00d076e3f7eadd6aac3653356697a733d698e8))
* **results:** fix an issue with stage switching computing wrong angle for the report ([4b3323a](https://github.com/FlorentinTh/MyoRatio-API/commit/4b3323a962e1c538463a5541d06238c754ad4251))
* **results:** revised version of the generation of the results given the analysis and stage ([1b37cd7](https://github.com/FlorentinTh/MyoRatio-API/commit/1b37cd7d894ff1d8a24e8e33bb80346a816c4e4c))


* **emg:** update normalized angles data output file name to match naming convention ([9bb6ab7](https://github.com/FlorentinTh/MyoRatio-API/commit/9bb6ab76f7a363efa9f28d8944008ccc6de4274c))

## [2.3.0](https://github.com/FlorentinTh/MyoRatio-API/compare/v2.2.0...v2.3.0) (2023-05-29)


### Bug Fixes

* **imu:** change the way angles are computed ([62ed6c2](https://github.com/FlorentinTh/MyoRatio-API/commit/62ed6c27db686dc1c070724483167cdc48766b4b))

## [2.2.0](https://github.com/FlorentinTh/MyoRatio-API/compare/v2.0.0...v2.2.0) (2023-05-20)

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
