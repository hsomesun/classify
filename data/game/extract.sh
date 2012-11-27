TODIR=train
TEMPDIR=tmp
FROMDIR=html
mkdir $TEMPDIR
mkdir $TODIR
echo '================step 1==========================='
for filename in `ls -l $FROMDIR | awk \{'print $8'\}`; do
    cat $FROMDIR/$filename | grep '<p>.*</p>' > $TEMPDIR/$filename
done
echo '================step 2==========================='
cd $TEMPDIR && ls -l | grep '\<0\>' | awk {'print $8'} | xargs rm && cd ..
echo '================step 3==========================='
for filename in `ls -l $TEMPDIR | awk \{'print $8'\}`; do
    python parser.py $TEMPDIR/$filename > $TODIR/$filename
done
echo '================step 4==========================='
rm -r $TEMPDIR
echo '================end==========================='
