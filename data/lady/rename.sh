FROMDIR=parser
SUBJECT=lady_
for filename in `ls -l $FROMDIR | awk \{'print $8'\}`; do
    echo $FROMDIR/$SUBJECT$filename
    mv $FROMDIR/$filename $FROMDIR/$SUBJECT$filename
done
TRAINDIR=/home/administrator/cs/dataminer/train
TESTDIR=/home/administrator/cs/dataminer/test
for filename in `ls -l $FROMDIR | head -200 | awk \{'print $8'\}`; do
    cp $FROMDIR/$filename $TESTDIR
done
for filename in `ls -l $FROMDIR | tail -n +200 | awk \{'print $8'\}`; do
    cp $FROMDIR/$filename $TRAINDIR
done
