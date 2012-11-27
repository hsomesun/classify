FROMDIR=train
TODIR=parser
DPWD=`pwd`
FROMPATH=$DPWD/$FROMDIR
TOPATH=$DPWD/$TODIR
echo $FROMPATH
echo $TOPATH
mkdir $TOPATH
cd ../../parser
for filename in `ls -l $FROMPATH | awk \{'print $8'\}`; do
    echo $FROMPATH/$filename
    ./parser $FROMPATH/$filename $TOPATH/$filename
done
cd -

