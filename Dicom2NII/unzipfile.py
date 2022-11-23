import zipfile
import logging


def unzip(zip_file, out_dir):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(out_dir)

in_file = r"C:\Users\liw66\Downloads\Cadaver_H12968-CT_Full body_2019-02-19.zip"
out_dir = r"C:\Users\liw66\Downloads"

# unzip(in_file, out_dir)

# show progress
# zf = zipfile.ZipFile(in_file)
#
# uncompress_size = sum((file.file_size for file in zf.infolist()))
#
# extracted_size = 0
#
# for file in zf.infolist():
#     extracted_size += file.file_size
#     print("%s %%" % (extracted_size * 100/uncompress_size))
#     zf.extract(file, out_dir)

# create logger
# logger = logging.getLogger('simple_example')
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
