TODIR=train
TEMPDIR=tmp
FROMDIR=html
if [ ! -d $TEMPDIR ]; then
    mkdir $TEMPDIR
fi

if [ ! -d $TODIR ]; then
    mkdir $TODIR
fi
echo '================step 1==========================='
for filename in `ls -l $FROMDIR | awk \{'print $NF'\}`; do
    cat $FROMDIR/$filename | grep '<p>.*</p>' > $TEMPDIR/$filename
done
echo '================step 2==========================='
cd $TEMPDIR && ls -l | grep '\<0\>' | awk {'print $NF'} | xargs rm || exit
cd ..
echo '================step 3==========================='
for filename in `ls -l $TEMPDIR | awk \{'print $NF'\}`; do
    python parser.py $TEMPDIR/$filename > $TODIR/$filename
done
echo '================step 4==========================='
if [ -d $TEMPDIR ]; then
    rm -r $TEMPDIR
fi
echo '================end==========================='
