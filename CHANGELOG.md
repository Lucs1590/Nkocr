## v2.4.2 (2024-04-18)

### Fix

- whell version

## v2.4.1 (2024-04-18)

### Fix

- script using string

## v2.4.0 (2024-04-18)

### Feat

- add timeout to security issue

### Fix

- update file id

## v2.3.1 (2023-11-13)

### Refactor

- remove withespaces

## v2.3.0 (2022-12-25)

### Feat

- docs to all methods in ocr product file
- Add docs to ocr table file
- creating docs to all auxiliary file

### Refactor

- tweak to use in my context

## v2.2.0 (2022-09-13)

### Feat

- updating version automatically
- automatic versioning reader

### Fix

- putting right version
- fix image error

### Refactor

- changing default language

## v2.1.0 (2022-05-18)

### Feat

- changing needed files

### Fix

- **python-app.yml**: setting python version
- deploy

## v2.0.2 (2021-10-15)

### Fix

- **environment.yml**: remove prefix var
- fix tests
- fix tests

## v2.0.1 (2021-04-05)

### Fix

- fix tests

## v2.0.0 (2021-03-19)

### Fix

- fix tests

### Refactor

- **auxiliary.py**: Invalid escape sequence

## v1.8.1 (2020-09-03)

## v1.8.0 (2020-09-03)

### Feat

- naming the integrations class
- **test_ocr_table.py**: add enable_socket at tests
- **test_auxiliary.py**: adding test of download again

### Fix

- **test_ocr_product.py**: add forgeted self]
- removed slow test
- **ocr_table.py**: removing wrong self
- **auxiliary.py**: function identation
- **nkocr.py**: wrong import
- test error

### Refactor

- **test_auxiliary.py**: separating the contents of the auxiliary tests
- **tests**: spliting integration and unit tests
- **tests**: using setUp
- **integration**: add unit main on tests
- **test_auxiliary.py**: changing strings to vars
- **test_ocr_product.py**: pylint recommendation
- **test_auxiliary.py**: pylint recommendations
- **test_ocr_table.py**: pylint recommendations
- **ocr_table.py**: pylint recommendations
- pylint indications
- **ocr_table.py**: making a generic funtion
- separeted horizontal and vertical contours
- reusing download method to url based ocr
- removing wrong class
- **auxiliary.py**: pylint indications
- applying class name convention- ocr_product
- applying class name convention - ocr_table

### Perf

- downgrade version of gdown

## v1.1.0 (2020-08-24)

### Feat

- **auxiliary.py**: increase confidence level
- **auxiliary.py**: sorting the text of the boxes
- **auxiliary**: applying decode and boxes into image
- **auxiliary.py**: method to run EAST
- **auxiliary.py**: add get size and radio functions
- **auxiliary.py**: body of function to east process
- **ocr_table.py**: making body to east process
- **test**: making tests of network
- add pytest_socket into test files
- **auxiliary**: making error treatmensts
- **auxiliary.py**: load model content and get from s3
- add method to get model to east]

### Fix

- fixed broken test error
- **test**: test error

### Refactor

- removed test of tests
- removed test of tests
- **ocr_table.py**: getting only the text result
- **ocr_table**: changing image return by east result
- **test_auxiliary.py**: changing order
- **auxiliary.py**: renaming var
- **auxiliary.py**: add condition to image resize
- changing model place
- talking about the needs of the network
- **test_auxiliary.py**: removing file if exist
- **auxiliary.py**: changing return location

### Perf

- remove unused var and lib

## v1.0.1 (2020-07-30)

### Fix

- fix test errors

## v1.0.0 (2020-07-24)

### Feat

- **test_auxiliary.py**: removing impossible tests
- **test_auxiliary.py**: methods to load image
- **test_auxiliary.py**: structure of tests to auxiliary package
- **ocr_table.py**: add pipeline to each image type process
- **auxiliary.py**: filter of binarization
- **auxiliary.py**: function to make dilatation
- **auxiliary.py**: function to make unsharp filter
- **auxiliary.py**: morphologic open and close filter
- **auxiliary.py**: image resize and dpi upgrade
- **ocr_table.py**: function to remove lines
- **auxiliary**: k-means pack
- **auxiliary.py**: optimization of brightness and contrast
- **auxiliary.py**: remove alpha channel of a image
- **ocr_table.py**: conditional to image type
- **auxiliary.py**: image to opencv type
- **auxiliary.py**: conditional to type of image
- **table_ocr.py**: choosing the classes
- **ocr_table.py**: struture of pipeline

### Fix

- sklearn name
- **auxiliary.py**: putting forgeted selfs
- **auxiliary.py**: puting forgeted selfs

### Refactor

- **ocr_table.py**: renaming function
- **ocr_table.py**: renaming funtion
- **ocr_table.py**: renaming filter
- **ocr_table.py**: rename function

## v0.2.2 (2020-07-17)

## v0.2.1 (2020-07-17)

## v0.2.0 (2020-07-15)

## 0.1.0 (2020-07-14)

## v0.0.3 (2020-07-14)

## v0.0.2 (2020-07-14)
