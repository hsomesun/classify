TODIR=html
FROMDIR=url
if [ ! -d $TODIR ]; then
    mkdir $TODIR
fi
    
for filename in `ls -l url | awk \{'print $NF'\}`; do
    iconv -t utf-8 -f gb2312 -c $FROMDIR/$filename > $TODIR/$filename
done
