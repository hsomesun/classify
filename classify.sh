TEST_FILE=$2
TEST_DOWNLOAD_FILE=$TEST_FILE.download
TEST_EXTRACT_FILE=$TEST_FILE.extra
DOWNLOAD_DIR=download

if [ -z $1 ] && [ -z $2 ]; then
    echo 'Argument too low, need 2 argument'
else
    if [ ! -d $DOWNLOAD_DIR ]; then
	mkdir $DOWNLOAD_DIR
    fi
    (curl $1 | grep '<p>.*</p>' | iconv -t utf-8 -f gb2312 -c > $DOWNLOAD_DIR/$TEST_DOWNLOAD_FILE) || exit 
    python parser.py $DOWNLOAD_DIR/$TEST_DOWNLOAD_FILE > $DOWNLOAD_DIR/$TEST_EXTRACT_FILE
    rm $DOWNLOAD_DIR/$TEST_DOWNLOAD_FILE
    cd parser
    ./parser ../$DOWNLOAD_DIR/$TEST_EXTRACT_FILE ../$DOWNLOAD_DIR/$TEST_FILE
    cd ..
    rm $DOWNLOAD_DIR/$TEST_EXTRACT_FILE
    python test.py $DOWNLOAD_DIR/$TEST_FILE
fi
