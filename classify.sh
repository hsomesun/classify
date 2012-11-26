TEST_FILE=$2
TEST_DOWNLOAD_FILE=$TEST_FILE.download

if [ -z $1 ] && [ -z $2 ]; then
    echo 'Argument too low, need 2 argument'
else
    (curl $1 | grep '<p>.*</p>' | iconv -t utf-8 -f gb2312 -c > $DOWNLOAD_DIR/$TEST_DOWNLOAD_FILE) || exit 
    python parser.py $DOWNLOAD_DIR/$TEST_DOWNLOAD_FILE 
    
fi
