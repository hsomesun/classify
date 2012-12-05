FROMDIR=train
TODIR=parser
DPWD=`pwd`
FROMPATH=$DPWD/$FROMDIR
TOPATH=$DPWD/$TODIR
echo $FROMPATH
echo $TOPATH
if [ ! -d $TOPATH ]; then
    mkdir $TOPATH
fi
cd ../../parser
for filename in `ls -l $FROMPATH | awk \{'print $NF'\}`; do
    echo $FROMPATH/$filename
    ./parser $FROMPATH/$filename $TOPATH/$filename
done
cd -

