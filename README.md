# EMGTrignoAPI

API of the Application to process EMG Trigno data

## Install
```shell
pip install -r requirements.txt
```
## Configure
Change ```configuration.py``` file content according to your needs.

## Build
```shell
pyinstaller --paths 'src' \
	--collect-all charset_normalizer \
	--collect-all reportlab.graphics.barcode \
	--console \
	--clean \
	--name EMGTrignoAPI \
	--icon='src/assets/icons/win/app.ico' \
	app.py --noconfirm
```

## Authors

- [**Florentin Thullier**](https://github.com/FlorentinTh) - 2022

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
