TODIR=html
FROMDIR=url
mkdir $TODIR
for filename in `ls -l url | awk \{'print $8'\}`; do
    iconv -t utf-8 -f gb2312 -c $FROMDIR/$filename > $TODIR/$filename
done
