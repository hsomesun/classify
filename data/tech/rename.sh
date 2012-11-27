FROMDIR=parser
SUBJECT=`pwd | awk -F'/' {'print $NF'}`_

for filename in `ls -l $FROMDIR | awk \{'print $8'\}`; do
    echo $FROMDIR/$SUBJECT$filename
    mv $FROMDIR/$filename $FROMDIR/$SUBJECT$filename
done

TRAINDIR=../../train
TESTDIR=../../test
if [ ! -d $TRAINDIR ]; then
    mkdir $TRAINDIR
fi
if [ ! -d $TESTDIR ]; then
    mkdir $TESTDIR
fi

for filename in `ls -l $FROMDIR | head -200 | awk \{'print $8'\}`; do
    cp $FROMDIR/$filename $TESTDIR
done
for filename in `ls -l $FROMDIR | tail -n +200 | awk \{'print $8'\}`; do
    cp $FROMDIR/$filename $TRAINDIR
done
