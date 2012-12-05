TO_DIR=url
if [ ! -d $TO_DIR ]; then
    mkdir $TO_DIR
fi
cd $TO_DIR
for url in `cat ../link.dat | grep 'html\$'`; do
    wget $url 
done
cd ..
