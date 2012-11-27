TEST_DIR=test
TRAIN_DIR=train
for filename in `ls -l $TRAIN_DIR | awk '{if($5 < 300) {print $8}}'`; do
    rm $TRAIN_DIR/$filename
done

for filename in `ls -l $TEST_DIR | awk '{if($5 < 300) {print $8}}'`; do
    rm $TEST_DIR/$filename
done

