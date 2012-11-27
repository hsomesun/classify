for url in `cat link.dat | grep 'html\$'`; do
    wget $url 
done
TO_DIR=url
mkdir $TO_DIR
for filename in `ls -l *.html | awk {'print $8'}`;do
    mv $filename $TO_DIR
done
